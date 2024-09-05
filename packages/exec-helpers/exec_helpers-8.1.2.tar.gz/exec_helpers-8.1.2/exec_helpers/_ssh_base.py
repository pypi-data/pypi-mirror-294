#    Copyright 2018 - 2023 Aleksei Stepanov aka penguinolog.

#    Copyright 2013 - 2016 Mirantis, Inc.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at

#         http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""SSH client helper based on Paramiko. Base class."""

from __future__ import annotations

import concurrent.futures
import copy
import datetime
import getpass
import logging
import pathlib
import shlex
import stat
import time
import typing
import warnings

import paramiko
import tenacity

from exec_helpers import api
from exec_helpers import constants
from exec_helpers import exceptions
from exec_helpers import exec_result
from exec_helpers import proc_enums
from exec_helpers import ssh_auth

from . import _helpers
from . import _log_templates
from . import _ssh_helpers

if typing.TYPE_CHECKING:
    import socket
    from collections.abc import Iterable
    from collections.abc import Sequence
    from types import TracebackType

    from typing_extensions import Self

    from exec_helpers.api import CalledProcessErrorSubClassT
    from exec_helpers.api import CommandT
    from exec_helpers.api import ErrorInfoT
    from exec_helpers.api import ExpectedExitCodesT
    from exec_helpers.api import LogMaskReT
    from exec_helpers.api import OptionalStdinT
    from exec_helpers.api import OptionalTimeoutT
    from exec_helpers.proc_enums import ExitCodeT

    from ._ssh_helpers import SSHConfigsDictT

__all__ = ("SSHClientBase", "SshExecuteAsyncResult", "SupportPathT")

KeepAlivePeriodT = typing.Union[int, bool]
SupportPathT = typing.Union[str, pathlib.PurePath]


class RetryOnExceptions(tenacity.retry_if_exception):
    """Advanced retry on exceptions.

    :param retry_on: Exceptions to retry on
    :type retry_on: type[BaseException] | tuple[type[BaseException], ...]
    :param reraise: Exceptions, which should be reraised, even if subclasses retry_on
    :type reraise: type[BaseException] | tuple[type[BaseException], ...]
    """

    def __init__(
        self,
        retry_on: type[BaseException] | tuple[type[BaseException], ...],
        reraise: type[BaseException] | tuple[type[BaseException], ...],
    ) -> None:
        """Retry on exceptions, except several types."""
        super().__init__(lambda e: isinstance(e, retry_on) and not isinstance(e, reraise))


# noinspection PyTypeHints
class SshExecuteAsyncResult(api.ExecuteAsyncResult):
    """Override original NamedTuple with proper typing."""

    __slots__ = ()

    @property
    def interface(self) -> paramiko.Channel:
        """Override original NamedTuple with proper typing.

        :return: Control interface.
        :rtype: paramiko.Channel
        """
        return super().interface  # type: ignore[no-any-return]

    @property
    def stdin(self) -> paramiko.channel.ChannelStdinFile:
        """Override original NamedTuple with proper typing.

        :return: STDIN interface.
        :rtype: paramiko.ChannelFile
        """
        warnings.warn(
            "stdin access deprecated: FIFO is often closed on execution and direct access is not expected.",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().stdin  # type: ignore[return-value]

    @property
    def stderr(self) -> paramiko.channel.ChannelStderrFile | None:
        """Override original NamedTuple with proper typing.

        :return: STDERR interface.
        :rtype: paramiko.ChannelFile | None
        """
        return super().stderr

    @property
    def stdout(self) -> paramiko.channel.ChannelFile | None:
        """Override original NamedTuple with proper typing.

        :return: STDOUT interface.
        :rtype: paramiko.ChannelFile | None
        """
        return super().stdout


class _SSHExecuteContext(api.ExecuteContext, typing.ContextManager[SshExecuteAsyncResult]):
    """SSH Execute context."""

    __slots__ = (
        "__auth",
        "__chan",
        "__get_pty",
        "__height",
        "__stderr_f",
        "__stdout_f",
        "__sudo_mode",
        "__timeout",
        "__transport",
        "__width",
    )

    def __init__(
        self,
        *,
        transport: paramiko.Transport,
        command: str,
        stdin: bytes | None = None,
        open_stdout: bool = True,
        open_stderr: bool = True,
        get_pty: bool = False,
        width: int = 80,
        height: int = 24,
        timeout: OptionalTimeoutT = None,
        sudo_mode: bool = False,
        auth: ssh_auth.SSHAuth,
        logger: logging.Logger,
        **kwargs: typing.Any,
    ) -> None:
        """Execute async context manager.

        :param transport: Executor instance (low level).
        :type transport: paramiko.Transport
        :param command: Command for execution (fully formatted).
        :type command: str
        :param stdin: Pass STDIN text to the process (fully formatted).
        :type stdin: bytes
        :param open_stdout: Open STDOUT stream for read.
        :type open_stdout: bool
        :param open_stderr: Open STDERR stream for read.
        :type open_stderr: bool
        :param get_pty: Get PTY for connection.
        :type get_pty: bool
        :param width: PTY width.
        :type width: int
        :param height: PTY height.
        :type height: int
        :param timeout: Timeout for connection (will be set on channel).
        :type timeout: int | float | None
        :param sudo_mode: Use sudo for command execution.
        :type sudo_mode: bool
        :param logger: Instance logger.
        :type logger: logging.Logger
        :param kwargs: Additional parameters for call.
        :type kwargs: typing.Any
        """
        super().__init__(
            command=command,
            stdin=stdin,
            open_stdout=open_stdout,
            open_stderr=open_stderr,
            logger=logger,
            **kwargs,
        )
        self.__transport = transport
        self.__get_pty = get_pty
        self.__width = width
        self.__height = height
        self.__timeout = timeout
        self.__sudo_mode = sudo_mode
        self.__auth = auth
        self.__chan: paramiko.Channel | None = None
        self.__stdout_f: paramiko.channel.ChannelFile | None = None
        self.__stderr_f: paramiko.channel.ChannelFile | None = None

    def __repr__(self) -> str:
        """Debug string.

        :return: reproduce for debug
        :rtype: str
        """
        return (
            f"<SSHClient().open_execute_context("
            f"command={self.command!r}, "
            f"stdin={self.stdin!r}, "
            f"open_stdout={self.open_stdout!r}, "
            f"open_stderr={self.open_stderr!r}, "
            f"get_pty={self.__get_pty!r}, "
            f"width={self.__width!r}, "
            f"height={self.__height!r}, "
            f"timeout={self.__timeout!r}, "
            f"sudo_mode={self.__sudo_mode!r}, "
            f"auth={self.__auth!r}, "
            f"transport={self.__transport!r}, "
            f"logger={self.logger!r}) "
            f"at {id(self)}>"
        )

    @property
    def get_pty(self) -> bool:
        """Get PTY for connection.

        :return: PTY should be opened.
        :rtype: bool
        """
        return self.__get_pty

    @property
    def width(self) -> int:
        """PTY width.

        :return: Width in symbols.
        :rtype: int
        """
        return self.__width

    @property
    def height(self) -> int:
        """PTY height.

        :return: Height in symbols.
        :rtype: int
        """
        return self.__height

    @property
    def timeout(self) -> OptionalTimeoutT:
        """Timeout for connection (will be set on a channel).

        :return: Connection timeout.
        :rtype: int | float | None
        """
        return self.__timeout

    @property
    def sudo_mode(self) -> bool:
        """Use sudo for command execution.

        :return: Require sudo.
        :rtype: bool
        """
        return self.__sudo_mode

    def __enter__(self) -> SshExecuteAsyncResult:
        """Context manager enter.

        :return: Raw execution information.
        :rtype: SshExecuteAsyncResult

        The Command is executed only in a context manager to be sure that everything will be cleaned up properly.
        """
        self.__chan = self.__transport.open_session()
        chan: paramiko.Channel = self.__chan.__enter__()
        if self.__timeout is not None:
            chan.settimeout(self.__timeout)

        if self.__get_pty:
            # Open PTY
            chan.get_pty(term="vt100", width=self.__width, height=self.__height, width_pixels=0, height_pixels=0)

        self.__stdout_f = chan.makefile("rb")
        stdout: paramiko.channel.ChannelFile = self.__stdout_f.__enter__()
        if self.open_stderr:
            self.__stderr_f = chan.makefile_stderr("rb")
            stderr: paramiko.channel.ChannelFile | None = self.__stderr_f.__enter__()
        else:
            stderr = None
        _stdin: paramiko.channel.ChannelFile
        with chan.makefile("wb") as _stdin:
            started = datetime.datetime.now(tz=datetime.timezone.utc)
            if self.__sudo_mode:
                chan.exec_command(self.command)  # nosec  # Sanitize on caller side
                if not stdout.channel.closed:
                    # noinspection PyTypeChecker
                    self.__auth.enter_password(_stdin)  # type: ignore[arg-type]
                    _stdin.flush()
            else:
                chan.exec_command(self.command)  # nosec  # Sanitize on caller side

            if self.stdin is not None:
                if not _stdin.channel.closed:
                    _stdin.write(self.stdin)
                    _stdin.flush()
                else:
                    self.logger.warning("STDIN Send failed: closed channel")

        if self.open_stdout:
            res_stdout: paramiko.channel.ChannelFile | None = stdout
        else:
            self.__stdout_f.__exit__(None, None, None)
            self.__stdout_f = None
            res_stdout = None

        # noinspection PyArgumentList
        return SshExecuteAsyncResult(
            interface=chan,
            stdin=_stdin,
            stderr=stderr,
            stdout=res_stdout,
            started=started,
        )

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.__stdout_f is not None:
            self.__stdout_f.__exit__(exc_type, exc_val, exc_tb)
            self.__stdout_f = None
        if self.__stderr_f is not None:
            self.__stderr_f.__exit__(exc_type, exc_val, exc_tb)
            self.__stderr_f = None
        if self.__chan is not None:
            self.__chan.__exit__(exc_type, exc_val, exc_tb)
            self.__chan = None


class _SudoContext(typing.ContextManager[None]):
    """Context manager for call commands with sudo.

    :param ssh: Connection instance.
    :type ssh: SSHClientBase
    :param enforce: Sudo mode for context manager.
    :type enforce: bool | None
    """

    __slots__ = ("__enforce", "__ssh", "__sudo_status")

    def __init__(self, ssh: SSHClientBase, enforce: bool | None = None) -> None:
        """Context manager for call commands with sudo."""
        self.__ssh: SSHClientBase = ssh
        self.__sudo_status: bool = ssh.sudo_mode
        self.__enforce: bool | None = enforce

    def __enter__(self) -> None:
        self.__sudo_status = self.__ssh.sudo_mode
        if self.__enforce is not None:
            self.__ssh.sudo_mode = self.__enforce

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.__ssh.sudo_mode = self.__sudo_status


class _KeepAliveContext(typing.ContextManager[None]):
    """Context manager for keepalive management.

    :param ssh: Connection instance.
    :type ssh: SSHClientBase
    :param enforce: Keepalive period for context manager.
    :type enforce: int
    """

    __slots__ = ("__enforce", "__keepalive_mode", "__keepalive_period", "__ssh")

    def __init__(self, ssh: SSHClientBase, enforce: int) -> None:
        """Context manager for keepalive management."""
        self.__ssh: SSHClientBase = ssh
        self.__keepalive_mode: bool = ssh.keepalive_mode
        self.__keepalive_period: int = ssh.keepalive_period
        self.__enforce: int = enforce

    def __enter__(self) -> None:
        self.__ssh.__enter__()
        self.__keepalive_mode = self.__ssh.keepalive_mode
        self.__keepalive_period = self.__ssh.keepalive_period
        self.__ssh.keepalive_mode = bool(self.__enforce)
        self.__ssh.keepalive_period = self.__enforce

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        # Exit before releasing!
        self.__ssh.__exit__(exc_type, exc_val, exc_tb)
        self.__ssh.keepalive_mode = self.__keepalive_mode
        self.__ssh.keepalive_period = self.__keepalive_period


class SSHClientBase(api.ExecHelper):
    """SSH Client helper.

    :param host: Remote hostname.
    :type host: str
    :param port: Remote ssh port.
    :type port: int | None
    :param username: Remote username.
    :type username: str | None
    :param password: Remote password.
    :type password: str | None
    :param auth: Credentials for connection.
    :type auth: ssh_auth.SSHAuth | None
    :param verbose: Show additional error/warning messages.
    :type verbose: bool
    :param ssh_config: SSH configuration for connection. Maybe config path, parsed as dict and paramiko parsed.
    :type ssh_config:
        str
        | paramiko.SSHConfig
        | dict[str, dict[str, str | int | bool | list[str]]]
        | HostsSSHConfigs
        | None
    :param ssh_auth_map: SSH authentication information mapped to host names. Useful for complex SSH Proxy cases.
    :type ssh_auth_map: dict[str, ssh_auth.SSHAuth] | ssh_auth.SSHAuthMapping | None
    :param sock: Socket for connection. Useful for ssh proxies support.
    :type sock: paramiko.ProxyCommand | paramiko.Channel | socket.socket | None
    :param keepalive: Keepalive period.
    :type keepalive: int | bool
    :param allow_ssh_agent: Use SSH Agent if available.
    :type allow_ssh_agent: bool

    .. note:: auth has priority over username/password/private_keys.
    .. note::

        for proxy connection auth information is collected from SSHConfig
        if ssh_auth_map record is not available.

    .. versionchanged:: 6.0.0 private_keys, auth and verbose became keyword-only arguments.
    .. versionchanged:: 6.0.0 Added optional ssh_config for ssh-proxy & low-level connection parameters handling.
    .. versionchanged:: 6.0.0 Added optional ssh_auth_map for ssh proxy cases with authentication on each step.
    .. versionchanged:: 6.0.0 Added optional sock for manual proxy chain handling.
    .. versionchanged:: 6.0.0 keepalive exposed to constructor.
    .. versionchanged:: 6.0.0 keepalive became int, now used in ssh transport as a period of keepalive requests.
    .. versionchanged:: 6.0.0 private_keys is deprecated.
    .. versionchanged:: 7.0.0 private_keys is removed.
    .. versionchanged:: 7.0.0 keepalive_mode is removed.
    .. versionchanged:: 7.4.0 Return of keepalive_mode to prevent mix with a keepalive period. Default is `False`.
    .. versionchanged:: 8.0.0 Expose SSH Agent usage override.
    """

    __slots__ = (
        "__allow_agent",
        "__auth_mapping",
        "__conn_chain",
        "__hostname",
        "__keepalive_mode",
        "__keepalive_period",
        "__port",
        "__sftp",
        "__sock",
        "__ssh",
        "__ssh_config",
        "__sudo_mode",
        "__verbose",
    )

    def __hash__(self) -> int:
        """Hash for usage as dict keys.

        :return: Hash describing the current connection.
        :rtype: int
        """
        return hash((self.__class__, self.hostname, self.port, self.auth))

    def __init__(
        self,
        host: str,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        *,
        auth: ssh_auth.SSHAuth | None = None,
        verbose: bool = True,
        ssh_config: str | paramiko.SSHConfig | SSHConfigsDictT | _ssh_helpers.HostsSSHConfigs | None = None,
        ssh_auth_map: dict[str, ssh_auth.SSHAuth] | ssh_auth.SSHAuthMapping | None = None,
        sock: paramiko.ProxyCommand | paramiko.Channel | socket.socket | None = None,
        keepalive: KeepAlivePeriodT = 1,
        allow_ssh_agent: bool = True,
    ) -> None:
        """Main SSH Client helper."""
        self.__sudo_mode = False
        self.__keepalive_period: int = int(keepalive)
        self.__keepalive_mode = False
        self.__verbose: bool = verbose
        self.__sock = sock

        self.__ssh: paramiko.SSHClient
        self.__sftp: paramiko.SFTPClient | None = None
        self.__allow_agent = allow_ssh_agent

        # Init ssh config. It's the main source for connection parameters
        if isinstance(ssh_config, _ssh_helpers.HostsSSHConfigs):
            self.__ssh_config: _ssh_helpers.HostsSSHConfigs = ssh_config
        else:
            self.__ssh_config = _ssh_helpers.parse_ssh_config(ssh_config, host)

        # Get config.
        # We are not resolving a full chain.
        # If you are having a chain for some reason - init config manually.
        config: _ssh_helpers.SSHConfig = self.__ssh_config[host]

        # Save resolved hostname and port
        self.__hostname: str = config.hostname
        if port is not None:
            self.__port: int = port
        else:
            self.__port = config.port if config.port is not None else 22

        # Store initial auth mapping
        self.__auth_mapping = ssh_auth.SSHAuthMapping(ssh_auth_map)
        # We are already resolved hostname
        if self.hostname not in self.__auth_mapping and host in self.__auth_mapping:
            self.__auth_mapping[self.hostname] = self.__auth_mapping[host]

        # Rebuild SSHAuth object if required.
        # Priority: auth > credentials > auth mapping
        real_auth = self.__handle_explicit_auth(
            username=username,
            config_username=config.user,
            password=password,
            auth=auth,
            key_filename=config.identityfile,
        )

        # Init super with host and real port and username
        mod_name = "exec_helpers" if self.__module__.startswith("exec_helpers") else self.__module__
        log_username: str = real_auth.username if real_auth.username is not None else getpass.getuser()

        super().__init__(
            logger=logging.getLogger(
                f"{mod_name}.{self.__class__.__name__}",
            ).getChild(
                f"({log_username}@{host}:{self.port})",
            )
        )

        # Update config for target host: merge with data from credentials and parameters.
        # SSHConfig is the single source for hostname/port/... during low-level connection construction.
        self.__rebuild_ssh_config()

        # Build a connection chain once and use it for connection later
        if sock is None:
            self.__conn_chain: list[tuple[_ssh_helpers.SSHConfig, ssh_auth.SSHAuth]] = self.__build_connection_chain()
        else:
            self.__conn_chain = []

        self.__connect()

    def __handle_explicit_auth(
        self,
        *,
        username: str | None,
        config_username: str | None,
        password: str | None,
        auth: ssh_auth.SSHAuth | None,
        key_filename: Iterable[str] | None,
    ) -> ssh_auth.SSHAuth:
        if auth is not None:
            self.__auth_mapping[self.hostname] = auth
        elif self.hostname not in self.__auth_mapping or any((username, password)):
            self.__auth_mapping[self.hostname] = ssh_auth.SSHAuth(
                username=username if username is not None else config_username,
                password=password,
                key_filename=key_filename,
            )

        return self.__auth_mapping[self.hostname]

    def __rebuild_ssh_config(self) -> None:
        """Rebuild the main ssh config from available information."""
        self.__ssh_config[self.hostname] = self.__ssh_config[self.hostname].overridden_by(
            _ssh_helpers.SSHConfig(
                hostname=self.hostname,
                port=self.port,
                user=self.auth.username,
                identityfile=self.auth.key_filename,
            )
        )

    def __build_connection_chain(self) -> list[tuple[_ssh_helpers.SSHConfig, ssh_auth.SSHAuth]]:
        """Build the ssh connection chain to reach destination host.

        :return: List of SSHConfig - SSHAuth pairs in order of connection
        :rtype: list[tuple[SSHConfig, ssh_auth.SSHAuth]]
        """
        conn_chain: list[tuple[_ssh_helpers.SSHConfig, ssh_auth.SSHAuth]] = []

        config = self.ssh_config[self.hostname]
        default_auth = ssh_auth.SSHAuth(username=config.user, key_filename=config.identityfile)
        auth = self.__auth_mapping.get_with_alt_hostname(
            config.hostname,
            self.hostname,
            default=default_auth,
        )
        conn_chain.append((config, auth))

        while config.proxyjump is not None:
            config = self.ssh_config[config.proxyjump]
            default_auth = ssh_auth.SSHAuth(username=config.user, key_filename=config.identityfile)
            conn_chain.append((config, self.__auth_mapping.get(config.hostname, default_auth)))
        return conn_chain[::-1]

    @property
    def auth(self) -> ssh_auth.SSHAuth:
        """Internal authorization object.

        Attention: this public property is mainly for inheritance,
        debug and information purposes.
        Calls outside SSHClient and child classes is a sign of incorrect design.
        Change is completely disallowed.

        :return: SSH authorization object for current connection.
        :rtype: ssh_auth.SSHAuth
        """
        return self.__auth_mapping[self.hostname]

    @property
    def allow_ssh_agent(self) -> bool:
        """Use SSH Agent if available.

        :return: SSH Agent usage allowed.
        :rtype: bool
        """
        return self.__allow_agent

    @property
    def hostname(self) -> str:
        """Connected remote host name.

        :return: Remote hostname.
        :rtype: str
        """
        return self.__hostname

    @property
    def port(self) -> int:
        """Connected remote port number.

        :return: Remote port.
        :rtype: int
        """
        return self.__port

    @property
    def ssh_config(self) -> _ssh_helpers.HostsSSHConfigs:
        """SSH connection config.

        :return: SSH config for connection.
        :rtype: HostsSSHConfigs
        """
        return copy.deepcopy(self.__ssh_config)

    @property
    def _ssh_transport(self) -> paramiko.Transport:
        """Paramiko transport object getter.

        :return: Paramiko transport.
        :rtype: paramiko.Transport
        :raises ConnectionError: Cannot get SSH transport (with reconnect).
        Used internally.
        """
        with self.lock:
            transport = self.__ssh.get_transport()
            if transport is not None:  # pylint: disable=consider-using-assignment-expr
                return transport

            self.reconnect()
            transport = self.__ssh.get_transport()
            if transport is not None:  # pylint: disable=consider-using-assignment-expr
                return transport
            raise ConnectionError("Can not get SSH transport (with reconnect)")

    @property
    def is_alive(self) -> bool:
        """Paramiko status: ready to use|reconnect required.

        :return: Paramiko transport is available
        :rtype: bool
        """
        return self.__ssh.get_transport() is not None

    def __repr__(self) -> str:
        """Representation for debug purposes.

        :return: Brief connection information for debug purposes.
        :rtype: str
        """
        return f"{self.__class__.__name__}(host={self.hostname}, port={self.port}, auth={self.auth!r})"

    def __str__(self) -> str:  # pragma: no cover
        """Representation for debug purposes.

        :return: Short string with connection information.
        :rtype: str
        """
        return f"{self.__class__.__name__}(host={self.hostname}, port={self.port}) for user {self.auth.username}"

    @property
    def _ssh(self) -> paramiko.SSHClient:
        """Ssh client object getter for inheritance support only.

        Attention: ssh client object creation and change are allowed only by __init__ and reconnect call.

        :rtype: paramiko.SSHClient
        """
        return self.__ssh

    @tenacity.retry(
        retry=RetryOnExceptions(retry_on=paramiko.SSHException, reraise=paramiko.AuthenticationException),
        stop=tenacity.stop.stop_after_attempt(3),
        wait=tenacity.wait.wait_fixed(3),
        reraise=True,
    )
    def __connect(self) -> None:
        """Main method for connection open."""
        with self.lock:
            if self.__sock is not None:
                self.__ssh = paramiko.SSHClient()
                self.__ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
                self.auth.connect(
                    client=self.__ssh,
                    hostname=self.hostname,
                    port=self.port,
                    log=self.__verbose,
                    sock=self.__sock,
                    allow_ssh_agent=self.allow_ssh_agent,
                )
            else:
                self.__ssh = self.__get_client()

            transport: paramiko.Transport = self._ssh_transport
            transport.set_keepalive(1 if self.__keepalive_period else 0)  # send keepalive packets

    def __get_client(self) -> paramiko.SSHClient:
        """Connect using connection chain information.

        :return: Paramiko ssh connection object.
        :rtype: paramiko.SSHClient
        :raises ValueError: ProxyCommand found in a connection chain after the first host reached an.
        :raises RuntimeError: Unexpected state.
        :raises ConnectionError: Cannot get SSH transport.
        """

        last_ssh_client: paramiko.SSHClient = paramiko.SSHClient()
        last_ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())  # noqa: S507,RUF100

        config, auth = self.__conn_chain[0]

        auth.connect(
            last_ssh_client,
            hostname=config.hostname,
            port=config.port or 22,
            sock=paramiko.ProxyCommand(config.proxycommand) if config.proxycommand else None,
            allow_ssh_agent=self.allow_ssh_agent,
        )

        for config, auth in self.__conn_chain[1:]:  # start has another logic, so do it out of cycle
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())  # noqa: S507,RUF100

            if config.proxyjump:
                transport = last_ssh_client.get_transport()
                if transport is None:  # pylint: disable=consider-using-assignment-expr
                    raise ConnectionError("Can not get SSH transport")
                sock = transport.open_channel(
                    kind="direct-tcpip",
                    dest_addr=(config.hostname, config.port or 22),
                    src_addr=(config.proxyjump, 0),
                )
                auth.connect(
                    ssh,
                    hostname=config.hostname,
                    port=config.port or 22,
                    sock=sock,
                    allow_ssh_agent=self.allow_ssh_agent,
                )
                last_ssh_client = ssh
                continue

            if config.proxycommand:
                raise ValueError(f"ProxyCommand found in connection chain after first host reached!\n{config}")

            raise RuntimeError("Unexpected state: Final host by configuration, but requested host is not reached")
        return last_ssh_client

    def __connect_sftp(self) -> None:
        """SFTP connection opener."""
        with self.lock:
            try:
                self.__sftp = self.__ssh.open_sftp()
            except paramiko.SSHException:
                self.logger.warning("SFTP enable failed! SSH only is accessible.")

    @property
    def _sftp(self) -> paramiko.sftp_client.SFTPClient:
        """SFTP channel access for inheritance.

        :rtype: paramiko.sftp_client.SFTPClient
        :raises paramiko.SSHException: SFTP connection failed.
        """
        if self.__sftp is not None:
            return self.__sftp
        self.logger.debug("SFTP is not connected, try to connect...")
        self.__connect_sftp()
        if self.__sftp is not None:
            return self.__sftp
        raise paramiko.SSHException("SFTP connection failed")

    def close(self) -> None:
        """Close SSH and SFTP sessions."""
        with self.lock:
            # noinspection PyBroadException
            try:
                self.__ssh.close()
                self.__sftp = None
            except Exception:
                self.logger.exception("Could not close ssh connection")
                if self.__sftp is not None:
                    # noinspection PyBroadException
                    try:
                        self.__sftp.close()
                    except Exception:
                        self.logger.exception("Could not close sftp connection")

    def __del__(self) -> None:
        """Destructor helper: close channel and threads BEFORE closing others.

        Due to threading in paramiko, default destructor could generate asserts on close,
        so we're calling channel close before a closing main ssh object.
        """
        try:
            self.__ssh.close()
        except BaseException as e:  # pragma: no cover  # NOSONAR
            self.logger.debug(f"Exception in {self!s} destructor call: {e}")
        self.__sftp = None

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager.

        .. versionchanged:: 1.0.0 Disconnect enforced on close.
        .. versionchanged:: 1.1.0 Release lock on exit.
        .. versionchanged:: 1.2.1 Disconnect enforced on close only not in keepalive mode.
        """
        if self._context_count == 1 and not self.__keepalive_mode:
            self.close()
        super().__exit__(exc_type, exc_val, exc_tb)

    @property
    def sudo_mode(self) -> bool:
        """Persistent sudo mode for a connection object.

        :rtype: bool
        """
        return self.__sudo_mode

    @sudo_mode.setter
    def sudo_mode(self, mode: bool) -> None:
        """Persistent sudo mode change for connection object.

        :param mode: Sudo status: enabled | disabled.
        :type mode: bool
        """
        self.__sudo_mode = mode

    @property
    def keepalive_period(self) -> int:
        """Keepalive period for connection object.

        :rtype: int
        If 0 - close connection on exit from context manager.
        """
        return self.__keepalive_period

    @keepalive_period.setter
    def keepalive_period(self, period: KeepAlivePeriodT) -> None:
        """Keepalive period change for a connection object.

        :param period: Keepalive period change.
        :type period: int | bool
        If 0 - close connection on exit from context manager.
        """
        self.__keepalive_period = int(period)
        transport: paramiko.Transport = self._ssh_transport
        transport.set_keepalive(int(period))

    @property
    def keepalive_mode(self) -> bool:
        """Keepalive mode.

        :rtype: bool
        Do not close connection on __exit__ if set.
        """
        return self.__keepalive_mode

    @keepalive_mode.setter
    def keepalive_mode(self, mode: bool) -> None:
        """Keepalive mode.

        :param mode: New mode.
        :type mode: bool
        Do not close connection on __exit__ if set.
        """
        self.__keepalive_mode = mode

    @keepalive_mode.deleter
    def keepalive_mode(self) -> None:
        """Keepalive mode.

        Do not close connection on __exit__ if set.
        """
        self.keepalive_mode = False

    def reconnect(self) -> None:
        """Reconnect SSH session."""
        with self.lock:
            self.close()
            self.__connect()

    def sudo(self, enforce: bool | None = None) -> _SudoContext:
        """Call contextmanager for sudo mode change.

        :param enforce: Enforce sudo enabled or disabled. By default: None.
        :type enforce: bool | None
        :return: Context manager with selected sudo state inside.
        :rtype: typing.ContextManager[None]
        """
        return _SudoContext(ssh=self, enforce=enforce)

    def keepalive(self, enforce: KeepAlivePeriodT = 1) -> _KeepAliveContext:
        """Call contextmanager with keepalive period change.

        :param enforce: Enforce a keepalive period.
        :type enforce: int | bool
        :return: Context manager with selected keepalive state inside.
        :rtype: typing.ContextManager[None]

        .. Note:: Enter and exit ssh context manager is produced as well.
        .. versionadded:: 1.2.1
        """
        return _KeepAliveContext(ssh=self, enforce=int(enforce))

    def _prepare_command(self, cmd: str, chroot_path: str | None = None, chroot_exe: str | None = None) -> str:
        """Prepare command: cover chroot and other cases.

        :param cmd: Main command.
        :param chroot_path: Path to make chroot for execution.
        :param chroot_exe: chroot executable, default "chroot".
        :return: The final command includes chroot, if required.
        """
        chroot_exe = chroot_exe or "chroot"
        if not self.sudo_mode:
            return super()._prepare_command(cmd=cmd, chroot_path=chroot_path, chroot_exe=chroot_exe)
        quoted_command: str = shlex.quote(cmd)
        if chroot_path is self._chroot_path is None:
            return f'sudo -S sh -c {shlex.quote(f"eval {quoted_command}")}'
        if chroot_path is not None:
            target_path: str = shlex.quote(chroot_path)
        else:
            target_path = shlex.quote(self._chroot_path)  # type: ignore[arg-type]
        return f'{chroot_exe} {target_path} sudo sh -c {shlex.quote(f"eval {quoted_command}")}'

    def _exec_command(  # type: ignore[override]
        self,
        command: str,
        async_result: SshExecuteAsyncResult,
        timeout: OptionalTimeoutT,
        *,
        verbose: bool = False,
        log_mask_re: LogMaskReT = None,
        stdin: OptionalStdinT = None,
        log_stdout: bool = True,
        log_stderr: bool = True,
        **kwargs: typing.Any,
    ) -> exec_result.ExecResult:
        """Get exit status from channel with timeout.

        :param command: Executed command (for logs).
        :type command: str
        :param async_result: execute_async result.
        :type async_result: SshExecuteAsyncResult
        :param timeout: Timeout before stop execution with TimeoutError.
        :type timeout: int | float | None
        :param verbose: Produce log.info records for STDOUT/STDERR.
        :type verbose: bool
        :param log_mask_re: Regex lookup rule to mask command for logger.
                            All MATCHED groups will be replaced by '<*masked*>'.
        :type log_mask_re: str | re.Pattern[str] | None
        :param stdin: Pass STDIN text to the process.
        :type stdin: bytes | str | bytearray | None
        :param log_stdout: Log STDOUT during read.
        :type log_stdout: bool
        :param log_stderr: Log STDERR during read.
        :type log_stderr: bool
        :param kwargs: Additional parameters for call.
        :type kwargs: typing.Any
        :return: Execution result.
        :rtype: ExecResult
        :raises ExecHelperTimeoutError: Timeout exceeded.

        .. versionchanged:: 1.2.0 log_mask_re regex rule for masking cmd
        """

        def poll_streams() -> None:
            """Poll FIFO buffers if data available."""
            if async_result.stdout and async_result.interface.recv_ready():
                result.read_stdout(src=async_result.stdout, log=self.logger if log_stdout else None, verbose=verbose)
            if async_result.stderr and async_result.interface.recv_stderr_ready():
                result.read_stderr(src=async_result.stderr, log=self.logger if log_stderr else None, verbose=verbose)

        def poll_pipes() -> None:
            """Polling task for FIFO buffers."""
            while not async_result.interface.status_event.is_set():
                time.sleep(0.1)
                if async_result.stdout or async_result.stderr:
                    poll_streams()

            result.read_stdout(src=async_result.stdout, log=self.logger, verbose=verbose)
            result.read_stderr(src=async_result.stderr, log=self.logger, verbose=verbose)
            result.exit_code = async_result.interface.exit_status

        # channel.status_event.wait(timeout)
        cmd_for_log: str = self._mask_command(cmd=command, log_mask_re=log_mask_re)

        # Store command with hidden data
        result = exec_result.ExecResult(cmd=cmd_for_log, stdin=stdin, started=async_result.started)

        with concurrent.futures.ThreadPoolExecutor(thread_name_prefix="exec-helpers_ssh_poll_") as executor:
            future: concurrent.futures.Future[None] = executor.submit(poll_pipes)

            concurrent.futures.wait([future], timeout)

            # Process closed?
            if async_result.interface.status_event.is_set():
                async_result.interface.close()
                return result

            async_result.interface.close()
            async_result.interface.status_event.set()
            future.cancel()

            concurrent.futures.wait([future], 0.001)

        result.set_timestamp()

        wait_err_msg: str = _log_templates.CMD_WAIT_ERROR.format(result=result, timeout=timeout)
        self.logger.debug(wait_err_msg)
        raise exceptions.ExecHelperTimeoutError(result=result, timeout=timeout)  # type: ignore[arg-type]

    def open_execute_context(
        self,
        command: str,
        *,
        stdin: OptionalStdinT = None,
        open_stdout: bool = True,
        open_stderr: bool = True,
        chroot_path: str | None = None,
        chroot_exe: str | None = None,
        get_pty: bool = False,
        width: int = 80,
        height: int = 24,
        timeout: OptionalTimeoutT = None,
        **kwargs: typing.Any,
    ) -> _SSHExecuteContext:
        """Get execution context manager.

        :param command: Command for execution.
        :type command: str | Iterable[str]
        :param stdin: Pass STDIN text to the process.
        :type stdin: bytes | str | bytearray | None
        :param open_stdout: Open STDOUT stream for read.
        :type open_stdout: bool
        :param open_stderr: Open STDERR stream for read.
        :type open_stderr: bool
        :param chroot_path: chroot path override.
        :type chroot_path: str | None
        :param chroot_exe: chroot exe override.
        :type chroot_exe: str | None
        :param get_pty: Get PTY for connection.
        :type get_pty: bool
        :param width: PTY width.
        :type width: int
        :param height: PTY height.
        :type height: int
        :param timeout: Timeout for **connection open**.
        :type timeout: int | float | None
        :param kwargs: Additional parameters for call.
        :type kwargs: typing.Any
        :return: Execute context.
        :rtype: _SSHExecuteContext
        .. versionadded:: 8.0.0
        """
        return _SSHExecuteContext(
            transport=self._ssh_transport,
            command=f"{self._prepare_command(cmd=command, chroot_path=chroot_path, chroot_exe=chroot_exe)}\n",
            stdin=None if stdin is None else self._string_bytes_bytearray_as_bytes(stdin),
            open_stdout=open_stdout,
            open_stderr=open_stderr,
            get_pty=get_pty,
            width=width,
            height=height,
            timeout=timeout,
            sudo_mode=self.sudo_mode,
            auth=self.auth,
            logger=self.logger,
            **kwargs,
        )

    def execute(
        self,
        command: CommandT,
        verbose: bool = False,
        timeout: OptionalTimeoutT = constants.DEFAULT_TIMEOUT,
        *,
        log_mask_re: LogMaskReT = None,
        stdin: OptionalStdinT = None,
        open_stdout: bool = True,
        log_stdout: bool = True,
        open_stderr: bool = True,
        log_stderr: bool = True,
        chroot_path: str | None = None,
        chroot_exe: str | None = None,
        get_pty: bool = False,
        width: int = 80,
        height: int = 24,
        **kwargs: typing.Any,
    ) -> exec_result.ExecResult:
        """Execute command and wait for return code.

        :param command: Command for execution.
        :type command: str | Iterable[str]
        :param verbose: Produce log.info records for command call and output.
        :type verbose: bool
        :param timeout: Timeout for command execution.
        :type timeout: int | float | None
        :param log_mask_re: Regex lookup rule to mask command for logger.
                            All MATCHED groups will be replaced by '<*masked*>'.
        :type log_mask_re: str | re.Pattern[str] | None
        :param stdin: pass STDIN text to the process.
        :type stdin: bytes | str | bytearray | None
        :param open_stdout: Open STDOUT stream for read.
        :type open_stdout: bool
        :param log_stdout: Log STDOUT during read.
        :type log_stdout: bool
        :param open_stderr: Open STDERR stream for read.
        :type open_stderr: bool
        :param log_stderr: Log STDERR during read.
        :type log_stderr: bool
        :param chroot_path: chroot path override.
        :type chroot_path: str | None
        :param chroot_exe: chroot exe override.
        :type chroot_exe: str | None
        :param get_pty: Get PTY for connection.
        :type get_pty: bool
        :param width: PTY width.
        :type width: int
        :param height: PTY height.
        :type height: int
        :param kwargs: Additional parameters for call.
        :type kwargs: typing.Any
        :return: Execution result.
        :rtype: ExecResult
        :raises ExecHelperTimeoutError: Timeout exceeded.

        .. versionchanged:: 1.2.0 default timeout 1 hour.
        .. versionchanged:: 2.1.0 Allow parallel calls.
        .. versionchanged:: 7.0.0 Allow command as list of arguments. Command will be joined with components escaping.
        .. versionchanged:: 8.0.0 chroot path exposed.
        .. versionchanged:: 8.1.0 chroot exe added.
        """
        return super().execute(
            command=command,
            verbose=verbose,
            timeout=timeout,
            log_mask_re=log_mask_re,
            stdin=stdin,
            open_stdout=open_stdout,
            log_stdout=log_stdout,
            open_stderr=open_stderr,
            log_stderr=log_stderr,
            chroot_path=chroot_path,
            chroot_exe=chroot_exe,
            get_pty=get_pty,
            width=width,
            height=height,
            **kwargs,
        )

    def __call__(
        self,
        command: CommandT,
        verbose: bool = False,
        timeout: OptionalTimeoutT = constants.DEFAULT_TIMEOUT,
        *,
        log_mask_re: LogMaskReT = None,
        stdin: OptionalStdinT = None,
        open_stdout: bool = True,
        log_stdout: bool = True,
        open_stderr: bool = True,
        log_stderr: bool = True,
        chroot_path: str | None = None,
        chroot_exe: str | None = None,
        get_pty: bool = False,
        width: int = 80,
        height: int = 24,
        **kwargs: typing.Any,
    ) -> exec_result.ExecResult:
        """Execute command and wait for return code.

        :param command: Command for execution.
        :type command: str | Iterable[str]
        :param verbose: Produce log.info records for command call and output.
        :type verbose: bool
        :param timeout: Timeout for command execution.
        :type timeout: int | float | None
        :param log_mask_re: Regex lookup rule to mask command for logger.
                            All MATCHED groups will be replaced by '<*masked*>'.
        :type log_mask_re: str | re.Pattern[str] | None
        :param stdin: Pass STDIN text to the process.
        :type stdin: bytes | str | bytearray | None
        :param open_stdout: Open STDOUT stream for read.
        :type open_stdout: bool
        :param log_stdout: Log STDOUT during read.
        :type log_stdout: bool
        :param open_stderr: Open STDERR stream for read.
        :type open_stderr: bool
        :param log_stderr: Log STDERR during read.
        :type log_stderr: bool
        :param chroot_path: Chroot path override.
        :type chroot_path: str | None
        :param chroot_exe: Chroot exe override.
        :type chroot_exe: str | None
        :param get_pty: Get PTY for connection.
        :type get_pty: bool
        :param width: PTY width.
        :type width: int
        :param height: PTY height.
        :type height: int
        :param kwargs: Additional parameters for call.
        :type kwargs: typing.Any
        :return: Execution result.
        :rtype: ExecResult
        :raises ExecHelperTimeoutError: Timeout exceeded.

        .. versionchanged:: 1.2.0 Default timeout 1 hour.
        .. versionchanged:: 2.1.0 Allow parallel calls.
        """
        return super().__call__(
            command=command,
            verbose=verbose,
            timeout=timeout,
            log_mask_re=log_mask_re,
            stdin=stdin,
            open_stdout=open_stdout,
            log_stdout=log_stdout,
            open_stderr=open_stderr,
            log_stderr=log_stderr,
            get_pty=get_pty,
            width=width,
            height=height,
            **kwargs,
        )

    def check_call(
        self,
        command: CommandT,
        verbose: bool = False,
        timeout: OptionalTimeoutT = constants.DEFAULT_TIMEOUT,
        error_info: ErrorInfoT = None,
        expected: ExpectedExitCodesT = (proc_enums.EXPECTED,),
        raise_on_err: bool = True,
        *,
        log_mask_re: LogMaskReT = None,
        stdin: OptionalStdinT = None,
        open_stdout: bool = True,
        log_stdout: bool = True,
        open_stderr: bool = True,
        log_stderr: bool = True,
        get_pty: bool = False,
        width: int = 80,
        height: int = 24,
        exception_class: CalledProcessErrorSubClassT = exceptions.CalledProcessError,
        **kwargs: typing.Any,
    ) -> exec_result.ExecResult:
        """Execute command and check for return code.

        :param command: Command for execution.
        :type command: str | Iterable[str]
        :param verbose: Produce log.info records for command call and output.
        :type verbose: bool
        :param timeout: Timeout for command execution.
        :type timeout: int | float | None
        :param error_info: Text for error details, if fail happens.
        :type error_info: str | None
        :param expected: Expected return codes (0 by default).
        :type expected: Iterable[int | proc_enums.ExitCodes]
        :param raise_on_err: Raise exception on unexpected return code.
        :type raise_on_err: bool
        :param log_mask_re: Regex lookup rule to mask command for logger.
                            All MATCHED groups will be replaced by '<*masked*>'.
        :type log_mask_re: str | re.Pattern[str] | None
        :param stdin: pass STDIN text to the process.
        :type stdin: bytes | str | bytearray | None
        :param open_stdout: Open STDOUT stream for read.
        :type open_stdout: bool
        :param log_stdout: Log STDOUT during read.
        :type log_stdout: bool
        :param open_stderr: Open STDERR stream for read.
        :type open_stderr: bool
        :param log_stderr: Log STDERR during read.
        :type log_stderr: bool
        :param get_pty: Get PTY for connection.
        :type get_pty: bool
        :param width: PTY width.
        :type width: int
        :param height: PTY height.
        :type height: int
        :param exception_class: Exception class for errors. Subclass of CalledProcessError is mandatory.
        :type exception_class: type[exceptions.CalledProcessError]
        :param kwargs: Additional parameters for call.
        :type kwargs: typing.Any
        :return: Execution result.
        :rtype: ExecResult
        :raises ExecHelperTimeoutError: Timeout exceeded.
        :raises CalledProcessError: Unexpected exit code.

        .. versionchanged:: 1.2.0 Default timeout 1 hour.
        .. versionchanged:: 3.2.0 Exception class can be substituted.
        .. versionchanged:: 3.4.0 Expected is not optional, defaults os dependent.
        """
        return super().check_call(
            command=command,
            verbose=verbose,
            timeout=timeout,
            error_info=error_info,
            expected=expected,
            raise_on_err=raise_on_err,
            log_mask_re=log_mask_re,
            stdin=stdin,
            open_stdout=open_stdout,
            log_stdout=log_stdout,
            open_stderr=open_stderr,
            log_stderr=log_stderr,
            get_pty=get_pty,
            width=width,
            height=height,
            exception_class=exception_class,
            **kwargs,
        )

    def check_stderr(
        self,
        command: CommandT,
        verbose: bool = False,
        timeout: OptionalTimeoutT = constants.DEFAULT_TIMEOUT,
        error_info: ErrorInfoT = None,
        raise_on_err: bool = True,
        *,
        expected: ExpectedExitCodesT = (proc_enums.EXPECTED,),
        log_mask_re: LogMaskReT = None,
        stdin: OptionalStdinT = None,
        open_stdout: bool = True,
        log_stdout: bool = True,
        open_stderr: bool = True,
        log_stderr: bool = True,
        get_pty: bool = False,
        width: int = 80,
        height: int = 24,
        exception_class: CalledProcessErrorSubClassT = exceptions.CalledProcessError,
        **kwargs: typing.Any,
    ) -> exec_result.ExecResult:
        """Execute command expecting return code 0 and empty STDERR.

        :param command: Command for execution.
        :type command: str | Iterable[str]
        :param verbose: Produce log.info records for command call and output.
        :type verbose: bool
        :param timeout: Timeout for command execution.
        :type timeout: int | float | None
        :param error_info: Text for error details, if fail happens.
        :type error_info: str | None
        :param raise_on_err: Raise exception on unexpected return code.
        :type raise_on_err: bool
        :param expected: Expected return codes (0 by default).
        :type expected: Iterable[int | proc_enums.ExitCodes]
        :param log_mask_re: Regex lookup rule to mask command for logger.
                            All MATCHED groups will be replaced by '<*masked*>'.
        :type log_mask_re: str | re.Pattern[str] | None
        :param stdin: Pass STDIN text to the process.
        :type stdin: bytes | str | bytearray | None
        :param open_stdout: Open STDOUT stream for read.
        :type open_stdout: bool
        :param log_stdout: Log STDOUT during read.
        :type log_stdout: bool
        :param open_stderr: Open STDERR stream for read.
        :type open_stderr: bool
        :param log_stderr: Log STDERR during read.
        :type log_stderr: bool
        :param get_pty: Get PTY for connection.
        :type get_pty: bool
        :param width: PTY width.
        :type width: int
        :param height: PTY height.
        :type height: int
        :param exception_class: Exception class for errors. Subclass of CalledProcessError is mandatory.
        :type exception_class: type[exceptions.CalledProcessError]
        :param kwargs: Additional parameters for call.
        :type kwargs: typing.Any
        :return: Execution result.
        :rtype: ExecResult
        :raises ExecHelperTimeoutError: Timeout exceeded.
        :raises CalledProcessError: Unexpected exit code or stderr presents.

        .. versionchanged:: 1.2.0 Default timeout 1 hour.
        .. versionchanged:: 3.2.0 Exception class can be substituted.
        .. versionchanged:: 3.4.0 Expected is not optional, defaults os dependent.
        """
        return super().check_stderr(
            command=command,
            verbose=verbose,
            timeout=timeout,
            error_info=error_info,
            raise_on_err=raise_on_err,
            expected=expected,
            log_mask_re=log_mask_re,
            stdin=stdin,
            open_stdout=open_stdout,
            log_stdout=log_stdout,
            open_stderr=open_stderr,
            log_stderr=log_stderr,
            get_pty=get_pty,
            width=width,
            height=height,
            exception_class=exception_class,
            **kwargs,
        )

    def proxy_to(
        self,
        host: str,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        *,
        auth: ssh_auth.SSHAuth | None = None,
        verbose: bool = True,
        ssh_config: str | paramiko.SSHConfig | SSHConfigsDictT | _ssh_helpers.HostsSSHConfigs | None = None,
        ssh_auth_map: dict[str, ssh_auth.SSHAuth] | ssh_auth.SSHAuthMapping | None = None,
        keepalive: KeepAlivePeriodT = 1,
    ) -> Self:
        """Start new SSH connection using current as proxy.

        :param host: Remote hostname.
        :type host: str
        :param port: Remote ssh port.
        :type port: int | None
        :param username: Remote username.
        :type username: str | None
        :param password: Remote password
        :type password: str | None
        :param auth: Credentials for connection.
        :type auth: ssh_auth.SSHAuth | None
        :param verbose: Show additional error/warning messages.
        :type verbose: bool
        :param ssh_config: SSH configuration for connection. Maybe config path, parsed as dict and paramiko parsed.
        :type ssh_config:
            str
            | paramiko.SSHConfig
            | dict[str, dict[str, str | int | bool | List[str]]]
            | HostsSSHConfigs,
            | None
        :param ssh_auth_map: SSH authentication information mapped to host names. Useful for complex SSH Proxy cases.
        :type ssh_auth_map: dict[str, ssh_auth.SSHAuth] | ssh_auth.SSHAuthMapping | None
        :param keepalive: Keepalive period.
        :type keepalive: int | bool
        :return: New ssh client instance using current as a proxy.
        :rtype: SSHClientBase

        .. note:: auth has priority over username/password.

        .. versionadded:: 6.0.0
        """
        if isinstance(ssh_config, _ssh_helpers.HostsSSHConfigs):
            parsed_ssh_config: _ssh_helpers.HostsSSHConfigs = ssh_config
        else:
            parsed_ssh_config = _ssh_helpers.parse_ssh_config(ssh_config, host)

        host_config = parsed_ssh_config[host]

        if port is not None:
            dest_port: int = port
        elif host_config.port is not None:
            dest_port = host_config.port
        else:
            dest_port = 22

        sock: paramiko.Channel = self._ssh_transport.open_channel(
            kind="direct-tcpip",
            dest_addr=(host_config.hostname, dest_port),
            src_addr=(self.hostname, 0),
        )

        cls: type[Self] = self.__class__
        return cls(
            host=host,
            port=dest_port,
            username=username,
            password=password,
            auth=auth,
            verbose=verbose,
            ssh_config=ssh_config,
            sock=sock,
            ssh_auth_map=ssh_auth_map if ssh_auth_map is not None else self.__auth_mapping,
            keepalive=int(keepalive),
        )

    def execute_through_host(
        self,
        hostname: str,
        command: CommandT,
        *,
        auth: ssh_auth.SSHAuth | None = None,
        port: int | None = None,
        verbose: bool = False,
        timeout: OptionalTimeoutT = constants.DEFAULT_TIMEOUT,
        stdin: OptionalStdinT = None,
        open_stdout: bool = True,
        log_stdout: bool = True,
        open_stderr: bool = True,
        log_stderr: bool = True,
        log_mask_re: LogMaskReT = None,
        get_pty: bool = False,
        width: int = 80,
        height: int = 24,
    ) -> exec_result.ExecResult:
        """Execute command on remote host through currently connected host.

        :param hostname: Target hostname.
        :type hostname: str
        :param command: Command for execution.
        :type command: str | Iterable[str]
        :param auth: Credentials for target machine.
        :type auth: ssh_auth.SSHAuth | None
        :param port: Target port.
        :type port: int | None
        :param verbose: Produce log.info records for command call and output.
        :type verbose: bool
        :param timeout: Timeout for command execution.
        :type timeout: int | float | None
        :param stdin: Pass STDIN text to the process.
        :type stdin: bytes | str | bytearray | None
        :param open_stdout: Open STDOUT stream for read.
        :type open_stdout: bool
        :param log_stdout: Log STDOUT during read.
        :type log_stdout: bool
        :param open_stderr: Open STDERR stream for read.
        :type open_stderr: bool
        :param log_stderr: Log STDERR during read.
        :type log_stderr: bool
        :param log_mask_re: Regex lookup rule to mask command for logger.
                            All MATCHED groups will be replaced by '<*masked*>'.
        :type log_mask_re: str | re.Pattern[str] | None
        :param get_pty: Open PTY on target machine.
        :type get_pty: bool
        :param width: PTY width.
        :type width: int
        :param height: PTY height.
        :type height: int
        :return: Execution result.
        :rtype: ExecResult
        :raises ExecHelperTimeoutError: Timeout exceeded.

        .. versionchanged:: 1.2.0 Default timeout 1 hour.
        .. versionchanged:: 1.2.0 log_mask_re regex rule for masking cmd.
        .. versionchanged:: 3.2.0 Expose pty options as optional keyword-only arguments.
        .. versionchanged:: 4.0.0 Expose stdin and log_mask_re as optional keyword-only arguments.
        .. versionchanged:: 6.0.0 Move channel open to separate method and make proper ssh-proxy usage.
        .. versionchanged:: 6.0.0 Only hostname and command are positional argument, target_port changed to port.
        .. versionchanged:: 7.0.0 target_port argument removed.
        """
        conn: Self
        if auth is None:
            auth = self.auth

        with self.proxy_to(
            host=hostname,
            port=port,
            auth=auth,
            verbose=verbose,
            ssh_config=self.ssh_config,
            keepalive=False,
        ) as conn:
            return conn(
                command,
                timeout=timeout,
                stdin=stdin,
                open_stdout=open_stdout,
                log_stdout=log_stdout,
                open_stderr=open_stderr,
                log_stderr=log_stderr,
                log_mask_re=log_mask_re,
                get_pty=get_pty,
                width=width,
                height=height,
            )

    @classmethod
    def execute_together(
        cls,
        remotes: Iterable[SSHClientBase],
        command: CommandT,
        timeout: OptionalTimeoutT = constants.DEFAULT_TIMEOUT,
        expected: ExpectedExitCodesT = (proc_enums.EXPECTED,),
        raise_on_err: bool = True,
        *,
        stdin: OptionalStdinT = None,
        open_stdout: bool = True,
        open_stderr: bool = True,
        chroot_path: str | None = None,
        chroot_exe: str | None = None,
        verbose: bool = False,
        log_mask_re: LogMaskReT = None,
        exception_class: type[exceptions.ParallelCallProcessError] = exceptions.ParallelCallProcessError,
        **kwargs: typing.Any,
    ) -> dict[tuple[str, int], exec_result.ExecResult]:
        """Execute command on multiple remotes in async mode.

        :param remotes: Connections to execute on.
        :type remotes: Iterable[SSHClientBase]
        :param command: Command for execution.
        :type command: str | Iterable[str]
        :param timeout: Timeout for command execution.
        :type timeout: int | float | None
        :param expected: Expected return codes (0 by default).
        :type expected: Iterable[int | proc_enums.ExitCodes]
        :param raise_on_err: Raise exception on unexpected return code.
        :type raise_on_err: bool
        :param stdin: Pass STDIN text to the process.
        :type stdin: bytes | str | bytearray | None
        :param open_stdout: Open STDOUT stream for read.
        :type open_stdout: bool
        :param open_stderr: Open STDERR stream for read.
        :type open_stderr: bool
        :param chroot_path: chroot path override.
        :type chroot_path: str | None
        :param chroot_exe: chroot exe override.
        :type chroot_exe: str | None
        :param verbose: Produce verbose log record on command call.
        :type verbose: bool
        :param log_mask_re: Regex lookup rule to mask command for logger.
                            All MATCHED groups will be replaced by '<*masked*>'.
        :type log_mask_re: str | re.Pattern[str] | None
        :param exception_class: Exception to raise on error. Mandatory subclass of exceptions.ParallelCallProcessError.
        :type exception_class: type[exceptions.ParallelCallProcessError]
        :param kwargs: Additional parameters for execute_async call.
        :type kwargs: typing.Any
        :return: Dictionary {(hostname, port): result}.
        :rtype: dict[tuple[str, int], exec_result.ExecResult]
        :raises ParallelCallProcessError: Unexpected any code at lest on one target.
        :raises ParallelCallExceptionsError: At lest one exception raised during execution (including timeout).

        .. versionchanged:: 1.2.0 Default timeout 1 hour.
        .. versionchanged:: 1.2.0 log_mask_re regex rule for masking cmd.
        .. versionchanged:: 3.2.0 Exception class can be substituted.
        .. versionchanged:: 3.4.0 Expected is not optional, defaults os dependent.
        .. versionchanged:: 4.0.0 Expose stdin and log_mask_re as optional keyword-only arguments.
        """

        def get_result(remote: SSHClientBase) -> exec_result.ExecResult:
            """Get result from remote call.

            :param remote: SSH connection instance.
            :return: Execution result.
            :raises ExecHelperTimeoutError: Timeout exceeded.
            """
            # pylint: disable=protected-access
            cmd_for_log: str = remote._mask_command(cmd=cmd, log_mask_re=log_mask_re)
            remote._log_command_execute(
                command=cmd,
                log_mask_re=log_mask_re,
                log_level=log_level,
                chroot_path=chroot_path,
                chroot_exe=chroot_exe,
                **kwargs,
            )
            # pylint: enable=protected-access

            with remote.open_execute_context(
                cmd,
                stdin=stdin,
                open_stdout=open_stdout,
                open_stderr=open_stderr,
                chroot_path=chroot_path,
                chroot_exe=chroot_exe,
                timeout=timeout,
                **kwargs,
            ) as async_result:
                done = async_result.interface.status_event.wait(timeout)

                res = exec_result.ExecResult(cmd=cmd_for_log, stdin=stdin, started=async_result.started)
                res.read_stdout(src=async_result.stdout)
                res.read_stderr(src=async_result.stderr)
                if done:
                    res.exit_code = async_result.interface.recv_exit_status()
                    return res

            res.set_timestamp()

            wait_err_msg: str = _log_templates.CMD_WAIT_ERROR.format(result=res, timeout=timeout)
            remote.logger.debug(wait_err_msg)
            raise exceptions.ExecHelperTimeoutError(result=res, timeout=timeout)  # type: ignore[arg-type]

        prep_expected: Sequence[ExitCodeT] = proc_enums.exit_codes_to_enums(expected)
        log_level: int = logging.INFO if verbose else logging.DEBUG
        cmd = _helpers.cmd_to_string(command)

        results: dict[tuple[str, int], exec_result.ExecResult] = {}
        errors: dict[tuple[str, int], exec_result.ExecResult] = {}
        raised_exceptions: dict[tuple[str, int], Exception] = {}
        not_done: set[concurrent.futures.Future[exec_result.ExecResult]]

        with concurrent.futures.ThreadPoolExecutor(thread_name_prefix="exec-helpers_ssh_multiple_poll_") as executor:
            futures: dict[SSHClientBase, concurrent.futures.Future[exec_result.ExecResult]] = {
                remote: executor.submit(get_result, remote) for remote in set(remotes)
            }  # Use distinct remotes

            _done, not_done = concurrent.futures.wait(futures.values(), timeout=timeout)

            for fut in not_done:  # pragma: no cover
                fut.cancel()

        for remote, future in futures.items():
            try:
                result = future.result(timeout=0.1)
                results[remote.hostname, remote.port] = result
                if result.exit_code not in prep_expected:
                    errors[remote.hostname, remote.port] = result
            except Exception as e:  # noqa: PERF203
                raised_exceptions[remote.hostname, remote.port] = e

        if raised_exceptions:  # always raise
            raise exceptions.ParallelCallExceptionsError(
                command=cmd,
                exceptions=raised_exceptions,
                errors=errors,
                results=results,
                expected=prep_expected,
            )
        if errors and raise_on_err:
            raise exception_class(cmd, errors, results, expected=prep_expected)
        return results

    def open(self, path: SupportPathT, mode: str = "r") -> paramiko.SFTPFile:
        """Open file on remote using SFTP session.

        :param path: Filesystem object path.
        :type path: str | pathlib.PurePath
        :param mode: Open file mode ('t' is not supported).
        :type mode: str
        :return: file.open() stream.
        :rtype: paramiko.SFTPFile
        """
        return self._sftp.open(pathlib.PurePath(path).as_posix(), mode)  # pragma: no cover

    def exists(self, path: SupportPathT) -> bool:
        """Check for file existence using SFTP session.

        :param path: Filesystem object path.
        :type path: str | pathlib.PurePath
        :return: path is valid (an object exists).
        :rtype: bool
        """
        try:
            self._sftp.lstat(pathlib.PurePath(path).as_posix())
        except OSError:
            return False

        return True

    def stat(self, path: SupportPathT) -> paramiko.sftp_attr.SFTPAttributes:
        """Get stat info for path with following symlinks.

        :param path: Filesystem object path.
        :type path: str | pathlib.PurePath
        :return: stat like information for a remote path.
        :rtype: paramiko.sftp_attr.SFTPAttributes
        """
        return self._sftp.stat(pathlib.PurePath(path).as_posix())  # pragma: no cover

    def utime(self, path: SupportPathT, times: tuple[int, int] | None = None) -> None:
        """Set atime, mtime.

        :param path: Filesystem object path.
        :type path: str | pathlib.PurePath
        :param times: (atime, mtime).
        :type times: tuple[int, int] | None

        .. versionadded:: 1.0.0
        """
        self._sftp.utime(pathlib.PurePath(path).as_posix(), times)  # pragma: no cover

    def isfile(self, path: SupportPathT) -> bool:
        """Check, that path is file using SFTP session.

        :param path: Remote path to validate.
        :type path: str | pathlib.PurePath
        :return: path is file.
        :rtype: bool
        """
        try:
            attrs: paramiko.sftp_attr.SFTPAttributes = self._sftp.lstat(pathlib.PurePath(path).as_posix())
            if attrs.st_mode is None:
                return False
            return stat.S_ISREG(attrs.st_mode)
        except (TypeError, OSError):
            return False

    def isdir(self, path: SupportPathT) -> bool:
        """Check, that path is directory using SFTP session.

        :param path: Remote path to validate.
        :type path: str | pathlib.PurePath
        :return: path is directory.
        :rtype: bool
        """
        try:
            attrs: paramiko.sftp_attr.SFTPAttributes = self._sftp.lstat(pathlib.PurePath(path).as_posix())
            if attrs.st_mode is None:
                return False
            return stat.S_ISDIR(attrs.st_mode)
        except (TypeError, OSError):
            return False

    def islink(self, path: SupportPathT) -> bool:
        """Check, that path is symlink using SFTP session.

        :param path: Remote path to validate.
        :type path: str | pathlib.PurePath
        :return: path is symlink.
        :rtype: bool
        """
        try:
            attrs: paramiko.sftp_attr.SFTPAttributes = self._sftp.lstat(pathlib.PurePath(path).as_posix())
            if attrs.st_mode is None:
                return False
            return stat.S_ISLNK(attrs.st_mode)
        except (TypeError, OSError):
            return False

    def symlink(self, source: SupportPathT, dest: SupportPathT) -> None:
        """Produce a symbolic link like `os.symlink`.

        :param source: Source path.
        :type source: str | pathlib.PurePath
        :param dest: Destination path.
        :type dest: str | pathlib.PurePath
        """
        self._sftp.symlink(pathlib.PurePath(source).as_posix(), pathlib.PurePath(dest).as_posix())  # pragma: no cover

    def chmod(self, path: SupportPathT, mode: int) -> None:
        """Change the mode (permissions) of a file like `os.chmod`.

        :param path: Filesystem object path.
        :type path: str | pathlib.PurePath
        :param mode: New permissions.
        :type mode: int
        """
        self._sftp.chmod(pathlib.PurePath(path).as_posix(), mode)  # pragma: no cover

    def chown(self, path: SupportPathT, uid: int, gid: int) -> None:
        """Change ownership for remote file.

        :param path: Filesystem object path.
        :type path: str | pathlib.PurePath
        :param uid: User identifier.
        :type uid: int
        :param gid: Group identifier.
        :type gid: int
        """
        self._sftp.chown(path=pathlib.PurePath(path).as_posix(), uid=uid, gid=gid)  # pragma: no cover

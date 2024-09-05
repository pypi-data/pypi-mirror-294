#    Copyright 2018 - 2023 Aleksei Stepanov aka penguinolog.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at

#         http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Execution helpers for simplified usage of subprocess and ssh."""

from __future__ import annotations

import importlib
import typing
import warnings

try:  # noqa: FURB107,SIM105,RUF100
    from ._version import version as __version__  # noqa: F401
except ImportError:
    pass

if typing.TYPE_CHECKING:
    from collections.abc import Sequence


# noinspection PyUnresolvedReferences
__all__ = (
    # pylint: disable=undefined-all-variable
    "CalledProcessError",
    "ExecCalledProcessError",
    "ExecHelper",
    "ExecHelperError",
    "ExecHelperNoKillError",
    "ExecHelperTimeoutError",
    "ExecResult",
    "ExitCodes",
    "HostsSSHConfigs",
    "ParallelCallExceptionsError",
    "ParallelCallProcessError",
    "SSHAuth",
    "SSHClient",
    "SSHConfig",
    "Subprocess",
    "async_api",
    "exceptions",
    "mask_command",
)

__locals: dict[str, typing.Any] = locals()  # use mutable access for pure lazy loading

__lazy_load_modules: Sequence[str] = (
    "async_api",
    "exceptions",
    "exec_result",
)

__lazy_load_parent_modules: dict[str, str] = {
    "HostsSSHConfigs": "_ssh_helpers",
    "SSHConfig": "_ssh_helpers",
    "SSHClient": "ssh",
    "SSHAuth": "ssh_auth",
    "Subprocess": "subprocess",
    # API
    "ExitCodes": "proc_enums",
    "ExecResult": "exec_result",
    "ExecHelper": "api",
    "mask_command": "_helpers",
    # Exceptions
    "ExecHelperError": "exceptions",
    "ExecCalledProcessError": "exceptions",
    "CalledProcessError": "exceptions",
    "ParallelCallExceptionsError": "exceptions",
    "ParallelCallProcessError": "exceptions",
    "ExecHelperNoKillError": "exceptions",
    "ExecHelperTimeoutError": "exceptions",
}

_deprecated: dict[str, str] = {}


def __getattr__(name: str) -> typing.Any:
    """Get attributes lazy.

    :return: Attribute by name.
    :raises AttributeError: Attribute is not defined for the lazy load.
    """
    if name in _deprecated:
        warnings.warn(
            f"{name} is deprecated in favor of {_deprecated[name]}",
            DeprecationWarning,
            stacklevel=2,
        )
    if name in __lazy_load_modules:
        mod = importlib.import_module(f"{__package__}.{name}")
        __locals[name] = mod
        return mod
    if name in __lazy_load_parent_modules:
        mod = importlib.import_module(f"{__package__}.{__lazy_load_parent_modules[name]}")
        obj = getattr(mod, name)
        __locals[name] = obj
        return obj
    raise AttributeError(f"{name} not found in {__package__}")


__author__ = "Aleksei Stepanov"
__author_email__ = "penguinolog@gmail.com"
__maintainers__ = {
    "Aleksei Stepanov": "penguinolog@gmail.com",
    "Antonio Esposito": "esposito.cloud@gmail.com",
    "Dennis Dmitriev": "dis-xcom@gmail.com",
}
__url__ = "https://github.com/python-useful-helpers/exec-helpers"
__description__ = "Execution helpers for simplified usage of subprocess and ssh."
__license__ = "Apache License, Version 2.0"

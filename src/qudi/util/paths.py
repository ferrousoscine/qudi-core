"""
Copyright (c) 2021, the qudi developers. See the AUTHORS.md file at the top-level directory of this
distribution and on <https://github.com/Ulm-IQO/qudi-core/>

This file is part of qudi.

Qudi is free software: you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Qudi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with qudi.
If not, see <https://www.gnu.org/licenses/>.
"""

__all__ = [
    "get_appdata_dir",
    "get_artwork_dir",
    "get_daily_directory",
    "get_default_config_dir",
    "get_default_data_dir",
    "get_default_log_dir",
    "get_home_dir",
    "get_main_dir",
    "get_module_app_data_path",
    "get_userdata_dir",
]

import datetime
import os
import sys
from pathlib import Path


def get_main_dir() -> str:
    """
    Returns the absolute path to the directory of the main software.

    Returns
    -------
    str
        Path to the main tree of the software.
    """
    from qudi import core  # noqa: PLC0415

    return str((Path(core.__file__).parent / "..").resolve())


def get_artwork_dir() -> str:
    """
    Returns the absolute path to the Qudi artwork directory.

    Returns
    -------
    str
        Path to the artwork directory of Qudi.
    """
    return str(Path(get_main_dir()) / "artwork")


def get_home_dir() -> str:
    """
    Returns the absolute path to the home directory.

    Returns
    -------
    str
        Absolute path to the home directory.
    """
    return str(Path.home().resolve())


def get_userdata_dir(create_missing: bool | None = False) -> str:
    """
    Returns the absolute path to the Qudi subfolder in the user home directory.
    This path should be used for exposed user data like config files, etc.

    Returns
    -------
    str
        Absolute path to the Qudi subfolder in the user home directory.
    """
    path = Path(get_home_dir()) / "qudi"
    if create_missing and not path.exists():
        path.mkdir()
    return str(path)


def get_appdata_dir(create_missing: bool | None = False) -> str:
    """
    Get the system-specific application data directory.

    Returns
    -------
    str
        Path to the application data directory specific to the system.
    """
    if sys.platform == "win32":
        path = Path(os.environ["APPDATA"]) / "qudi"
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Preferences" / "qudi"
    else:
        path = Path.home() / ".local" / "qudi"

    if create_missing and not path.exists():
        path.mkdir(parents=True)
    return str(path)


def get_default_config_dir(create_missing: bool | None = False) -> str:
    """
    Get the system-specific application data directory.

    Returns
    -------
    str
        Path to the application data directory specific to the system.

    """
    path = Path(get_userdata_dir(create_missing)) / "config"
    if create_missing and not path.exists():
        path.mkdir()
    return str(path)


def get_default_log_dir(create_missing: bool | None = False) -> str:
    """
    Get the system-specific application log directory.

    Returns
    -------
    str
        Path to the default logging directory specific to the system.

    """
    path = Path(get_userdata_dir(create_missing)) / "log"
    if create_missing and not path.exists():
        path.mkdir()
    return str(path)


def get_default_data_dir(create_missing: bool | None = False) -> str:
    """Get the system specific application fallback data root directory.
    Does NOT consider qudi configuration.

    Returns
    -------
    str
        Path to default data root directory.
    """
    path = Path(get_userdata_dir(create_missing)) / "Data"
    if create_missing and not path.exists():
        path.mkdir()
    return str(path)


def get_daily_directory(
    timestamp: datetime.datetime | None = None, root: str | None = None, create_missing: bool | None = False
) -> str:
    """
    Returns a path tree according to the timestamp given.

    The directory structure will have the form: root/<YYYY>/<MM>/<YYYY-MM-DD>
    If no root directory is given, this method will return just the relative path stub:
    <YYYY>/<MM>/<YYYY-MM-DD>

    Parameters
    ----------
    timestamp : datetime.datetime, optional
        Timestamp for which to create the daily directory. Defaults to current timestamp if not provided.
    root : str, optional
        Root path for the daily directory structure. If not provided, only the relative path stub is returned.
    create_missing : bool, optional
        Indicates if the directory should be created (True) or not (False). Only considered if root is given.

    Returns
    -------
    str
        Path representing the directory structure based on the timestamp.
    """
    if timestamp is None:
        timestamp = datetime.datetime.now(tz=datetime.UTC)

    day_dir = timestamp.strftime("%Y-%m-%d")
    year_dir, month_dir = day_dir.split("-")[:2]
    daily_path = Path(year_dir) / month_dir / day_dir
    if root is not None:
        daily_path = Path(root) / daily_path
        if create_missing:
            daily_path.mkdir(parents=True, exist_ok=True)
    return str(daily_path)


def get_module_app_data_path(cls_name: str, module_base: str, module_name: str) -> str:
    """Constructs the appData file path for the given qudi module."""
    file_name = f"status-{cls_name}_{module_base}_{module_name}.cfg"
    return str(Path(get_appdata_dir()) / file_name)

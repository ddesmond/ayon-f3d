import os
import time
import platform

import ayon_api

from .version import __version__
from .constants import ADDON_NAME


def get_f3d_icon_url(server_url=None):
    """Get URL to f3d icon.

    Args:
        server_url (Optional[str]): AYON server URL.

    Returns:
        str: URL where f3d icon is located.
    """

    server_url = server_url or ayon_api.get_base_url()
    return "{}/addons/{}/{}/public/f3d.png".format(
        server_url, ADDON_NAME, __version__
    )


def get_f3d_paths_from_settings(addon_settings=None):
    """

    Args:
        addon_settings (Optional[dict[str, Any]): Addon settings.

    Returns:
        list[str]: List to f3d executable paths. Paths are not validated.
    """

    if addon_settings is None:
        addon_settings = ayon_api.get_addon_settings(ADDON_NAME, __version__)

    platform_name = platform.system().lower()
    return addon_settings.get("f3d_path", {}).get(platform_name, [])


def get_f3d_executable_path(paths=None, addon_settings=None):
    """

    Args:
        paths (Optional[list[str]]): List of paths to f3d executable.
        addon_settings (Optional[dict[str, Any]): Addon settings.

    Returns:
        list[str]: List of available paths to f3d executable.
    """

    if paths is None:
        paths = get_f3d_paths_from_settings(addon_settings)

    for path in paths:
        if path and os.path.exists(path):
            return path
    return None


class F3dExecutableCache:
    lifetime = 10

    def __init__(self):
        self._cached_time = None
        self._f3d_paths = None
        self._f3d_path = None

    def is_cache_valid(self):
        """Cache is valid.

        Returns:
            bool: True if cache is valid, False otherwise.
        """

        if self._cached_time is None:
            return False

        start = time.time()
        return (start - self._cached_time) <= self.lifetime

    def get_paths(self):
        """Get all paths to f3d executable from settings.

        Returns:
            list[str]: Path to f3d executables.
        """

        if not self.is_cache_valid():
            self._f3d_paths = get_f3d_paths_from_settings()
            self._cached_time = time.time()
        return self._f3d_paths

    def get_path(self):
        """Get path to f3d executable.

        Returns:
            Union[str, None]: Path to f3d executable or None.
        """

        if not self.is_cache_valid():
            self._f3d_path = get_f3d_executable_path(self.get_paths())
        return self._f3d_path

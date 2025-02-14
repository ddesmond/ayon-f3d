import os
from ayon_core.addon import AYONAddon, IPluginPaths

from .version import __version__
from .constants import ADDON_NAME, F3D_ROOT


class F3dAddon(AYONAddon, IPluginPaths):
    """Addon adds f3d functionality via plugins."""

    name = ADDON_NAME
    version = __version__

    def get_plugin_paths(self):
        return {
            "load": self.get_load_plugin_paths()
        }

    def get_load_plugin_paths(self, host_name=None):
        return [
            os.path.join(F3D_ROOT, "plugins", "load"),
        ]

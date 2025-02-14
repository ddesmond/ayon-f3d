import os
import time

from ayon_core.lib import run_detached_process
from ayon_core.pipeline import load

from ayon_f3d.utils import F3dExecutableCache


class OpenInF3d(load.LoaderPlugin):
    """Open Geomtery with system default"""

    _executable_cache = F3dExecutableCache()
    product_types = ["pointcache", "usd", "model", "assembly", "animation"]
    representations = ["*"]
    extensions = {"*"}

    label = "Open in F3d"
    order = -10
    icon = "play-circle"
    color = "orange"

    @classmethod
    def get_f3d_path(cls):
        return cls._executable_cache.get_path()

    @classmethod
    def is_compatible_loader(cls, context):
        if not cls.get_f3d_path():
            return False
        return super().is_compatible_loader(context)

    def load(self, context, name, namespace, data):

        path = self.filepath_from_context(context)
        directory = os.path.dirname(path)

        self.log.info("Opening : {}".format(path))

        executable = self.get_f3d_path()
        cmd = [
            # f3d path
            str(executable),
            # PATH TO COMPONENT
            path
        ]

        try:
            # Run f3d with these commands
            run_detached_process(cmd)
            # Keep process in memory for some time
            time.sleep(0.1)

        except FileNotFoundError:
            self.log.error(
                f"File \"{os.path.basename(filepath)}\" was not found."
            )

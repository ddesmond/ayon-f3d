import os
import time

import clique

from ayon_core.lib import run_detached_process
from ayon_core.lib.transcoding import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS
from ayon_core.pipeline import load

from ayon_f3d.utils import F3dExecutableCache


class OpenInF3d(load.LoaderPlugin):
    """Open Geomtery with system default"""

    _executable_cache = F3dExecutableCache()
    product_types = ["*"]
    representations = ["*"]
    extensions = {
        ext.lstrip(".")
        for ext in set(IMAGE_EXTENSIONS) | set(VIDEO_EXTENSIONS)
    }

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

        pattern = clique.PATTERNS["frames"]
        files = os.listdir(directory)
        collections, remainder = clique.assemble(
            files,
            patterns=[pattern],
            minimum_items=1
        )

        if not remainder:
            sequence = collections[0]
            first_image = list(sequence)[0]
        else:
            first_image = path
        filepath = os.path.normpath(os.path.join(directory, first_image))

        self.log.info("Opening : {}".format(filepath))

        executable = self.get_f3d_path()
        cmd = [
            # f3d path
            str(executable),
            # PATH TO COMPONENT
            filepath
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

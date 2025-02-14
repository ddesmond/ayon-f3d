from ayon_server.settings import (
    BaseSettingsModel,
    SettingsField,
    MultiplatformPathListModel,
)


class F3dsettings(BaseSettingsModel):
    """f3d addon settings."""

    enabled: bool = SettingsField(True)
    f3d_path: MultiplatformPathListModel = SettingsField(
        title="f3d paths",
        default_factory=MultiplatformPathListModel,
        scope=["studio"],
    )


DEFAULT_VALUES = {
    "enabled": True,
    "f3d_path": {
        "windows": [
            "C:\\Program Files\\f3d\\bin\\f3d.exe",
        ],
        "linux": [
            "/usr/bin/f3d",
            "/opt/F3D-3.0.0-Linux-x86_64-raytracing/bin/f3d",
        ],
        "darwin": [
            "/Applications/f3d.app/Contents/MacOS/f3d",
        ]
    }
}

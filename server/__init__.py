from typing import Type

from ayon_server.addons import BaseServerAddon

from .settings import F3dsettings, DEFAULT_VALUES


class F3dAddon(BaseServerAddon):
    settings_model: Type[F3dsettings] = F3dsettings

    async def get_default_settings(self):
        settings_model_cls = self.get_settings_model()
        return settings_model_cls(**DEFAULT_VALUES)

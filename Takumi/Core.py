from functools import partial
from typing import TYPE_CHECKING, Any, final

from ep_plugintakumi_builtin_fonts import get_font_bytes, list_fonts
from ErisPulse import i18n
from ErisPulse.Core.Bases import BaseModule
from takumi_py import FontResource, Renderer
from typing_extensions import override

from .Config import TakumiConfig
from .Constants import BUILTIN_FONTS, FONT_AWARE_METHODS
from .I18n import TakumiI18n

# 静态分析/IDE 补全用：让 Main 在类型检查时表现为 Renderer 子类；
if TYPE_CHECKING:
    _RendererBase = Renderer
else:
    _RendererBase = object


@final
class Main(BaseModule, _RendererBase):

    ConfigClass = TakumiConfig
    I18nClass = TakumiI18n

    def __init__(self, sdk): # pyright: ignore[reportMissingSuperCall]

        self.sdk = sdk
        self.logger = self.sdk.logger.get_child("Takumi")
        self.storage = self.sdk.storage
        self.adapter = self.sdk.adapter
        self.client = self.sdk.client

        self.renderer, self.families = self._create_renderer()
        self.fonts = tuple(list_fonts())

        self.logger.info(i18n.t("Takumi.init_done", count=len(self.fonts)))

    @staticmethod
    def _create_renderer(**kwargs: Any) -> tuple[Renderer, tuple[str, ...]]:
        kwargs.setdefault("load_default_fonts", False)
        renderer = Renderer(**kwargs)
        families: list[str] = []
        for filename, name, style, generic_family in BUILTIN_FONTS:
            registered = renderer.register_font(
                FontResource(
                    get_font_bytes(filename),
                    name=name,
                    style=style,
                    generic_family=generic_family,
                )
            )
            families.extend(registered)

        return renderer, tuple(dict.fromkeys(families))

    def create_renderer(self, **kwargs: Any) -> Renderer:
        renderer, _ = self._create_renderer(**kwargs)
        return renderer

    def __getattr__(self, name: str):
        renderer = self.__dict__.get("renderer")
        if renderer is None:
            raise AttributeError(name)

        try:
            attribute = getattr(renderer, name)
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__!s} object has no attribute {name!r}"
            ) from None

        if name in FONT_AWARE_METHODS:
            return partial(self._call_renderer, name)
        return attribute

    def _call_renderer(self, method: str, *args, **kwargs):
        options = kwargs.get("options")
        if "font_families" not in kwargs and (
            options is None or options.font_families is None
        ):
            kwargs["font_families"] = self.families
        return getattr(self.renderer, method)(*args, **kwargs)

    @staticmethod
    @override
    def get_load_strategy():
        from ErisPulse.loaders.strategy import ModuleLoadStrategy

        return ModuleLoadStrategy(lazy_load=True, priority=100)

    @override
    async def on_load(self, event: dict[str, Any]) -> bool:
        # await self._register_message_handlers()
        self.logger.info(i18n.t("Takumi.module_loaded", event=event))
        return True

    @override
    async def on_unload(self, event: dict[str, Any]) -> bool:
        self.logger.info(i18n.t("Takumi.module_unloaded", event=event))
        return True

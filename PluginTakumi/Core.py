from dataclasses import dataclass, field
from functools import partial
from typing import Any, final

from ep_plugintakumi_builtin_fonts import get_font_bytes, list_fonts
from ErisPulse.Core.Bases import BaseModule
from ErisPulse.runtime.config_schema import BaseConfig
from takumi_py import FontResource, GenericFontFamily, Renderer
from typing_extensions import override

_BUILTIN_FONTS: tuple[tuple[str, str, str, GenericFontFamily], ...] = (
    ("NotoSansSC-VariableFont_wght.ttf", "Noto Sans SC", "normal", "sans-serif"),
    ("Roboto-VariableFont_wdth,wght.ttf", "Roboto", "normal", "sans-serif"),
    ("Roboto-Italic-VariableFont_wdth,wght.ttf", "Roboto", "italic", "sans-serif"),
    (
        "SourceCodePro-VariableFont_wght.ttf",
        "Source Code Pro",
        "normal",
        "monospace",
    ),
    (
        "SourceCodePro-Italic-VariableFont_wght.ttf",
        "Source Code Pro",
        "italic",
        "monospace",
    ),
)

_FONT_AWARE_METHODS = frozenset(
    {
        "measure_compiled",
        "measure_html",
        "measure_node",
        "render_animation",
        "render_compiled",
        "render_html",
        "render_node",
        "render_sequence_at_time",
        "render_svg_compiled",
        "render_svg_html",
        "render_svg_node",
        "render_svg_template",
        "render_template",
    }
)


@dataclass
class PluginTakumiConfig(BaseConfig):
    """PluginTakumi 模块配置"""

    enabled: bool = field(
        default=True,
        metadata={
            "description": "是否启用模块",
        },
    )


@final
class Main(BaseModule):
    """
    PluginTakumi 模块

    封装 takumi-py 的 API，并提供开箱即用的中英文字体。
    """

    ConfigClass = PluginTakumiConfig

    def __init__(self, sdk=None):
        from ErisPulse import sdk as _sdk

        self.sdk = _sdk if sdk is None else sdk
        self.logger = self.sdk.logger.get_child("PluginTakumi")  # pyright: ignore [reportCallIssue]
        self.storage = self.sdk.storage
        self.adapter = self.sdk.adapter
        self.client = self.sdk.client

        self.renderer, self.families = self._create_renderer()
        self.fonts = tuple(list_fonts())

        self.logger.info(
            f"PluginTakumi 初始化完成，已加载 {len(self.fonts)} 个内置字体文件"
        )

    @staticmethod
    def _create_renderer(**kwargs: Any) -> tuple[Renderer, tuple[str, ...]]:
        kwargs.setdefault("load_default_fonts", False)
        renderer = Renderer(**kwargs)
        families: list[str] = []
        for filename, name, style, generic_family in _BUILTIN_FONTS:
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
        """创建一个已注册插件内置字体的独立 Renderer 实例。"""
        renderer, _ = self._create_renderer(**kwargs)
        return renderer

    def __getattr__(self, name: str):
        """将 takumi-py Renderer API 暴露到模块实例上。"""
        renderer = self.__dict__.get("renderer")
        if renderer is None:
            raise AttributeError(name)

        try:
            attribute = getattr(renderer, name)
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__!s} object has no attribute {name!r}"
            ) from None

        if name in _FONT_AWARE_METHODS:
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

        return ModuleLoadStrategy(lazy_load=False, priority=100)

    @override
    async def on_load(self, event: dict[str, Any]) -> bool:
        """
        模块被加载时调用

        :param event: 事件内容
        :return: 处理结果
        """
        # await self._register_message_handlers()
        self.logger.info(f"模块已加载: {event}")
        return True

    @override
    async def on_unload(self, event: dict[str, Any]) -> bool:
        """
        模块被卸载时调用

        :param event: 事件内容
        :return: 处理结果
        """
        self.logger.info(f"模块已卸载: {event}")
        return True

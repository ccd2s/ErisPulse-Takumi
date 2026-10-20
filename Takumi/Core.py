import tempfile
import uuid
from pathlib import Path
from typing import Any

from ep_plugintakumi_builtin_fonts import get_font_bytes, list_fonts
from ErisPulse import i18n
from ErisPulse.Core.Bases import BaseModule, ModuleMeta
from takumi_py import AnimationScene, FontResource, Renderer, parse_html

from .Constants import BUILTIN_FONTS
from .I18n import TakumiI18n


class Main(BaseModule):

    I18nClass = TakumiI18n

    def __init__(self, sdk):
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

    def _fonts(self, kwargs: dict) -> dict:
        if not kwargs.get("font_families"):
            kwargs["font_families"] = self.families
        return kwargs

    def _render_html(self, html: str, **kwargs: Any) -> bytes:
        return self.render_html(html, **kwargs)

    def _render_animation(self, scenes: list, **kwargs: Any) -> bytes:
        return self.render_animation(scenes, **kwargs)

    def _parse_node(self, html: str):
        return parse_html(html).node

    def render_html(self, html: str, **kwargs: Any) -> bytes:
        return self.renderer.render_html(html, **self._fonts(kwargs))

    def render_node(self, node: Any, **kwargs: Any) -> bytes:
        return self.renderer.render_node(node, **self._fonts(kwargs))

    def render_compiled(self, node: Any, **kwargs: Any) -> bytes:
        return self.renderer.render_compiled(node, **self._fonts(kwargs))

    def render_template(self, template_name: str, context: Any, **kwargs: Any) -> bytes:
        return self.renderer.render_template(template_name, context, **self._fonts(kwargs))

    def render_sequence_at_time(self, scenes: list, time_ms: int, **kwargs: Any) -> bytes:
        return self.renderer.render_sequence_at_time(scenes, time_ms, **self._fonts(kwargs))

    def render_animation(self, scenes: list, **kwargs: Any) -> bytes:
        return self.renderer.render_animation(scenes, **self._fonts(kwargs))

    def render_svg_html(self, html: str, **kwargs: Any) -> str:
        return self.renderer.render_svg_html(html, **self._fonts(kwargs))

    def render_svg_node(self, node: Any, **kwargs: Any) -> str:
        return self.renderer.render_svg_node(node, **self._fonts(kwargs))

    def render_svg_compiled(self, node: Any, **kwargs: Any) -> str:
        return self.renderer.render_svg_compiled(node, **self._fonts(kwargs))

    def render_svg_template(self, template_name: str, context: Any, **kwargs: Any) -> str:
        return self.renderer.render_svg_template(template_name, context, **self._fonts(kwargs))

    def measure_html(self, html: str, **kwargs: Any):
        return self.renderer.measure_html(html, **self._fonts(kwargs))

    def measure_node(self, node: Any, **kwargs: Any):
        return self.renderer.measure_node(node, **self._fonts(kwargs))

    def measure_compiled(self, node: Any, **kwargs: Any):
        return self.renderer.measure_compiled(node, **self._fonts(kwargs))

    def compile_html(self, html: str, **kwargs: Any):
        return self.renderer.compile_html(html, **kwargs)

    def compile_node(self, node: Any, **kwargs: Any):
        return self.renderer.compile_node(node, **kwargs)

    def compile_stylesheet(self, css: str):
        return self.renderer.compile_stylesheet(css)

    def compile_stylesheet_lossy(self, css: str):
        return self.renderer.compile_stylesheet_lossy(css)

    def compile_keyframes(self, keyframes: Any):
        return self.renderer.compile_keyframes(keyframes)

    def encode_frames(self, frames: list, **kwargs: Any) -> bytes:
        return self.renderer.encode_frames(frames, **kwargs)

    def register_font(self, font: Any) -> tuple[str, ...]:
        return self.renderer.register_font(font)

    def register_fonts(self, fonts: list) -> tuple[str, ...]:
        return self.renderer.register_fonts(fonts)

    def load_font(self, font: Any) -> None:
        self.renderer.load_font(font)

    def load_fonts(self, fonts: list) -> None:
        self.renderer.load_fonts(fonts)

    def list_builtin_fonts(self) -> list[str]:
        return list(self.fonts)

    def list_font_families(self) -> tuple[str, ...]:
        return self.families

    def put_persistent_image(self, resource, data: bytes | None = None, cache: str = "auto") -> None:
        self.renderer.put_persistent_image(resource, data, cache=cache)

    def clear_image_store(self) -> None:
        self.renderer.clear_image_store()

    def _parse_node_public(self, html: str):
        return self._parse_node(html)

    @staticmethod
    def get_load_strategy():
        from ErisPulse.loaders.strategy import ModuleLoadStrategy

        return ModuleLoadStrategy(lazy_load=True, priority=100)

    @staticmethod
    def get_meta():
        info = dict(
            name="Takumi",
            description="HTML/CSS 渲染引擎：卡片、海报、SVG、模板与 GIF 动图",
            version="1.3.0",
            group="工具",
            tags=["render", "image", "svg", "html"],
            services=[
                {
                    "name": "render_card",
                    "description": "渲染 HTML 为图片文件（PNG/JPEG），返回本地文件路径；height 传 0 按内容自适应",
                    "parameters": {
                        "html": "要渲染的完整 HTML 文档或片段（内联 CSS 生效）",
                        "width": "视口宽度（px，默认 800）",
                        "height": "视口高度（px，0 按内容自适应）",
                        "image_format": "png（默认）或 jpeg",
                        "stylesheets": "额外样式表列表",
                    },
                },
                {
                    "name": "render_gif",
                    "description": "渲染 HTML 为循环 GIF 动图文件，返回本地文件路径",
                    "parameters": {
                        "html": "要渲染的 HTML（可用 CSS 动画）",
                        "duration_ms": "动画循环时长（毫秒，默认 1200）",
                        "width": "视口宽度（px，默认 800）",
                        "height": "视口高度（px，0 按内容自适应）",
                        "stylesheets": "额外样式表列表",
                    },
                },
                {
                    "name": "render_html_ex",
                    "description": "render_html 全参版：渲染 HTML 为图片文件，支持 quality/lossless/time_ms/device_pixel_ratio/images 等全部渲染参数",
                    "parameters": {
                        "html": "要渲染的 HTML",
                        "options": "渲染参数字典（width/height/format/quality/time_ms/font_size/images 等，透传 takumi-py）",
                    },
                },
                {
                    "name": "render_svg",
                    "description": "渲染 HTML 为 SVG 文本（矢量，无损缩放）",
                    "parameters": {
                        "html": "要渲染的 HTML",
                        "options": "渲染参数字典（width/height/time_ms/font_families 等）",
                    },
                },
                {
                    "name": "measure_html",
                    "description": "测量 HTML 内容尺寸（不渲染出图），用于自适应排版决策",
                    "parameters": {
                        "html": "要测量的 HTML",
                        "options": "渲染参数字典（width/font_size 等）",
                    },
                },
                {
                    "name": "compile_html",
                    "description": "预编译 HTML 为可复用的 CompiledHtml（同一内容多次渲染/多时刻截图时更快），配合 render_compiled 使用",
                    "parameters": {"html": "要编译的 HTML"},
                },
                {
                    "name": "render_compiled",
                    "description": "渲染 compile 系列的产物（CompiledHtml/CompiledNode）为图片",
                    "parameters": {
                        "compiled": "compile_html/compile_node 的返回值",
                        "options": "渲染参数字典（time_ms 等可变参数）",
                    },
                },
                {
                    "name": "list_fonts",
                    "description": "列出内置字体文件与可用字体族",
                },
            ],
        )
        return ModuleMeta(**info)

    def _save_render(self, data: bytes, image_format: str) -> dict:
        suffix = "jpg" if image_format == "jpeg" else image_format
        path = Path(tempfile.gettempdir()) / f"takumi_{uuid.uuid4().hex[:8]}.{suffix}"
        path.write_bytes(data)
        return {"path": str(path), "bytes": len(data)}

    def render_card(
        self,
        html: str,
        width: int = 800,
        height: int = 0,
        image_format: str = "png",
        stylesheets: list | None = None,
    ) -> dict:
        data = self.render_html(
            html,
            stylesheets=stylesheets,
            width=width,
            height=height if height and height > 0 else None,
            format=image_format,
        )
        return self._save_render(data, image_format)

    def render_gif(
        self,
        html: str,
        duration_ms: int = 1200,
        width: int = 800,
        height: int = 0,
        stylesheets: list | None = None,
    ) -> dict:
        node = self._parse_node(html)
        scene = AnimationScene(node=node, duration_ms=duration_ms)
        data = self.render_animation(
            [scene],
            stylesheets=stylesheets,
            width=width,
            height=height if height and height > 0 else None,
        )
        return self._save_render(data, "gif")

    def render_html_ex(self, html: str, options: dict | None = None) -> dict:
        data = self.render_html(html, **(options or {}))
        fmt = str((options or {}).get("format") or "png")
        return self._save_render(data, fmt)

    def render_svg(self, html: str, options: dict | None = None) -> dict:
        return {"svg": self.render_svg_html(html, **(options or {}))}

    def measure(self, html: str, options: dict | None = None) -> dict:
        m = self.measure_html(html, **(options or {}))
        info = {}
        for key in ("width", "height", "font_size"):
            value = getattr(m, key, None)
            if value is not None:
                info[key] = value
        return info or {"repr": str(m)[:200]}

    def render_compiled_ex(self, compiled: Any, options: dict | None = None) -> dict:
        # CompiledHtml（compile_html 产物）需取其 node；CompiledNode 可直接渲染
        if not hasattr(compiled, "tag") and hasattr(compiled, "node"):
            compiled = compiled.node
        data = self.render_compiled(compiled, **(options or {}))
        fmt = str((options or {}).get("format") or "png")
        return self._save_render(data, fmt)

    def list_fonts(self) -> dict:
        return {"builtin_files": list(self.fonts), "families": list(self.families)}

    async def on_load(self, event: dict[str, Any]) -> bool:
        return True

    async def on_unload(self, event: dict[str, Any]) -> bool:
        return True

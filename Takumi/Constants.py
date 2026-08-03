from takumi_py import GenericFontFamily

BUILTIN_FONTS: tuple[tuple[str, str, str, GenericFontFamily], ...] = (
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

FONT_AWARE_METHODS: frozenset[str] = frozenset(
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

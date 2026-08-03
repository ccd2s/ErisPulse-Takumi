# ErisPulse-Takumi

基于 [takumi-py](https://github.com/BalconyJH/takumi-py) 的 ErisPulse 图片渲染模块，内置中英文及等宽字体。

## 特性

- 通过 `sdk.Takumi` 直接使用 `takumi-py` 的 `Renderer` API
- 自动注册 Noto Sans SC、Roboto 和 Source Code Pro
- 自动把内置字体作为渲染、测量、SVG 和动画接口的回退字体
- 可创建带有全部内置字体的独立 `Renderer` 实例
- 支持 HTML、节点树、Jinja 模板、SVG 和动画渲染

## 安装

```bash
epsdk install Takumi
```

## 使用

模块会自动加载，通过 `sdk.Takumi` 访问模块实例。

### 渲染 HTML

```python
from ErisPulse import sdk

png = sdk.Takumi.render_html(
    """
    <div class="card">
      <h1>你好，ErisPulse</h1>
      <p>Hello from Takumi</p>
    </div>
    """,
    stylesheets=["""
    .card {
      width: 800px;
      height: 400px;
      padding: 48px;
      color: white;
      background: #111827;
      font-family: "Noto Sans SC";
    }
    """],
    width=800,
    height=400,
    lang="zh-CN",
)
```

### 渲染节点树

```python
png = sdk.Takumi.render_node(
    {
        "type": "text",
        "text": "中文和 English 都可直接渲染",
        "style": {"fontSize": 48, "color": "#111827"},
    },
    width=800,
    height=200,
    lang="zh-CN",
)
```

### 使用原生 Renderer

`sdk.Takumi.renderer` 是原始 `takumi_py.Renderer` 实例，适用于需要完全控制参数的场景。模块级渲染接口会自动传入内置字体回退栈；直接调用 `renderer` 时可以手动传入：

```python
png = sdk.Takumi.renderer.render_html(
    "<div>你好</div>",
    font_families=sdk.Takumi.families,
    lang="zh-CN",
)
```

### 创建独立 Renderer

需要隔离字体、图片或资源缓存时，可以创建新的 `Renderer`。每次调用都会返回一个独立实例，并自动注册本插件的全部内置字体：

```python
renderer = sdk.Takumi.create_renderer(cache_max_bytes=64 * 1024 * 1024)

png = renderer.render_html(
    "<div>独立 Renderer / 独立渲染器</div>",
    font_families=sdk.Takumi.families,
    width=800,
    height=200,
    lang="zh-CN",
)
```

`create_renderer()` 接受 `takumi_py.Renderer` 的构造参数。默认使用 `load_default_fonts=False`，只加载插件内置字体；如需同时加载 Takumi 自带字体，可显式传入 `load_default_fonts=True`。通过 `fonts` 传入的自定义字体也会与插件内置字体一起注册：

```python
renderer = sdk.Takumi.create_renderer(
    load_default_fonts=True,
    fonts=[custom_font],
)
```

独立实例不会经过模块的接口代理，因此调用渲染或测量方法时，如需统一的内置字体回退栈，应显式传入 `font_families=sdk.Takumi.families`。

可通过以下属性查看内置资源：

- `sdk.Takumi.fonts`：字体文件名元组
- `sdk.Takumi.families`：已注册的字体 family 元组

如果显式传入 `font_families`，模块会尊重调用方设置，不再注入默认回退栈。`RenderOptions(font_families=...)` 同样有效。

## 配置

在 `config.toml` 中添加:

```toml
[Takumi]
enabled = true
```

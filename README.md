# PluginTakumi

基于 [takumi-py](https://github.com/BalconyJH/takumi-py) 的 ErisPulse 图片渲染模块，内置中英文及等宽字体。

## 特性

- 通过 `sdk.PluginTakumi` 直接使用 `takumi-py` 的 `Renderer` API
- 自动注册 Noto Sans SC、Roboto 和 Source Code Pro
- 自动把内置字体作为渲染、测量、SVG 和动画接口的回退字体
- 支持 HTML、节点树、Jinja 模板、SVG 和动画渲染

## 安装

```bash
epsdk install PluginTakumi
```

## 使用

模块会自动加载，通过 `sdk.PluginTakumi` 访问模块实例。

### 渲染 HTML

```python
from ErisPulse import sdk

png = sdk.PluginTakumi.render_html(
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
png = sdk.PluginTakumi.render_node(
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

`sdk.PluginTakumi.renderer` 是原始 `takumi_py.Renderer` 实例，适用于需要完全控制参数的场景。模块级渲染接口会自动传入内置字体回退栈；直接调用 `renderer` 时可以手动传入：

```python
png = sdk.PluginTakumi.renderer.render_html(
    "<div>你好</div>",
    font_families=sdk.PluginTakumi.families,
    lang="zh-CN",
)
```

可通过以下属性查看内置资源：

- `sdk.PluginTakumi.fonts`：字体文件名元组
- `sdk.PluginTakumi.families`：已注册的字体 family 元组

如果显式传入 `font_families`，模块会尊重调用方设置，不再注入默认回退栈。`RenderOptions(font_families=...)` 同样有效。

## 配置

在 `config.toml` 中添加:

```toml
[PluginTakumi]
enabled = true
```

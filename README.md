<div align="center">

<img src=".github/assets/ErisPulseLogo.png" width="180" alt="ErisPulse-Takumi" />

# ErisPulse-Takumi

**Render images in your Bot — HTML / node trees / SVG / animations, with CJK fonts out of the box.**

<p>
  <a href="https://pypi.org/project/ErisPulse-Takumi/"><img src="https://img.shields.io/pypi/v/ErisPulse-Takumi?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="https://pypi.org/project/ErisPulse-Takumi/"><img src="https://img.shields.io/badge/Python-3.10+-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-GPL--3.0-blue?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/ccd2s/ErisPulse-Takumi"><img src="https://img.shields.io/github/stars/ccd2s/ErisPulse-Takumi?style=for-the-badge&logo=github&color=brightgreen" alt="Stars"></a>
  <a href="https://pepy.tech/project/ErisPulse-Takumi"><img src="https://img.shields.io/pepy/dt/ErisPulse-Takumi?style=for-the-badge&color=blue" alt="Downloads"></a>
  <a href="https://github.com/ErisPulse/ErisPulse"><img src="https://img.shields.io/badge/Powered_by-ErisPulse-FF6B9D?style=for-the-badge&logo=bookstack&logoColor=white" alt="ErisPulse"></a>
</p>

[English](#english) | [简体中文](#简体中文)

</div>

---

<a id="english"></a>

## English

Image rendering for ErisPulse, built on [takumi-py](https://github.com/BalconyJH/takumi-py). Noto Sans SC, Roboto and Source Code Pro are bundled, so Chinese / English / monospace text just works — no extra font setup.

Supports HTML, node trees, Jinja templates, SVG and animations.

### Install

```bash
epsdk install Takumi
```

### Usage

The module auto-loads. Grab it through the module manager, or use the `sdk` shortcut:

```python
from ErisPulse import sdk

takumi = sdk.module.get("Takumi")
# equivalent: takumi = sdk.Takumi
```

#### Render HTML

```python
png = takumi.render_html(
    """
    <div class="card">
      <h1>Hello, ErisPulse</h1>
      <p>Rendered by Takumi</p>
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

#### Render a node tree

```python
png = takumi.render_node(
    {
        "type": "text",
        "text": "中英混排 renders fine",
        "style": {"fontSize": 48, "color": "#111827"},
    },
    width=800,
    height=200,
    lang="zh-CN",
)
```

#### Raw Renderer

`takumi.renderer` is the underlying `takumi_py.Renderer`. The convenience methods above inject the bundled font fallback automatically; when you call the renderer directly, pass the families yourself:

```python
png = takumi.renderer.render_html(
    "<div>hello</div>",
    font_families=takumi.families,
    lang="zh-CN",
)
```

#### Independent Renderer

Need isolated font / image / resource caches? Spin up a fresh `Renderer` — the bundled fonts are auto-registered:

```python
renderer = takumi.create_renderer(cache_max_bytes=64 * 1024 * 1024)

png = renderer.render_html(
    "<div>isolated renderer</div>",
    font_families=takumi.families,
    width=800,
    height=200,
    lang="zh-CN",
)
```

`create_renderer()` takes the `takumi_py.Renderer` constructor kwargs. It defaults to `load_default_fonts=False` (bundled fonts only); pass `load_default_fonts=True` to also load Takumi's own, and `fonts=[...]` to register custom fonts alongside.

An independent instance bypasses the module proxy, so pass `font_families=takumi.families` explicitly to keep the same fallback stack.

Bundled resources:

- `takumi.fonts` — bundled font filenames
- `takumi.families` — registered font families

Pass `font_families` yourself and the module respects it — no default fallback is injected. `RenderOptions(font_families=...)` works too.

### Config

```toml
[Takumi]
enabled = true
```

---

<a id="简体中文"></a>

## 简体中文

ErisPulse 的图片渲染模块，基于 [takumi-py](https://github.com/BalconyJH/takumi-py)。内置 Noto Sans SC、Roboto、Source Code Pro，中文 / 英文 / 等宽文本开箱即用，无需额外配置字体。

支持 HTML、节点树、Jinja 模板、SVG 和动画渲染。

### 安装

```bash
epsdk install Takumi
```

### 使用

模块会自动加载，通过模块管理器获取，也可以用 `sdk` 快捷方式：

```python
from ErisPulse import sdk

takumi = sdk.module.get("Takumi")
# 等价写法：takumi = sdk.Takumi
```

#### 渲染 HTML

```python
png = takumi.render_html(
    """
    <div class="card">
      <h1>你好，ErisPulse</h1>
      <p>由 Takumi 渲染</p>
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

#### 渲染节点树

```python
png = takumi.render_node(
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

#### 原生 Renderer

`takumi.renderer` 是原始的 `takumi_py.Renderer` 实例。上面的便捷方法会自动注入内置字体回退栈；直接调用 renderer 时自行传入 families：

```python
png = takumi.renderer.render_html(
    "<div>你好</div>",
    font_families=takumi.families,
    lang="zh-CN",
)
```

#### 独立 Renderer

需要隔离字体 / 图片 / 资源缓存时，创建新的 `Renderer`，内置字体会自动注册：

```python
renderer = takumi.create_renderer(cache_max_bytes=64 * 1024 * 1024)

png = renderer.render_html(
    "<div>独立 Renderer</div>",
    font_families=takumi.families,
    width=800,
    height=200,
    lang="zh-CN",
)
```

`create_renderer()` 接受 `takumi_py.Renderer` 的构造参数。默认 `load_default_fonts=False`（仅加载内置字体）；传入 `load_default_fonts=True` 可同时加载 Takumi 自带字体，`fonts=[...]` 可一并注册自定义字体。

独立实例不经过模块代理，因此若要保留统一的内置字体回退栈，需显式传入 `font_families=takumi.families`。

内置资源：

- `takumi.fonts`：内置字体文件名
- `takumi.families`：已注册的字体 family

若显式传入 `font_families`，模块会尊重调用方设置，不再注入默认回退栈。`RenderOptions(font_families=...)` 同样有效。

### 配置

```toml
[Takumi]
enabled = true
```

---

<div align="center">

**Related** · [ErisPulse](https://github.com/ErisPulse/ErisPulse) · [takumi-py](https://github.com/BalconyJH/takumi-py) · [Documentation](https://www.erisdev.com) · [Issues](https://github.com/ccd2s/ErisPulse-Takumi/issues)

</div>

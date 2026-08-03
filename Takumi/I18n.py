from ErisPulse.Core.Bases import BaseI18n, I18nKey


class TakumiI18n(BaseI18n):

    enabled: I18nKey = I18nKey(
        default="Enable module",
        zh_CN="是否启用模块",
        zh_TW="是否啟用模組",
        en="Enable module",
        ja="モジュールを有効化",
        ru="Включить модуль",
    )
    init_done: I18nKey = I18nKey(
        default="Takumi initialized, {count} builtin font(s) loaded",
        zh_CN="Takumi 初始化完成，已加载 {count} 个内置字体文件",
        zh_TW="Takumi 初始化完成，已載入 {count} 個內建字型",
        en="Takumi initialized, {count} builtin font(s) loaded",
        ja="Takumi の初期化が完了しました。内蔵フォント {count} 個を読み込みました",
        ru="Takumi инициализирован, загружено встроенных шрифтов: {count}",
    )
    module_loaded: I18nKey = I18nKey(
        default="Module loaded: {event}",
        zh_CN="模块已加载: {event}",
        zh_TW="模組已載入: {event}",
        en="Module loaded: {event}",
        ja="モジュールを読み込みました: {event}",
        ru="Модуль загружен: {event}",
    )
    module_unloaded: I18nKey = I18nKey(
        default="Module unloaded: {event}",
        zh_CN="模块已卸载: {event}",
        zh_TW="模組已卸載: {event}",
        en="Module unloaded: {event}",
        ja="モジュールを解除しました: {event}",
        ru="Модуль выгружен: {event}",
    )

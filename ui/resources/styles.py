"""Цветовые константы темы (синхронизируются через theme_manager)."""

PRIMARY_COLOR = "#2FC6F6"
PRIMARY_DARK = "#1BA8D4"
PRIMARY_LIGHT = "#E8F9FE"
SECONDARY_COLOR = "#525C69"
SUCCESS_COLOR = "#9DCF00"
WARNING_COLOR = "#FFA900"
ERROR_COLOR = "#FF5752"
INFO_COLOR = "#2FC6F6"
LIGHT_COLOR = "#F5F7F8"
DARK_COLOR = "#333B4F"

ACCENT = "#FF5752"
ACCENT_LIGHT = "#FFF0F0"

BG_MAIN = "#F4F6FA"
BG_CARD = "#FFFFFF"
BG_HEADER = "#FFFFFF"

TEXT_PRIMARY = "#0F172A"
TEXT_SECONDARY = "#64748B"
TEXT_WHITE = "#FFFFFF"

BORDER = "#E0E4EA"
BORDER_LIGHT = "#EEF0F3"
DIVIDER = "#E8EAED"

SIDEBAR_BG = "#0F172A"
SIDEBAR_HOVER = "#3E4659"
SIDEBAR_ACTIVE = "#2FC6F6"
SIDEBAR_TEXT = "#FFFFFF"
SIDEBAR_TEXT_DIM = "#A8B0BC"
SIDEBAR_BORDER = "#2A3140"

STATUS_NEW = "#2FC6F6"
STATUS_NEW_BG = "#E8F9FE"
STATUS_PROGRESS = "#FFA900"
STATUS_PROGRESS_BG = "#FFF8E6"
STATUS_REVIEW = "#9B59B6"
STATUS_REVIEW_BG = "#F5EEFF"
STATUS_DONE = "#9DCF00"
STATUS_DONE_BG = "#F3FBE6"

FONT_FAMILY = "'Segoe UI', 'Open Sans', sans-serif"

GLOBAL_STYLE = ""

COLORS = {
    'primary': PRIMARY_COLOR,
    'primary_dark': PRIMARY_DARK,
    'primary_light': PRIMARY_LIGHT,
    'accent': ACCENT,
    'bg_main': BG_MAIN,
    'bg_card': BG_CARD,
    'text_primary': TEXT_PRIMARY,
    'text_secondary': TEXT_SECONDARY,
    'border': BORDER,
    'status_new': STATUS_NEW,
    'status_new_bg': STATUS_NEW_BG,
    'status_progress': STATUS_PROGRESS,
    'status_progress_bg': STATUS_PROGRESS_BG,
    'status_review': STATUS_REVIEW,
    'status_review_bg': STATUS_REVIEW_BG,
    'status_done': STATUS_DONE,
    'status_done_bg': STATUS_DONE_BG,
}

try:
    from ui.resources.theme_manager import get_stylesheet, build_palette, sync_styles_module
    GLOBAL_STYLE = get_stylesheet()
    sync_styles_module(build_palette())
except Exception:
    pass

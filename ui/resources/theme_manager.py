"""Управление темой: светлая/тёмная, акцент, фон."""

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont, QColor

from ui.resources.style_builder import build_stylesheet

ORG = 'KABAN'
APP = 'KABAN:manager'

_current_palette = None

LIGHT_DEFAULTS = {
    'bg_main': '#EDEEF0',
    'bg_card': '#FFFFFF',
    'bg_header': '#FFFFFF',
    'input_bg': '#FFFFFF',
}

DARK_DEFAULTS = {
    'bg_main': '#181b21',
    'bg_card': '#23272f',
    'bg_header': '#23272f',
    'input_bg': '#2a2f38',
}

BG_PRESETS = {
    'default': '',
    'gray': '#E8E9EC',
    'blue': '#E8F4FC',
    'mint': '#E8F5F0',
    'warm': '#F5F0E8',
    'dark_gray': '#1a1d24',
    'dark_blue': '#151c28',
    'dark_purple': '#1a1824',
}


def _hex_to_rgb(hex_color):
    c = hex_color.lstrip('#')
    if len(c) == 3:
        c = ''.join(x * 2 for x in c)
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def _darken(hex_color, factor=0.18):
    r, g, b = _hex_to_rgb(hex_color)
    return f'#{int(r * (1 - factor)):02x}{int(g * (1 - factor)):02x}{int(b * (1 - factor)):02x}'


def _lighten(hex_color, factor=0.85):
    r, g, b = _hex_to_rgb(hex_color)
    return f'#{int(r + (255 - r) * factor):02x}{int(g + (255 - g) * factor):02x}{int(b + (255 - b) * factor):02x}'


def _accent_tint(hex_color, alpha=0.12):
    r, g, b = _hex_to_rgb(hex_color)
    return f'rgba({r}, {g}, {b}, {alpha})'


def get_config(settings=None):
    s = settings or QSettings(ORG, APP)
    theme = s.value('theme', 'light')
    if theme not in ('light', 'dark'):
        theme = 'light'
    preset = s.value('bg_preset', 'default')
    custom_bg = s.value('bg_color', '')
    bg_main = custom_bg or BG_PRESETS.get(preset, '') or ''
    return {
        'theme': theme,
        'accent': s.value('accent_color', '#2FC6F6'),
        'bg_main': bg_main,
        'bg_preset': preset,
        'font_size': max(8, min(16, int(s.value('font_size', 10)))),
    }


def build_palette(config=None):
    config = config or get_config()
    is_dark = config['theme'] == 'dark'
    accent = config['accent'] if QColor(config['accent']).isValid() else '#2FC6F6'
    base = DARK_DEFAULTS if is_dark else LIGHT_DEFAULTS

    bg_main = config['bg_main'] or base['bg_main']

    if is_dark:
        p = {
            'bg_main': bg_main,
            'bg_card': '#23272f',
            'bg_header': '#23272f',
            'input_bg': '#2a2f38',
            'text_primary': '#e8eaed',
            'text_secondary': '#9aa0a9',
            'text_white': '#ffffff',
            'text_on_primary': '#ffffff',
            'border': '#3a3f4b',
            'border_light': '#2e333d',
            'border_hover': '#4a5060',
            'divider': '#363b47',
            'table_alt': '#1e2229',
            'table_header': '#2a2f38',
            'kanban_col_bg': '#1e2229',
            'scrollbar': '#4a5060',
            'scrollbar_hover': '#5a6070',
            'sidebar_bg': '#14171c',
            'sidebar_hover': '#1f242d',
            'sidebar_user_bg': '#101318',
            'sidebar_text': '#ffffff',
            'sidebar_text_dim': '#8b939e',
            'sidebar_border': '#0d0f13',
            'sidebar_active_bg': _accent_tint(accent, 0.18),
        }
        status_new_bg = '#1a2a32'
        status_progress_bg = '#2a2418'
        status_review_bg = '#241a2e'
        status_done_bg = '#1a2a1a'
        accent_light = '#3a2020'
    else:
        p = {
            'bg_main': bg_main,
            'bg_card': '#FFFFFF',
            'bg_header': '#FFFFFF',
            'input_bg': '#FFFFFF',
            'text_primary': '#333333',
            'text_secondary': '#828B95',
            'text_white': '#ffffff',
            'text_on_primary': '#ffffff',
            'border': '#E0E4EA',
            'border_light': '#EEF0F3',
            'border_hover': '#C0C8D6',
            'divider': '#E8EAED',
            'table_alt': '#FAFBFC',
            'table_header': '#F7F8FA',
            'kanban_col_bg': '#F0F2F5',
            'scrollbar': '#C5CAD3',
            'scrollbar_hover': '#A0A8B4',
            'sidebar_bg': '#333B4F',
            'sidebar_hover': '#3E4659',
            'sidebar_user_bg': '#2A3140',
            'sidebar_text': '#ffffff',
            'sidebar_text_dim': '#A8B0BC',
            'sidebar_border': '#2A3140',
            'sidebar_active_bg': _accent_tint(accent, 0.15),
        }
        status_new_bg = '#E8F9FE'
        status_progress_bg = '#FFF8E6'
        status_review_bg = '#F5EEFF'
        status_done_bg = '#F3FBE6'
        accent_light = '#FFF0F0'

    p.update({
        'primary': accent,
        'primary_dark': _darken(accent, 0.15),
        'primary_pressed': _darken(accent, 0.25),
        'primary_light': _accent_tint(accent, 0.14 if not is_dark else 0.22),
        'success': '#9DCF00',
        'warning': '#FFA900',
        'error': '#FF5752',
        'accent_light': accent_light,
        'status_new': accent if is_dark else '#2FC6F6',
        'status_new_bg': status_new_bg,
        'status_progress': '#FFA900',
        'status_progress_bg': status_progress_bg,
        'status_review': '#9B59B6',
        'status_review_bg': status_review_bg,
        'status_done': '#9DCF00',
        'status_done_bg': status_done_bg,
    })
    return p


def get_stylesheet(config=None):
    return build_stylesheet(build_palette(config))


def get_login_styles(config=None):
    p = build_palette(config)
    return {
        'gradient': f'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {p["primary"]}, stop:0.5 {_lighten(p["primary"], 0.3)}, stop:1 {p["primary_dark"]})',
        'card_bg': p['bg_card'],
        'text_primary': p['text_primary'],
        'text_secondary': p['text_secondary'],
        'border': p['border'],
        'primary': p['primary'],
        'primary_dark': p['primary_dark'],
        'primary_light': p['primary_light'],
    }


def apply_theme(app, config=None):
    global _current_palette
    config = config or get_config()
    _current_palette = build_palette(config)
    app.setFont(QFont('Segoe UI', config['font_size']))
    stylesheet = build_stylesheet(_current_palette)
    app.setStyleSheet(stylesheet)
    sync_styles_module(_current_palette)
    return _current_palette


def current_palette():
    global _current_palette
    if _current_palette is None:
        _current_palette = build_palette()
    return _current_palette


def sync_styles_module(palette):
    """Синхронизирует ui.resources.styles для кода, импортирующего константы."""
    import ui.resources.styles as styles
    mapping = {
        'PRIMARY_COLOR': 'primary',
        'PRIMARY_DARK': 'primary_dark',
        'PRIMARY_LIGHT': 'primary_light',
        'BG_MAIN': 'bg_main',
        'BG_CARD': 'bg_card',
        'BG_HEADER': 'bg_header',
        'TEXT_PRIMARY': 'text_primary',
        'TEXT_SECONDARY': 'text_secondary',
        'TEXT_WHITE': 'text_white',
        'BORDER': 'border',
        'BORDER_LIGHT': 'border_light',
        'SIDEBAR_BG': 'sidebar_bg',
        'SIDEBAR_HOVER': 'sidebar_hover',
        'SIDEBAR_ACTIVE': 'primary',
        'SIDEBAR_TEXT': 'sidebar_text',
        'SIDEBAR_TEXT_DIM': 'sidebar_text_dim',
        'SIDEBAR_BORDER': 'sidebar_border',
        'STATUS_NEW': 'status_new',
        'STATUS_NEW_BG': 'status_new_bg',
        'STATUS_PROGRESS': 'status_progress',
        'STATUS_PROGRESS_BG': 'status_progress_bg',
        'STATUS_REVIEW': 'status_review',
        'STATUS_REVIEW_BG': 'status_review_bg',
        'STATUS_DONE': 'status_done',
        'STATUS_DONE_BG': 'status_done_bg',
        'ACCENT': 'error',
        'ACCENT_LIGHT': 'accent_light',
    }
    for attr, key in mapping.items():
        if key in palette:
            setattr(styles, attr, palette[key])
    styles.GLOBAL_STYLE = build_stylesheet(palette)
    styles.COLORS = {k: palette.get(k, v) for k, v in styles.COLORS.items() if k in palette or True}
    styles.COLORS = {
        'primary': palette['primary'],
        'primary_dark': palette['primary_dark'],
        'primary_light': palette['primary_light'],
        'accent': palette['error'],
        'bg_main': palette['bg_main'],
        'bg_card': palette['bg_card'],
        'text_primary': palette['text_primary'],
        'text_secondary': palette['text_secondary'],
        'border': palette['border'],
        'status_new': palette['status_new'],
        'status_new_bg': palette['status_new_bg'],
        'status_progress': palette['status_progress'],
        'status_progress_bg': palette['status_progress_bg'],
        'status_review': palette['status_review'],
        'status_review_bg': palette['status_review_bg'],
        'status_done': palette['status_done'],
        'status_done_bg': palette['status_done_bg'],
    }

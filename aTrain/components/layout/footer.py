from importlib.resources import files
from pathlib import Path
from typing import cast

from nicegui import ui
from aTrain.utils.i18n import tr

STATIC_DIR = Path(__file__).parents[2] / "static" / "images"
BANDAS_LOGO = STATIC_DIR / "Bandas_Logo.svg"
ILLZACH_LOGO = STATIC_DIR / "Illzach_Logo.svg"
BANDAS_LINK = "https://github.com/JuergenFleiss/aTrain"


def footer():
    footer_classes = "bg-white justify-between items-center p-10"
    with ui.footer(wrap=False, fixed=False).classes(footer_classes):
        with ui.row().classes("items-center gap-6"):
            ui.image(BANDAS_LOGO).props("height=50px width=150px fit=contain")
            ui.image(ILLZACH_LOGO).props("height=50px width=100px fit=contain")
        with ui.column(align_items="end").classes("gap-0"):
            ui.label(tr("fork_text_1")).classes("text-black text-xs")
            ui.label(tr("fork_text_2")).classes("text-black text-xs")
            ui.link(tr("original_project"), target=BANDAS_LINK, new_tab=True).classes("text-[10px] text-gray-500")

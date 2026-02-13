from importlib.resources import files
from pathlib import Path
from typing import cast

from nicegui import ui

from aTrain.version import __version__

from aTrain.utils.i18n import tr, get_lang, set_lang

STATIC_DIR = Path(__file__).parents[2] / "static" / "images"
ATRAIN_LOGO = STATIC_DIR / "logo.svg"
GITHUB_LOGO = STATIC_DIR / "github.svg"
GITHUB_LINK = "https://github.com/jerome00253/aTrain"


def header(drawer_handle: ui.drawer):
    # Detect logo (check custom first)
    from aTrain_core.globals import ATRAIN_DIR
    import os
    
    logo_src = f"/static/images/logo.svg?v={__version__}"
    custom_dir = ATRAIN_DIR / "custom_assets"
    
    # Check for custom logos in order of preference
    for ext in ['svg', 'png', 'jpg', 'jpeg', 'webp']:
        custom_file = custom_dir / f"logo.{ext}"
        if custom_file.exists():
            # Use mtime for cache busting to allow live updates without rebuild
            mtime = os.path.getmtime(custom_file)
            logo_src = f"/static/custom/logo.{ext}?v={mtime}"
            break

    with ui.header().classes("bg-white justify-between items-center px-10"):
        with ui.row().classes("items-center"):
            with ui.button().classes("lt-md") as menu_button:
                menu_button.props("color=white text-color=black icon=menu flat")
                menu_button.on_click(lambda: drawer_handle.toggle())
            ui.image(logo_src).props(
                "height=30px width=80px fit=contain"
            )
        
        with ui.row().classes("items-center gap-4"):
            # Language Switcher
            current_lang = get_lang()
            with ui.button_group().props("unelevated outline size=sm"):
                btn_fr = ui.button("FR", on_click=lambda: (set_lang("fr"), ui.navigate.reload()))
                btn_en = ui.button("EN", on_click=lambda: (set_lang("en"), ui.navigate.reload()))
                if current_lang == "fr":
                    btn_fr.props("color=dark")
                else:
                    btn_en.props("color=dark")

            with ui.link(target=GITHUB_LINK, new_tab=True):
                ui.image(GITHUB_LOGO).props("height=25px width=25px fit=contain")

from nicegui import ui
from aTrain.layouts.base import base_layout
from aTrain.utils.i18n import tr

AUTHORS = ["Armin Haberl", "Jürgen Fleiß", "Dominik Kowald", "Stefan Thalmann"]
DEVELOPERS = ["LINHER Jérôme", "Kankowsky Patrice"]
MAIL = "mailto:jerome0025@gmail.com"
LICENSE = "https://github.com/jerome00253/aTrain/blob/master/LICENSE"


@ui.page("/about")
def page():
    with base_layout():
        ui.label(tr("about_title")).classes("text-lg text-dark font-bold")
        ui.separator()
        with ui.element("div").classes("grid grid-cols-1 md:grid-cols-2 gap-4 w-full"):
            with ui.column().classes("gap-0"):
                ui.label(tr("initial_authors")).classes("font-bold")
                [ui.label(author) for author in AUTHORS]
            with ui.column().classes("gap-0"):
                ui.label(tr("fork_developer")).classes("font-bold")
                [ui.label(developer) for developer in DEVELOPERS]
        ui.separator()
        ui.label(tr("disclaimer"))
        ui.separator()
        with ui.element("div").classes("grid grid-cols-1 md:grid-cols-2 gap-4 w-full"):
            with ui.link(target=MAIL, new_tab=True):
                btn_mail = ui.button(f"📧 {tr('contact')} (Mail)", color="gray-100")
                btn_mail.props("text-color=dark no-caps unelevated")
                btn_mail.classes("w-full")
            with ui.link(target=LICENSE, new_tab=True):
                btn_license = ui.button(f"📃 {tr('license')}", color="gray-100")
                btn_license.props("text-color=dark no-caps unelevated")
                btn_license.classes("w-full")

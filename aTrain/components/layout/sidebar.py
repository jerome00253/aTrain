from nicegui import ui
from aTrain.utils.i18n import tr


def sidebar():
    with ui.left_drawer().classes("bg-gray-100") as drawer_handle:
        nav_button(icon="🎧", text=tr("transcribe"), path="/")
        nav_button(icon="💾", text=tr("archive"), path="/archive")
        nav_button(icon="🧮", text=tr("models"), path="/models")
        nav_button(icon="📖", text=tr("faq"), path="/faq")
        ui.separator()
        nav_button(icon="💡", text=tr("about"), path="/about")
    return drawer_handle


def nav_button(icon: str, text: str, path: str):
    is_current_page = ui.context.client.page.path == path
    button_color = "gray-200" if is_current_page else "white"
    with ui.link(target=path).classes("w-full"):
        with ui.button(color=button_color) as nav_item:
            nav_item.props("text-color=black align=left flat no-caps")
            nav_item.classes("w-full rounded-lg")
            ui.label(icon).classes("text-base font-medium mr-4")
            ui.label(text).classes("text-base font-medium")

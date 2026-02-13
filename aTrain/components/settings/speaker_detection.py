from nicegui import ui, app
from aTrain.utils.i18n import tr


def input_speaker_detection():
    with ui.column().classes("gap-2"):
        ui.label(tr("speaker_detection")).classes("font-bold text-dark text-md")
        ui.separator()
        input = ui.switch(tr("speaker_detection"))
        input.props("color=dark")
    input.bind_value(app.storage.general, "speaker_detection")

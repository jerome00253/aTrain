from nicegui import app, ui
from aTrain.utils.i18n import tr


def input_speaker_count():
    with ui.column().classes("gap-2") as column:
        ui.label(tr("num_speakers")).classes("font-bold text-dark text-md")
        ui.separator()
        input = ui.number(min=1, placeholder=tr("detect_automatically"))
        input.classes("w-full")
        input.props("filled bg-color=gray-100 color=dark clearable")

    input.bind_value(app.storage.general, "speaker_count")
    column.bind_visibility(app.storage.general, "speaker_detection")

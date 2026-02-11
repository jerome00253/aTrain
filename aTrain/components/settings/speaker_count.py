from nicegui import app, ui


def input_speaker_count():
    with ui.column().classes("gap-2") as column:
        ui.label("Number of Speakers").classes("font-bold text-dark text-md")
        ui.separator()
        input = ui.number(min=1, placeholder="Detect automatically")
        input.classes("w-full")
        input.props("filled bg-color=gray-100 color=dark clearable")

    input.bind_value(app.storage.general, "speaker_count")
    column.bind_visibility(app.storage.general, "speaker_detection")

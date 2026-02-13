from aTrain_core.settings import ComputeType
from nicegui import ElementFilter, app, ui
from aTrain.utils.i18n import tr


def advanced_settings(open: bool):
    with ui.dialog(value=open) as dialog, ui.card() as card:
        dialog.props("position=right full-height").classes("[&>*]:p-0")
        card.props("square").classes("w-72 xl:w-96 p-6 gap-6")
        ui.label(tr("advanced_settings")).classes("text-lg text-dark font-bold")
        input_gpu()
        input_compute_type()
        input_temperature()
        input_initial_prompt()
        btn = ui.button(tr("ok"), color="dark").props("unelevated no-caps")
        btn.on_click(dialog.close)
        dialog.on("hide", dialog.delete)


def input_gpu():
    from torch import cuda  # Lazy import for improved startup speed

    state = app.storage.general
    tooltip = tr("gpu_tooltip")
    with ui.column().classes("w-full gap-2"):
        with ui.row(align_items="center").classes("w-full justify-between"):
            ui.label(tr("gpu_acceleration")).classes("font-bold text-dark")
            ui.icon("info_outline", size="sm", color="grey").tooltip(tooltip)
        ui.separator()
        if cuda.is_available():
            switch = ui.switch("GPU", value=True).props("color=dark")
        else:
            switch = ui.switch("GPU", value=False).props("color=dark disable")
            state["GPU"] = False
    switch.bind_value(state, "GPU")
    switch.on_value_change(set_compute_options)


def input_compute_type():
    state = app.storage.general
    tooltip = tr("compute_tooltip")
    with ui.column().classes("w-full gap-2"):
        with ui.row(align_items="center").classes("w-full justify-between"):
            ui.label(tr("compute_type")).classes("font-bold text-dark")
            ui.icon("info_outline", size="sm", color="grey").tooltip(tooltip)
        ui.separator()
        value = state.get("compute_type") or ComputeType.INT8.value
        select = ui.select(options=[x.value for x in ComputeType], value=value)
        select.props("filled bg-color=gray-100 color=dark").classes("w-full")
        select.bind_value(state, "compute_type").mark("select_compute")
    set_compute_options()


def input_temperature():
    with ui.column().classes("w-full gap-2"):
        ui.label(tr("temperature")).classes("font-bold text-dark")
        ui.separator()
        number = ui.number(min=0.0, max=1.0, step=0.1, precision=1, placeholder=tr("auto"))
        number.props("filled bg-color=gray-100 color=dark clearable").classes("w-full")
    number.bind_value(app.storage.general, "temperature_override")  # <- New state name

    # Fix wrong default setting from version 1.4.0, TODO: Revert state name to "temperature" in upcoming releases
    app.storage.general["temperature"] = None


def input_initial_prompt():
    with ui.column().classes("w-full gap-2"):
        ui.label(tr("initial_prompt")).classes("font-bold text-dark")
        ui.separator()
        textarea = ui.textarea(placeholder=tr("placeholder_prompt"))
        textarea.props("color=dark autogrow clearable").classes("w-full")
    textarea.bind_value(app.storage.general, "initial_prompt")


def set_compute_options():
    state = app.storage.general
    options = list(map(str, ComputeType)) if state["GPU"] else [ComputeType.INT8.value]
    new_value = ComputeType.INT8.value if not state["GPU"] else state["compute_type"]
    for select in ElementFilter(marker="select_compute", kind=ui.select):
        select.set_options(options, value=new_value)

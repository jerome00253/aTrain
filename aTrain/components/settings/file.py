from aTrain_core.settings import load_formats
from nicegui import ui
from aTrain.utils.i18n import tr


class CustomUpload(ui.upload):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on("added", self.set_added)
        self.set_select()

    def pick_files(self):
        self.reset()
        self.set_select()
        self.run_method("pickFiles")

    def upload(self):
        self.run_method("upload")

    def set_added(self):
        self.file_text = f"1 {tr('file_added')}"
        self.file_icon = "file_present"

    def set_select(self):
        self.file_text = tr("select_file")
        self.file_icon = "attach_file"


def input_file() -> CustomUpload:
    allowed_files = "".join(x for x in str(load_formats()) if x not in "[]'")
    uploader = CustomUpload().classes("hidden")
    uploader.props(f"accept='{allowed_files}'")

    with ui.column().classes("gap-2"):
        ui.label(tr("select_file")).classes("font-bold text-dark text-md")
        ui.separator()
        with ui.button() as select_button:
            select_button.props("color=gray-100 text-color=dark align=left")
            select_button.props("unelevated no-caps :ripple=false")
            select_button.classes("w-full h-full")

    select_button.bind_text(uploader, "file_text")
    select_button.bind_icon(uploader, "file_icon")
    select_button.on_click(uploader.pick_files)

    return uploader

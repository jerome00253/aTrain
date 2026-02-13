from nicegui import ui

from aTrain.components.dialogs.delete import dialog_delete
from aTrain.layouts.base import base_layout
from aTrain.utils.archive import delete_transcription as delete
from aTrain.utils.archive import open_file_directory as show
from aTrain.utils.archive import read_archive
from aTrain.utils.i18n import tr

@ui.page("/archive")
def page():
    transcriptions = read_archive()

    with base_layout():
        with ui.row().classes("justify-between w-full"):
            ui.label(tr("archive")).classes("text-lg text-dark font-bold")
            with ui.row():
                btn_show_all = ui.button(tr("show_all"), color="dark")
                btn_show_all.props("size=0.8rem unelevated no-caps")
                btn_show_all.on_click(lambda: show("all"))

                btn_del_all = ui.button(tr("delete_all"), color="gray-100")
                btn_del_all.props("size=0.8rem unelevated no-caps")
                btn_del_all.on_click(dialog_delete)

        with ui.list().classes("w-full").props("separator"):
            with ui.item():
                with ui.grid(columns="minmax(0, 60px) 1fr 1fr 1fr") as grid:
                    grid.classes("w-full text-grey text-xs items-end")
                    ui.label("#")
                    ui.label(tr("date"))
                    ui.label(tr("input"))
                    ui.label(tr("actions"))
            for i, transcription in enumerate(transcriptions):
                with ui.item().classes("hover:bg-gray-100"):
                    with ui.grid(columns="minmax(0, 60px) 1fr 1fr 1fr") as grid:
                        grid.classes("w-full items-center")
                        ui.label(str(i + 1)).classes("text-medium")
                        ui.label(transcription["timestamp"]).classes("font-light")
                        ui.label(transcription["filename"]).classes("font-light")
                        with ui.row().classes("gap-2 items-center"):
                            btn_open = ui.button(icon="visibility", color="blue-6")
                            btn_open.props(f'no-caps size=0.7rem unelevated title="{tr("detail")}"')
                            btn_open.on_click(lambda t=transcription: ui.navigate.to(f"/viewer/{t['file_id']}"))

                            # Download dropdown
                            with ui.button(icon="download", color="green-6").props('no-caps size=0.7rem unelevated title="Download"') as btn_dl:
                                with ui.menu() as menu:
                                    ui.menu_item("JSON", on_click=lambda t=transcription: ui.download(f"/transcriptions/{t['file_id']}/transcription.json"))
                                    ui.menu_item("SRT", on_click=lambda t=transcription: ui.download(f"/transcriptions/{t['file_id']}/transcription.srt"))
                                    ui.menu_item("TXT", on_click=lambda t=transcription: ui.download(f"/transcriptions/{t['file_id']}/transcription.txt"))
                                    ui.menu_item("Timestamps", on_click=lambda t=transcription: ui.download(f"/transcriptions/{t['file_id']}/transcription_timestamps.txt"))
                                    ui.menu_item("MAXQDA", on_click=lambda t=transcription: ui.download(f"/transcriptions/{t['file_id']}/transcription_maxqda.txt"))

                            btn_delete = ui.button(icon="delete", color="red-6")
                            btn_delete.props(f'no-caps size=0.7rem unelevated title="{tr("delete")}"')
                            btn_delete.on_click(
                                lambda t=transcription: (delete(t["file_id"]), ui.navigate.reload())
                            )

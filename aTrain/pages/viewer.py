import os
from pathlib import Path
from nicegui import ui, app
from aTrain.layouts.base import base_layout
from aTrain_core.globals import TRANSCRIPT_DIR, METADATA_FILENAME
from aTrain.utils.archive import open_file_directory as download_zip
from aTrain.utils.i18n import tr
import yaml

@ui.page("/viewer/{file_id}")
def page(file_id: str):
    directory = os.path.join(TRANSCRIPT_DIR, file_id)
    
    if not os.path.exists(directory):
        with base_layout():
            ui.label("Transcription not found").classes("text-h4 text-red")
            ui.button(tr("back_to_archive"), on_click=lambda: ui.navigate.to("/archive")).props("unelevated no-caps")
        return

    # Load metadata if exists
    metadata = {}
    metadata_path = os.path.join(directory, METADATA_FILENAME)
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

    # Try to load transcription content
    # Order of preference: .srt, .txt
    content = ""
    file_type = ""
    for ext in [".srt", ".txt"]:
        content_path = os.path.join(directory, f"transcription{ext}")
        if os.path.exists(content_path):
            with open(content_path, "r", encoding="utf-8") as f:
                content = f.read()
                file_type = ext[1:].upper()
            break
            
    if not content:
        content = "No transcription content found."

    with base_layout():
        with ui.row().classes("justify-between w-full items-center"):
            ui.label(tr("view_transcription")).classes("text-lg text-dark font-bold")
            with ui.row():
                ui.button(tr("back_to_archive"), on_click=lambda: ui.navigate.to("/archive")).props("outline no-caps size=sm")
                ui.button(tr("download_transcription"), on_click=lambda: download_zip(file_id)).props("unelevated no-caps size=sm color=dark")

        with ui.card().classes("w-full q-pa-md"):
            with ui.row().classes("w-full gap-4"):
                with ui.column().classes("gap-0"):
                    ui.label(tr("date")).classes("text-xs text-grey")
                    ui.label(metadata.get("timestamp", file_id[:20])).classes("text-sm")
                with ui.column().classes("gap-0"):
                    ui.label(tr("input")).classes("text-xs text-grey")
                    ui.label(metadata.get("filename", file_id[20:] or "n/a")).classes("text-sm")
                with ui.column().classes("gap-0"):
                    ui.label(tr("file_id")).classes("text-xs text-grey")
                    ui.label(file_id).classes("text-sm")
                with ui.column().classes("gap-0"):
                    ui.label("Format").classes("text-xs text-grey")
                    ui.label(file_type).classes("text-sm")

        ui.separator().classes("my-4")

        # Scrollable area for the text
        with ui.scroll_area().classes("w-full border p-4 bg-gray-50").style("height: 60vh"):
            ui.markdown(f"```text\n{content}\n```").classes("w-full")

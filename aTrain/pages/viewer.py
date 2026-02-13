import os
import re
import json
import yaml
from pathlib import Path
from nicegui import ui, app
from aTrain.layouts.base import base_layout
from aTrain_core.globals import TRANSCRIPT_DIR, METADATA_FILENAME
from aTrain.utils.archive import open_file_directory as download_zip
from aTrain.utils.i18n import tr

class TranscriptionEditor:
    def __init__(self, file_id: str):
        self.file_id = file_id
        self.directory = os.path.join(TRANSCRIPT_DIR, file_id)
        self.data = self._load_json()
        self.segments = self.data.get("segments", [])
        self.editing = False
        self.audio_player = None

    def _load_json(self):
        path = os.path.join(self.directory, "transcription.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"segments": []}

    def _format_timestamp(self, seconds: float):
        td = float(seconds)
        h = int(td // 3600)
        m = int((td % 3600) // 60)
        s = int(td % 60)
        ms = int((td % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def _format_short_timestamp(self, seconds: float):
        td = float(seconds)
        h = int(td // 3600)
        m = int((td % 3600) // 60)
        s = int(td % 60)
        return f"[{h:02d}:{m:02d}:{s:02d}]"

    def save(self):
        try:
            # 1. Update and save JSON
            json_path = os.path.join(self.directory, "transcription.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)

            # 2. Generate and save SRT
            srt_path = os.path.join(self.directory, "transcription.srt")
            srt_content = []
            for i, seg in enumerate(self.segments):
                start = self._format_timestamp(seg['start'])
                end = self._format_timestamp(seg['end'])
                srt_content.append(f"{i+1}\n{start} --> {end}\n{seg['text'].strip()}")
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write("\n\n".join(srt_content) + "\n")

            # 3. Generate and save TXT
            txt_path = os.path.join(self.directory, "transcription.txt")
            txt_content = "\n".join([seg['text'].strip() for seg in self.segments])
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(txt_content + "\n")

            # 4. Generate and save Timestamps TXT
            ts_path = os.path.join(self.directory, "transcription_timestamps.txt")
            ts_content = [f"Transcription for {self.file_id}\n"]
            last_speaker = None
            for seg in self.segments:
                speaker = seg.get('speaker', 'Unknown')
                if speaker != last_speaker:
                    ts_content.append(f"\n{speaker}")
                    last_speaker = speaker
                ts_content.append(f"{self._format_short_timestamp(seg['start'])} - {seg['text'].strip()}")
            with open(ts_path, "w", encoding="utf-8") as f:
                f.write("\n".join(ts_content) + "\n")

            # 5. Generate and save MAXQDA TXT (similar to timestamps but slightly different header/spacing often)
            mq_path = os.path.join(self.directory, "transcription_maxqda.txt")
            with open(mq_path, "w", encoding="utf-8") as f:
                f.write("\n".join(ts_content) + "\n")

            ui.notify(tr("save_success"), type='positive', duration=4)
            self.editing = False
            ui.timer(1.5, ui.navigate.reload, once=True)
        except Exception as e:
            ui.notify(f"Error saving: {e}", type='negative', duration=0)
            print(f"DEBUG: Save failed: {traceback.format_exc()}")

    def seek_audio(self, seconds: float):
        if self.audio_player:
            self.audio_player.seek(seconds)
            self.audio_player.play()

@ui.page("/viewer/{file_id}")
def page(file_id: str):
    directory = os.path.join(TRANSCRIPT_DIR, file_id)
    if not os.path.exists(directory):
        with base_layout():
            ui.label("Transcription not found").classes("text-h4 text-red")
            ui.button(tr("back_to_archive"), on_click=lambda: ui.navigate.to("/archive")).props("unelevated no-caps")
        return

    metadata = {}
    metadata_path = os.path.join(directory, METADATA_FILENAME)
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

    editor = TranscriptionEditor(file_id)
    
    # Check for audio file
    audio_src = None
    for ext in ['.mp3', '.wav', '.m4a', '.ogg', '.MP3', '.WAV']:
        audio_path = os.path.join(directory, f"source_audio{ext}")
        if os.path.exists(audio_path):
            audio_src = f"/transcriptions/{file_id}/source_audio{ext}"
            break

    with base_layout():
        with ui.row().classes("justify-between w-full items-center"):
            ui.label(tr("view_transcription")).classes("text-lg text-dark font-bold")
            with ui.row():
                ui.button(tr("back_to_archive"), on_click=lambda: ui.navigate.to("/archive")).props("outline no-caps size=sm")
                ui.button(tr("download_transcription"), on_click=lambda: download_zip(file_id)).props("unelevated no-caps size=sm color=dark")

        with ui.card().classes("w-full q-pa-md mb-4"):
            with ui.row().classes("w-full justify-between items-start"):
                with ui.row().classes("gap-4"):
                    with ui.column().classes("gap-0"):
                        ui.label(tr("date")).classes("text-xs text-grey")
                        ui.label(metadata.get("timestamp", file_id[:20])).classes("text-sm")
                    with ui.column().classes("gap-0"):
                        ui.label(tr("input")).classes("text-xs text-grey")
                        ui.label(metadata.get("filename", file_id[20:] or "n/a")).classes("text-sm")
                
                if audio_src:
                    editor.audio_player = ui.audio(audio_src).classes("w-64")

        with ui.row().classes("w-full mb-4") as action_row:
            edit_btn = ui.button(tr("edit"), icon="edit").props("unelevated no-caps size=sm")
            save_btn = ui.button(tr("save"), icon="save", on_click=editor.save).props("unelevated no-caps size=sm color=green")
            save_btn.set_visibility(False)
            cancel_btn = ui.button(tr("cancel"), icon="cancel", on_click=lambda: ui.navigate.reload()).props("outline no-caps size=sm color=red")
            cancel_btn.set_visibility(False)

        container = ui.column().classes("w-full border p-4 bg-gray-50 mb-8")
        
        def render_view():
            container.clear()
            with container:
                with ui.scroll_area().style("height: 60vh"):
                    last_speaker = None
                    for seg in editor.segments:
                        speaker = seg.get('speaker', 'SPEAKER_00')
                        if speaker != last_speaker:
                            ui.label(speaker).classes("text-xs font-bold mt-2 text-primary")
                            last_speaker = speaker
                        
                        with ui.row().classes("w-full items-start gap-2 mb-1 no-wrap hover:bg-gray-100 p-1 rounded"):
                             if audio_src:
                                 ui.button(icon="play_arrow", on_click=lambda s=seg: editor.seek_audio(s['start'])).props("flat round size=xs")
                             ui.label(editor._format_timestamp(seg['start'])).classes("text-xs text-grey italic w-24 flex-shrink-0 mt-1")
                             ui.label(seg['text']).classes("text-sm break-words flex-grow")

        def render_edit():
            container.clear()
            with container:
                with ui.scroll_area().style("height: 65vh").classes("w-full"):
                    for seg in editor.segments:
                        with ui.row().classes("w-full items-start gap-2 mb-2 no-wrap p-1"):
                            if audio_src:
                                ui.button(icon="play_arrow", on_click=lambda s=seg: editor.seek_audio(s['start'])).props("flat round size=xs")
                            with ui.column().classes("w-24 flex-shrink-0"):
                                ui.label(seg.get('speaker', 'SPEAKER_00')).classes("text-xs font-bold")
                                ui.label(editor._format_timestamp(seg['start'])).classes("text-xs text-grey")
                            ui.textarea(value=seg['text'], on_change=lambda e, s=seg: s.update(text=e.value)).props("autogrow borderless").classes("flex-grow bg-white p-2 border rounded text-sm shadow-sm")

        def toggle_edit():
            editor.editing = not editor.editing
            edit_btn.set_visibility(not editor.editing)
            save_btn.set_visibility(editor.editing)
            cancel_btn.set_visibility(editor.editing)
            if editor.editing:
                render_edit()
            else:
                render_view()

        edit_btn.on_click(toggle_edit)
        render_view()

import os
from importlib.resources import files
from pathlib import Path
from typing import cast
from unittest.mock import patch

from aTrain_core.globals import ATRAIN_DIR, REQUIRED_MODELS
from aTrain_core.load_resources import get_model
from typer import Option, Typer
from typing_extensions import Annotated
from contextlib import contextmanager

# Try to import wakepy, but don't crash if missing
try:
    from wakepy import keep as _real_keep
except ImportError:
    _real_keep = None

class RobustKeep:
    @contextmanager
    def running(self):
        if _real_keep:
            try:
                # Try to acquire the wake lock
                with _real_keep.running():
                    yield
                return
            except Exception as e:
                # If it fails (e.g. in Docker), log it and continue normally
                print(f"⚠️ Wake lock disabled (running in headless/container mode): {e}")
        
        # Fallback: just yield control so the app runs without lock
        yield

keep = RobustKeep()

with patch.dict(os.environ, NICEGUI_STORAGE_PATH=str(ATRAIN_DIR / "settings")):
    from nicegui import app, ui

    from aTrain.pages import about, archive, faq, models, transcribe, viewer  # noqa

    # Register static files directory
    # Default static (bundled in package)
    pkg_static_dir = str(files("aTrain") / "static")
    
    # Optional custom static (in persistent /data for live updates)
    from aTrain_core.globals import ATRAIN_DIR, TRANSCRIPT_DIR
    custom_static_dir = ATRAIN_DIR / "custom_assets"
    
    if custom_static_dir.exists():
        # Serve custom assets first so they can override bundled ones
        app.add_static_files("/static/custom", str(custom_static_dir))
        # Note: We keep /static for the bundled ones to ensure CSS/JS works
        # but we'll instruct the user to use /static/custom for live logos
        static_dir = pkg_static_dir
    else:
        static_dir = pkg_static_dir

    app.add_static_files("/static", static_dir)
    app.add_static_files("/transcriptions", TRANSCRIPT_DIR)

cli = Typer(help="CLI for aTrain.")


@cli.command()
def init():
    """Download all required model for aTrain."""
    for model in REQUIRED_MODELS:
        get_model(model=model)


@cli.command()
def start(
    native: Annotated[bool, Option(help="Run in a native window")] = True,
    host: Annotated[str, Option(help="Host to run the web server on")] = "127.0.0.1",
    port: Annotated[int, Option(help="Port to run the web server on")] = 8080,
    reload: Annotated[bool, Option(help="Reload on code change")] = False,
):
    """Start aTrain."""
    print("Running aTrain")
    with keep.running():
        ui.run(
            native=native,
            host=host,
            port=port,
            reload=reload,
            title="aTrain",
            storage_secret="atrain_secret_key",  # Enabled for i18n preference storage
            favicon=cast(Path, files("aTrain") / "static" / "favicon.ico"),
            window_size=(1280, 720) if native else None,
            proxy_headers=True,
            forwarded_allow_ips="*",
        )

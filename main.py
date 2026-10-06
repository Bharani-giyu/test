import os
import secrets

from nicegui import app, ui

from src.dashboard_app import build_dashboard


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/readyz")
async def readyz():
    return {"status": "ok"}


build_dashboard()


if __name__ == "__main__":
    ui.run(
        title="Operations Dashboard",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
        reload=False,
        storage_secret=os.environ.get("NICEGUI_STORAGE_SECRET") or secrets.token_urlsafe(32),
    )

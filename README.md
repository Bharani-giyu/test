# KPI Dashboard Starter

A small NiceGUI dashboard with a region filter, KPI cards, and a simple trend chart. It is designed to be a compact Azure App Service starter that runs locally and exposes health endpoints for platform probes.

## Local run

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python main.py
   ```
4. Open the app in your browser at http://localhost:8080

## Environment variables

`.env.sample` documents the settings; the app does not load `.env` files automatically. Set these in your shell or hosting platform:

- `PORT`: HTTP port used by the app.
- `NICEGUI_STORAGE_SECRET`: Stable secret for NiceGUI browser storage. If unset, a random secret is generated at startup; set this explicitly in Azure so it remains stable across restarts.

In PowerShell, for example:

```powershell
$env:PORT = "8080"
$env:NICEGUI_STORAGE_SECRET = "replace-with-a-long-random-value"
python main.py
```

## Endpoints

- `/healthz` returns `{"status": "ok"}`
- `/readyz` returns `{"status": "ok"}`

## Deploy to Azure App Service from GitHub

1. Push this project to a GitHub repository.
2. In Azure, create a **Web App** with **Code** publish, **Python 3.12** on Linux, and a **Basic B1** plan or higher.
3. Open the Web App's **Deployment Center**, choose **GitHub** and **GitHub Actions**, then select the repository and branch. Save the configuration; Azure creates a workflow under `.github/workflows/`.
4. In **Settings > Environment variables** (or **Configuration > Application settings**), add:
   - `PORT` = `8080`
   - `NICEGUI_STORAGE_SECRET` = a long random value (generate one with `python -c "import secrets; print(secrets.token_urlsafe(48))"`).
5. Set the Web App startup command to `python main.py`, save, and restart the app.
6. Commit Azure's generated workflow to GitHub. Future pushes to the selected branch will deploy automatically.

Keep the storage secret in Azure App Service settings or a GitHub/Azure secret store; never commit a real secret to the repository.

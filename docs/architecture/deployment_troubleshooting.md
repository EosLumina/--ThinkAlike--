# Deployment & Installation Troubleshooting Guide

## 1. Introduction

This guide addresses common issues encountered during the local installation process and deployment to the Render cloud
platform. Use this guide when you encounter errors or unexpected behavior during setup or deployment.

* --

## 2. Local Installation Issues

### 2.1 Backend (Python/FastAPI)

1. **Issue:** `ModuleNotFoundError: No module named 'xyz'`

    * **Fix:** Activate the virtual environment (`source venv/bin/activate` or `.\venv\Scripts\Activate.ps1`) and run

`pip install -r requirements.txt`.

1. **Issue:** Database Connection Error (SQLite `unable to open database file`)

    * **Fix:** Verify `DATABASE_URL` in `.env` (e.g., `sqlite:///instance/thinkalike.db`). Ensure the `instance/`

directory exists with write permissions.

1. **Issue:** `uvicorn` starts but `/docs` or API endpoints give 404.

    * **Fix:** Check `uvicorn main:app` reference is correct. Ensure routers are included in `main.py`.

* --

## 3. Render Deployment Issues

1. **Issue:** Build Fails on Render.

    * **Fix:** Check Render Build Logs. Verify "Build Command" in Render settings. Ensure `requirements.txt` and

`package.json` have all dependencies.

1. **Issue:** Deploy Succeeds, App Crashes / "Application Error".

    * **Fix:** Check Render Runtime Logs. Verify environment variables like `DATABASE_URL` and `SECRET_KEY`.

* --

## 4. General Advice

* **Read Logs:** Console, terminal, and Render logs are key.

* **Consult Documentation:** Refer to the [Installation Guide](../core/installation.md) and [Deployment

Guide](../guides/implementation_guides/deployment_guide.md).

* --

## Document Details

* Title: Deployment Troubleshooting Guide

* Type: Troubleshooting Documentation

* Version: 1.0.0

## - Last Updated: 2025-04-06

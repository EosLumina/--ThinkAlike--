# Deployment & Installation Troubleshooting Guide

## 1. Introduction

This guide addresses common issues encountered during the local installation process ([`docs/core/installation.md`](../core/installation.md)) and deployment to the Render cloud platform ([`docs/guides/implementation_guides/deployment_guide.md`](../guides/implementation_guides/deployment_guide.md)). Use this guide when you encounter errors or unexpected behavior during setup or deployment.

Always check the specific error messages in your terminal, browser console (F12), or Render logs first, as they often provide the most direct clues.

---

## 2. Local Installation Issues

Common problems encountered when setting up the development environment locally.

### 2.1 Backend (Python/FastAPI)

1.  **Issue:** `ModuleNotFoundError: No module named 'xyz'`
    *   **Cause:** Python dependencies are missing, or the virtual environment is not activated.
    *   **Solution:**
        1.  Navigate to the project root directory in your terminal.
        2.  Activate the virtual environment:
            *   Windows PowerShell: `.\venv\Scripts\Activate.ps1`
            *   macOS/Linux: `source venv/bin/activate`
            *   (Your prompt should show `(venv)`).
        3.  Ensure `requirements.txt` lists all needed packages.
        4.  Run `pip install -r requirements.txt` again.

2.  **Issue:** Database Connection Error (e.g., `OperationalError: unable to open database file 'instance/thinkalike.db'` for SQLite)
    *   **Cause:** Incorrect path in `DATABASE_URL`; `instance/` directory doesn't exist or lacks write permissions; database file not created by `init_db.py`.
    *   **Solution:**
        1.  Verify the `DATABASE_URL` in your root `.env` file is correct relative to where you run `uvicorn`. For the standard setup, `sqlite:///instance/thinkalike.db` should work if run from the root.
        2.  Ensure the `instance/` directory exists in the project root. If not, create it (`mkdir instance`).
        3.  Confirm your user has write permissions for the `instance/` directory and the `thinkalike.db` file within it.
        4.  Ensure `init_db.py` and `schema.sql` exist and run `python init_db.py` (with venv activated) to create the database structure. Check for errors during its execution.

3.  **Issue:** `uvicorn main:app --reload` starts, but browsing `http://localhost:8000/docs` gives 404 Not Found.
    *   **Cause:** Incorrect application instance (`main:app`); API routers not included in `main.py`; incorrect base URL prefix.
    *   **Solution:**
        1.  Confirm `main:app` matches your main FastAPI file (`main.py`) and the app variable name (`app = FastAPI()`).
        2.  In `main.py`, check that all necessary API routers are imported (e.g., `from api.endpoints_users import router as user_router`) and included using `app.include_router(user_router, prefix="/api/v1", tags=["Users"])`. Verify the `/api/v1` prefix is consistently used.
        3.  Check the specific endpoint decorator paths in your router files (e.g., `@router.get("/users/{userId}")`).

4.  **Issue:** Frontend receives CORS errors when calling the local backend API.
    *   **Cause:** Backend `CORSMiddleware` is missing or doesn't include `http://localhost:3000` (or your frontend's dev port) in its allowed origins.
    *   **Solution:**
        1.  In `main.py`, ensure `CORSMiddleware` is imported and added to the `app`.
        2.  Verify the `origins` list includes `"http://localhost:3000"`.
            ```python
            from fastapi.middleware.cors import CORSMiddleware
            # ... other imports
            app = FastAPI()
            origins = ["http://localhost:3000", # Add others if needed
                      ]
            app.add_middleware(CORSMiddleware, allow_origins=origins, ...)
            # ... include routers etc.
            ```

### 2.2 Frontend (Node/React)

1.  **Issue:** `npm install` (or `yarn install`) fails with `ERESOLVE` errors or similar dependency conflicts.
    *   **Cause:** Node.js/npm version mismatches between project requirements and your installed versions; conflicts between different package dependencies.
    *   **Solution:**
        1.  Check project documentation or `package.json` (`engines` field) for the required Node.js version. Use `nvm` (Node Version Manager) if possible to switch to the correct version (`nvm install <version>`, `nvm use <version>`).
        2.  Delete `node_modules` and `package-lock.json` (or `yarn.lock`).
        3.  Try installing again: `npm install`.
        4.  As a last resort (understand the risks), try: `npm install --legacy-peer-deps`.

2.  **Issue:** `npm start` fails with `ERR_OSSL_EVP_UNSUPPORTED` error.
    *   **Cause:** Common with newer Node.js versions (v17+) interacting with older build tools/dependencies that use outdated OpenSSL providers.
    *   **Solution:** Set the `NODE_OPTIONS` environment variable before running `npm start`:
        *   PowerShell: `Set-Item -Path Env:NODE_OPTIONS -Value "--openssl-legacy-provider"; npm start` (or set globally for the session)
        *   macOS/Linux: `export NODE_OPTIONS=--openssl-legacy-provider && npm start`

3.  **Issue:** `npm start` runs, browser opens, but shows "Cannot GET /" or similar error, or a blank page.
    *   **Cause:** Build process error; routing issue; missing `index.html` in `public/`; incorrect base path configuration.
    *   **Solution:**
        1.  Check the terminal where `npm start` is running for any compilation errors. Fix them first.
        2.  Ensure you have a basic `public/index.html` file.
        3.  Verify your React Router setup (`BrowserRouter`, Routes, etc.) in `src/App.js` or similar is correct.
        4.  Check the browser console (F12) for JavaScript errors.

4.  **Issue:** Frontend loads but cannot fetch data from the backend API (shows loading spinners indefinitely, network errors in console).
    *   **Cause:** Backend server isn't running; `REACT_APP_BACKEND_URL` in `frontend/.env` is incorrect; CORS error (see Backend section 2.1.4).
    *   **Solution:**
        1.  Make sure the FastAPI backend (`uvicorn`) is running in a separate terminal.
        2.  Verify `frontend/.env` has `REACT_APP_BACKEND_URL=http://localhost:8000` (or your correct backend port). Remember to restart the frontend (`npm start`) after changing `.env` files.
        3.  Check the browser console Network tab for failed requests. Look for CORS errors or 404s indicating the backend endpoint wasn't found.

---

## 3. Render Deployment Issues

Common problems encountered when deploying to Render.

1.  **Issue:** Build Fails on Render.
    *   **Cause:** Incorrect "Build Command" in Render settings; missing production dependencies in `requirements.txt` / `package.json`; incorrect Python/Node version selected on Render; insufficient resources (Free tier limits).
    *   **Solution:**
        1.  **Check Render Logs:** Go to your service on Render -> "Events" or "Logs" tab. Examine the build logs for the specific error message.
        2.  **Verify Build Command:** Ensure the command in Render settings is correct (e.g., `pip install -r requirements.txt` for backend; `npm install && npm run build` for frontend).
        3.  **Check Dependencies:** Ensure *all* dependencies needed for *production* (not just development) are listed in the respective files and committed.
        4.  **Check Runtimes:** Verify the Python/Node version selected under "Settings" -> "Environment" on Render matches project requirements.
        5.  **Resource Limits:** Complex builds might exceed Free tier memory/CPU limits. Try upgrading temporarily or optimizing your build process.

2.  **Issue:** Deployment Succeeds, but Application Crashes / "Application Error".
    *   **Cause:** Missing/incorrect Environment Variables on Render (especially `DATABASE_URL`, `SECRET_KEY`); database not ready or migrations failed; incorrect "Start Command"; application port binding issue.
    *   **Solution:**
        1.  **Check Runtime Logs:** Go to the "Logs" tab for your running service on Render. Look for errors immediately after startup.
        2.  **Verify Environment Variables:** Go to "Environment" tab on Render. Meticulously check *every* variable. Use Render's **Internal** Database URL for `DATABASE_URL`. Ensure `SECRET_KEY` is set. Check `PYTHON_VERSION` if needed.
        3.  **Verify Start Command:** Ensure it's correct for production (e.g., `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker` for backend, binding to Render's `$PORT`). For static sites, ensure the "Publish Directory" is correct (`frontend/build`).
        4.  **Database Migrations:** Confirm migrations ran successfully (check logs or run manually via Render Shell if needed).
        5.  **Port Binding (Backend):** Ensure your application (Uvicorn/Gunicorn) is configured to listen on host `0.0.0.0` and port `$PORT` (Render sets the `$PORT` variable automatically).

3.  **Issue:** Application Runs, but Frontend has CORS errors trying to reach Backend API.
    *   **Cause:** The deployed frontend URL (e.g., `https://thinkalike-frontend.onrender.com`) was not added to the backend's allowed CORS origins.
    *   **Solution:**
        1.  Get your exact frontend URL from the Render Static Site dashboard.
        2.  Go to your **Backend** Web Service on Render -> "Environment".
        3.  Add/Update the environment variable controlling CORS origins (e.g., `CORS_ALLOWED_ORIGINS`) to include your full frontend URL (e.g., `https://thinkalike-frontend.onrender.com`). If multiple origins, separate them as your backend code expects (often comma-separated).
        4.  Trigger a redeploy of the backend service for the environment variable change to take effect.

4.  **Issue:** Frontend Routes (React Router) other than `/` give a 404 Not Found on Render.
    *   **Cause:** The Render Static Site needs a rewrite rule to handle client-side routing.
    *   **Solution:**
        1.  Go to your Static Site settings on Render -> "Redirects/Rewrites".
        2.  Add a **Rewrite Rule**:
            *   Source: `/*`
            *   Destination: `/index.html`
            *   Action: Rewrite

---

## 4. General Advice

*   **Read the Logs:** This is the most crucial step for any issue.
*   **Check Documentation:** Refer back to `installation.md` and `deployment_guide.md`.
*   **Isolate:** Determine if the problem is frontend, backend, database, or configuration. Test components individually if possible (e.g., use `curl` or Postman to test backend API directly).
*   **Ask for Help:** If stuck, use the project's communication channels (GitHub Issues, Discord). Provide clear details: what you did, what you expected, the exact error message, relevant logs, your OS/environment.

---

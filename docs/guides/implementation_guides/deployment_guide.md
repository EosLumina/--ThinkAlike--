# Deployment Guide (render)

---

## 1. Introduction

This guide provides step-by-step instructions for deploying the ThinkAlike platform (FastAPI backend and React frontend) to the [Render](https://render.com/) cloud platform. Render offers convenient services for hosting web applications, static sites, and databases, making it a suitable choice for deploying ThinkAlike.

Following these steps assumes you have completed local development and testing as outlined in the [Installation Guide](../../core/installation.md) and [Testing and Validation Plan](../developer_guides/testing_and_validation_plan.md).

**Target Environment:** Render Cloud Platform
**Backend:** Web Service (Python/FastAPI)
**Frontend:** Static Site (React)
**Database:** Render PostgreSQL

---

## 2. Prerequisites

Before deploying, ensure you have:

1. **A Render Account:** Sign up at [render.com](https://render.com/).
2. **GitHub Repository:** Your ThinkAlike project code pushed to a GitHub repository that Render can access.
3. **Code Readiness:** Your `main` branch (or deployment branch) is stable, tested, and ready for deployment.
4. **Dependencies Defined:**
    * Backend: `requirements.txt` in the project root is up-to-date.
    * Frontend: `package.json` in the `frontend/` directory is up-to-date.
5. **(Optional but Recommended) Docker:** While not strictly required for this Render guide, having Docker knowledge helps understand containerization, which Render uses internally.

---

## 3. Backend Deployment (Render Web Service)

Deploy the FastAPI backend as a Render Web Service.

### 3.1 Create Database (Render PostgreSQL)

1. **Navigate to Render Dashboard:** Log in to your Render account.
2. **Create New PostgreSQL Database:**
    * Click "New +" -> "PostgreSQL".
    * Choose a unique name (e.g., `thinkalike-db`).
    * Select a Region close to your users.
    * Choose a plan (e.g., "Free" for initial testing, upgrade as needed).
    * Click "Create Database".
3. **Copy Connection String:** Once the database is ready, go to its page and copy the **"Internal Connection String"**. You will need this for the backend environment variables. It will look something like `postgresql://user:password@host:port/database`.

### 3.2 Create Web Service

1. **Navigate to Render Dashboard.**
2. **Create New Web Service:**
    * Click "New +" -> "Web Service".
    * Connect Your GitHub Repository: Choose "Build and deploy from a Git repository" and connect the GitHub account holding your `thinkalike_project` repository. Select the repository.
3. **Configure Service Settings:**
    * **Name:** Give your service a unique name (e.g., `thinkalike-backend`). Render will generate a default URL like `thinkalike-backend.onrender.com`.
    * **Region:** Choose the same region as your database.
    * **Branch:** Select the branch to deploy from (e.g., `main`).
    * **Root Directory:** Leave blank if `requirements.txt` and your FastAPI app (`main.py` or similar entry point) are in the project root. If your backend code is in a subdirectory (e.g., `backend/`), specify that here.
    * **Runtime:** Render should auto-detect `Python 3`. Ensure the version matches your development environment (e.g., 3.9+). You might need to specify it in environment variables if detection fails.
    * **Build Command:** Render usually detects `pip install -r requirements.txt` automatically. Verify this is correct.
    * **Start Command:** This command runs your application using a production server like Gunicorn.
        * Example: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
        * Replace `main:app` with your actual FastAPI app instance location (`filename:fastapi_app_variable`).
        * `-w 4`: Number of worker processes (adjust based on your plan).
        * `-k uvicorn.workers.UvicornWorker`: Specifies the Uvicorn worker for ASGI compatibility.
4. **Add Environment Variables (Secrets):**
    * Go to the "Environment" section for your new Web Service.
    * Add **Secret Files** for sensitive configuration if you used `.env` locally (Render doesn't directly use `.env` files in production). Create a secret file with your environment variables.
    * Alternatively, add **individual Environment Variables**:
        * `DATABASE_URL`: Paste the **Internal Connection String** copied from your Render PostgreSQL database.
        * `SECRET_KEY`: Add your Flask/FastAPI secret key (use a strong, randomly generated key).
        * `PYTHON_VERSION`: (Optional, e.g., `3.9.10`) Specify if Render doesn't detect the correct version.
        * `FRONTEND_URL`: **Leave this blank for now.** You will add the deployed frontend URL later after deploying the frontend and configuring CORS.
        * *(Add any other required environment variables like API keys)*
5. **Choose Instance Type:** Select a plan (e.g., "Free" or a paid plan for more resources).
6. **Create Web Service:** Click "Create Web Service". Render will start building and deploying your backend. Monitor the deploy logs for errors.

### 3.3 Database Migrations (If Using Alembic/Flask-Migrate)

If your application uses database migrations (e.g., with Alembic):

* **Option 1 (Manual via Shell):** Once the service is deployed, use Render's "Shell" tab for your backend service to run migration commands (e.g., `alembic upgrade head`). You'll need to activate the virtual environment first within the shell if applicable.
* **Option 2 (Startup Script):** Modify your service's Start Command or use a separate startup script (`render_startup.sh`) to automatically run migrations *before* starting the Gunicorn server. Be cautious with this approach to avoid issues during startup failures.

### 3.4 Azure Deployment Alternative

While Render is our primary recommended deployment platform, Azure offers robust services that may be preferable for teams with existing Azure experience or enterprise requirements:

1. **Azure App Service** for hosting the FastAPI backend:
   * Create an App Service Plan (Basic B1 or higher recommended)
   * Deploy from GitHub using Azure App Service Deployment Center
   * Configure environment variables in Application Settings

2. **Azure Static Web Apps** for the React frontend:
   * Connect to your GitHub repository
   * Configure build settings (build command: `npm run build`, output location: `build`)
   * Set up environment variables for API connection

3. **Azure Database for PostgreSQL** instead of Render PostgreSQL:
   * Create a managed PostgreSQL server
   * Configure firewall rules to allow connections from App Service
   * Update connection strings in App Service configuration

This alternative deployment path provides additional scaling options and integration with Azure's security and monitoring tools.

---

## 4. Frontend Deployment (Render Static Site)

Deploy the React frontend as a Render Static Site.

1. **Build Frontend Locally (Important Check):** Before deploying, ensure your frontend builds correctly:

    ```bash
    cd frontend
    npm install
    npm run build
    cd ..
    ```

    This creates the `frontend/build` directory containing the optimized static assets. Fix any build errors before proceeding.
2. **Navigate to Render Dashboard.**
3. **Create New Static Site:**
    * Click "New +" -> "Static Site".
    * Connect Your GitHub Repository: Select the same `thinkalike_project` repository.
4. **Configure Static Site Settings:**
    * **Name:** Give your site a unique name (e.g., `thinkalike-frontend`). Render will generate a URL like `thinkalike-frontend.onrender.com`.
    * **Branch:** Select the branch to deploy from (e.g., `main`).
    * **Root Directory:** Set this to `frontend`. Render needs to know where your `package.json` for the frontend is located.
    * **Build Command:** `npm install && npm run build` (This tells Render how to build your React app).
    * **Publish Directory:** Set this to `frontend/build` (This tells Render where the built static files are).
5. **Add Environment Variables:**
    * Go to the "Environment" section for your new Static Site.
    * Add **Environment Variable**:
        * `REACT_APP_BACKEND_URL`: Set this to the **full URL of your deployed backend service** on Render (e.g., `https://thinkalike-backend.onrender.com`). **Use HTTPS.**
        * *(Add any other frontend-specific build-time environment variables needed)*
6. **Create Static Site:** Click "Create Static Site". Render will start building and deploying your frontend.

### 4.1 Rewrite/Redirect Rules (for React Router)

Since React uses client-side routing (like `react-router-dom`), you need to configure Render to serve your `index.html` for any paths that don't match a static file.

1. Go to the "Redirects/Rewrites" section of your Static Site settings on Render.
2. Add a **Rewrite Rule**:
    * **Source Path:** `/*`
    * **Destination Path:** `/index.html`
    * **Action:** Rewrite

---

## 5. CORS Configuration (Backend Update)

Your backend API needs to allow requests from your deployed frontend URL.

1. **Get Frontend URL:** Note the final URL of your deployed Static Site (e.g., `https://thinkalike-frontend.onrender.com`).
2. **Update Backend CORS Settings:**
    * Open your backend code (`main.py` or wherever CORS is configured).
    * Update the `origins` list in your `CORSMiddleware` setup to include your **deployed frontend URL**.

        ```python
        # Example in main.py

        from fastapi.middleware.cors import CORSMiddleware

        origins = [
            "http://localhost:3000", # Keep for local dev

            "https://thinkalike-frontend.onrender.com", # Add your deployed frontend URL

            # Add any other origins if needed

        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        ```

3. **Commit and Push Changes:** Commit the updated CORS settings to your GitHub repository.
4. **Redeploy Backend:** Render should automatically detect the push to your deployment branch and redeploy the backend service. Monitor the deploy logs.

---

## 6. Post-Deployment Steps

1. **Testing:** Thoroughly test all features of the deployed application using the live frontend URL. Check:
    * User registration and login.
    * Profile creation/editing.
    * Matching functionality.
    * DataTraceability visualization.
    * Any community features implemented.
    * Check browser developer console for errors (especially CORS errors).
2. **Monitoring:** Utilize Render's built-in logging and metrics to monitor the health and performance of your backend service and database. Set up alerts if needed.
3. **Domain:** (Optional) Configure a custom domain for your frontend and backend services through Render's settings.

---

## 7. Troubleshooting Tips

* **Check Deploy Logs:** Render provides detailed logs for both builds and runtime. This is the first place to look for errors.
* **Environment Variables:** Double-check that all necessary environment variables (like `DATABASE_URL`, `SECRET_KEY`, `REACT_APP_BACKEND_URL`) are correctly set in the respective Render service environments and are *not* hardcoded. Remember to use the **Internal** Connection String for `DATABASE_URL` between Render services.
* **Start Command:** Ensure the command is correct and points to the right FastAPI app instance. Check runtime logs.
* **Static Site Rewrites:** If frontend routes aren't working (showing a 404), ensure the rewrite rule (`/*` to `/index.html`) is correctly configured in the Static Site settings.
* **Database Connection:** Verify the `DATABASE_URL` is correct and that the database is running. Use Render's shell to test connectivity if needed. Ensure migrations have run successfully.

---

---
**Document Details**
- Title: Deployment Guide (render)
- Type: Technical Documentation
- Version: 1.0.0
- Last Updated: 2025-04-05
---
End of Deployment Guide (render)
---



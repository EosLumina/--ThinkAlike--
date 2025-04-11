# Installation Guide

**Welcome to ThinkAlike! - Read This First!**

This guide provides step-by-step instructions for setting up your local development environment for the ThinkAlike project using the correct technology stack (FastAPI backend, React frontend, SQLite database for local development).

Following these instructions **exactly** will help you get your local environment running smoothly.

**Reference:** Always consult the [SOURCE OF TRUTH - THINKALIKE PROJECT - MASTER REFERENCE.md](master_refernce.md) for the overarching project vision, ethical principles, and architectural guidelines.

---

## Quick Start Summary (For Experienced Users)

If you're familiar with Python/Node environments, here are the essential commands (run from project root, assuming prerequisites are met):

1. `git clone https://github.com/EosLumina/--ThinkAlike--.git ThinkAlike`
2. `cd ThinkAlike`
3. `python -m venv venv`
4. `.\venv\Scripts\Activate.ps1` (Windows PowerShell) OR `source venv/bin/activate` (macOS/Linux)
5. `pip install -r requirements.txt`
6. `cd frontend`
7. `npm install`
8. `cd ..`
9. `python init_db.py` (Ensure `schema.sql` exists and `instance/` folder can be created)

1. `git clone https://github.com/Willeede/thinkalike_project.git ThinkAlike`
2. `cd ThinkAlike`
3. `python -m venv venv`
4. `.\venv\Scripts\Activate.ps1` (Windows PowerShell) OR `source venv/bin/activate` (macOS/Linux)
5. `pip install -r requirements.txt`
6. `cd frontend`
7. `npm install`
8. `cd ..`
9. `python init_db.py` (Ensure `schema.sql` exists and `instance/` folder can be created)
10. Configure `.env` files (root and `frontend/`) as per detailed steps below.
11. **Terminal 1 (Root):** `.\venv\Scripts\Activate.ps1` then `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
12. **Terminal 2 (Root):** `cd frontend` then `npm start`
13. Access Frontend: `http://localhost:3000`
14. Access Backend Docs: `http://localhost:8000/docs`

---

## 1. Prerequisites - Before You Begin

Ensure you have the following software installed *before* cloning the project:

1. **Git:**

    * **Purpose:** Version control and cloning from GitHub.

    * **Download:** [https://git-scm.com/](https://git-scm.com/)

2. **Python 3.9+:**

    * **Purpose:** Running the FastAPI backend.

    * **Download:** [https://www.python.org/downloads/](https://www.python.org/downloads/)

    * **Important:** During installation, **check the option to "Add Python to PATH"**.

3. **Node.js 16+ and npm:**

    * **Purpose:** Managing frontend dependencies and running the React development server. npm comes bundled with Node.js.

    * **Download:** [https://nodejs.org/](https://nodejs.org/) (Version 16 or later LTS recommended).

4. **Visual Studio Code (Recommended):**

    * **Purpose:** Code editor with good support for Python and JavaScript/React.

    * **Download:** [https://code.visualstudio.com/](https://code.visualstudio.com/)

5. **Docker Desktop (Optional but Recommended for Future):**

    * **Purpose:** Simplifies setup, ensures consistent environments, useful for PostgreSQL later.

    * **Download:** [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

    * *(Note: We use SQLite directly for initial local setup).*

---

## 2. Project Setup

**Step 1: Clone the Repository**

* Open **PowerShell** (or your preferred terminal).

* Navigate to the directory where you want to store the project (e.g., `C:\`).

* Clone the repository:

    ```powershell
    git clone https://github.com/EosLumina/--ThinkAlike--.git ThinkAlike
    ```

* Navigate into the project directory:

    ```powershell
    cd ThinkAlike
    ```

    *(Your prompt should now show the path, e.g., `PS C:\ThinkAlike>`)*

**Step 2: Backend Setup (Python Virtual Environment & Dependencies)**

* **Create a Virtual Environment:** From the project root (`C:\ThinkAlike`), create a Python virtual environment named `venv`:

    ```powershell
    python -m venv venv
    ```

* **Activate the Virtual Environment:**

    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

    *(If you encounter execution policy errors, you might need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` in an **Administrator** PowerShell window first, then try activating again in your regular PowerShell window).*

    *(Your terminal prompt should now show `(venv)` at the beginning, like `(venv) PS C:\ThinkAlike>`)*

* **Install Backend Dependencies:** Install the Python packages listed in `requirements.txt`:

    ```powershell
    pip install -r requirements.txt
    ```

**Step 3: Frontend Setup (Node.js Dependencies)**

* **Navigate to the `frontend` directory:**

    ```powershell
    cd frontend
    ```

* **Install Frontend Dependencies:**

    ```powershell
    npm install
    ```

    *(If you encounter SSL errors or similar, try setting `NODE_OPTIONS=--openssl-legacy-provider` before running `npm install` or `npm start`, especially with Node.js v17+)*

* **Navigate back to the project root:**

    ```powershell
    cd ..
    ```

---

## 3. Configuration

**Step 4: Initialize SQLite Database**

* Ensure your virtual environment is activated (`(venv)` should be visible in your prompt).

* Ensure an `instance/` directory exists in the root, or that the script can create it.

* Ensure a `schema.sql` file exists with your table definitions.

* Run the database initialization script. From the project root (`C:\ThinkAlike`):

    ```powershell
    python init_db.py
    ```

    *(This script should connect to the SQLite DB path defined (likely `instance/thinkalike.db`), create the file if it doesn't exist, and execute the SQL from `schema.sql` to create tables.)*

**Step 5: Configure Environment Variables (`.env` files)**

* **Backend (`.env` in Root):**

  * Create the file `C:\ThinkAlike\.env` if it doesn't exist.

  * Add *at least* the following, **changing the `SECRET_KEY`**:

        ```dotenv
        # C:\ThinkAlike\.env

        DEBUG=True
        SECRET_KEY=your_very_strong_random_secret_key_here_CHANGE_ME
        DATABASE_URL=sqlite:///instance/thinkalike.db
        # Add other backend keys if needed (e.g., AI_API_KEY)

        ```

* **Frontend (`.env` in `frontend/`):**

  * Create the file `C:\ThinkAlike\frontend\.env` if it doesn't exist.

  * Add the URL for your *local* backend:

        ```dotenv
        # C:\ThinkAlike\frontend\.env

        REACT_APP_BACKEND_URL=http://localhost:8000
        ```

* **`.gitignore`:** Ensure your main `.gitignore` file (in `C:\ThinkAlike`) ignores `.env` files, `venv/`, and `instance/` (if `thinkalike.db` is inside):

    ```gitignore
    # Environment variables

    .env
    .env.*

    *.env.local
    !*.env.example

    # Virtual environment

    venv/
    .venv/

    # Instance folder (for SQLite DB)

    instance/

    # Node

    frontend/node_modules/
    frontend/build/
    frontend/.pnp.*
    frontend/.DS_Store
    npm-debug.log*
    yarn-debug.log*
    yarn-error.log*
    ```

---

## 4. Running the Application Locally

Run the backend and frontend servers simultaneously in **separate terminals**.

**Step 6: Start the Backend Server**

* Open a **new** PowerShell window/tab.

* Navigate to the project root: `cd C:\ThinkAlike`

* Activate the virtual environment: `.\venv\Scripts\Activate.ps1`

* Start the FastAPI server using Uvicorn:

    ```powershell
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

    *(Keep this terminal open. You should see output indicating the server is running, typically on `http://127.0.0.1:8000`. Access API docs at `http://127.0.0.1:8000/docs`)*

**Step 7: Start the Frontend Development Server**

* Open ***another new***, *separate* PowerShell window/tab.

* Navigate to the `frontend` directory: `cd C:\ThinkAlike\frontend`

* *(Optional: If you hit SSL errors)* `Set-Item -Path Env:NODE_OPTIONS -Value "--openssl-legacy-provider"`

* Start the React development server:

    ```powershell
    npm start
    ```

    *(Keep this terminal open. Your browser should open automatically to `http://localhost:3000`. If not, open it manually.)*

---

## 5. Verification

* **Backend:** Open `http://localhost:8000/docs` in your browser. See the FastAPI interactive API documentation.

* **Frontend:** Open `http://localhost:3000`. See the ThinkAlike application interface.

* **Interaction:** Test basic features (login/register if implemented, fetching data). Use browser developer tools (F12) -> "Console" and "Network" tabs to check for errors. Ensure frontend requests to `http://localhost:8000` are successful (check Network tab for CORS errors if they fail).

---

You should now have a working local development environment for ThinkAlike! Refer to `CONTRIBUTING.md` and other documentation for development guidelines.

---

**Document Details**

* Title: Installation Guide

* Type: Core Documentation

* Version: 1.0.0

* Last Updated: 2025-04-05

---

End of Installation Guide

---

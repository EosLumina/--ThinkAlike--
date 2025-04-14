# Contributor Quick Start Guide

Welcome to ThinkAlike! This guide will help you get started as a contributor as quickly as possible.

## 1. Five-Minute Setup

1. **Clone & Install:**

   ```bash
   git clone https://github.com/EosLumina/--ThinkAlike--.git
   cd --ThinkAlike--
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

   pip install -r requirements.txt
   cd frontend
   npm install
   cd ..
   python init_db.py
   ```

2. **Start Development Servers:**

   ```bash
   # Terminal 1

   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2

   cd frontend
   npm start
   ```

3. **Access the App:**

   * Frontend: [http://localhost:3000](http://localhost:3000)

   * API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## 2. Project Structure at a Glance

```text

--ThinkAlike--/

├── main.py               # Backend entry point (FastAPI)

├── requirements.txt      # Python dependencies

├── frontend/            # React frontend

│   ├── src/             # Frontend source code

│   └── package.json     # Node.js dependencies

├── app/                 # Backend modules

│   ├── models/          # Database models

│   ├── routes/          # API endpoints

│   └── services/        # Business logic

└── docs/                # Project documentation

```

## 3. Making Your First Contribution

1. **Choose a Task:**

   * Check [GitHub Issues](https://github.com/EosLumina/--ThinkAlike--/issues) for tasks marked `good first issue`

   * Review the [MVP Implementation Guide](../guides/implementation_guides/mvp_implementation_guide.md)

2. **Create a Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes & Test:**

   * Follow the [Developer Workflow Guide](./developer_workflow.md)

   * Ensure all tests pass before submitting

4. **Submit a Pull Request:**

   * Push your branch to GitHub

   * Create a PR with a clear description of your changes

## 4. Participating in Swarming Sessions

ThinkAlike uses collaborative coding sessions ("swarms") for complex features:

1. **Join the Discord:** [ThinkAlike Discord](https://discord.gg/TnAcWezH)
2. **Check the Swarming Schedule:** Posted in #swarming-schedule channel
3. **Prepare for Sessions:** Review relevant documentation before joining

## 5. Need Help?

### Resources

* **Documentation:** Start with [Project Overview](./project_overview.md)

* **Installation Issues:** See [Troubleshooting Guide](../architecture/deployment_troubleshooting.md)

* **Contribution Guidelines:** Read our [Contributing Overview](../contributing.md) or [Detailed Contributing Guide](../core/contributing.md)

* **Questions:** Ask in Discord #help channel

Happy coding!

---

**Document Details**

* Title: Contributor Quick Start Guide

* Type: Core Documentation

* Version: 1.0.0

* Last Updated: 2025-05-10

---

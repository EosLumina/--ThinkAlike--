"""
ThinkAlike Entry Point

This script provides a convenient entry point for running the ThinkAlike application.
It represents our principle of accessibility by making the project easy to start for 
contributors of all technical backgrounds.
"""
import os
import subprocess
import sys
import argparse
from pathlib import Path


def check_environment():
    """Check if the environment is properly set up."""
    if not Path("venv").exists():
        print("Virtual environment not found. Running setup script...")
        try:
            subprocess.run(
                [sys.executable, "scripts/setup_project.py"], check=True)
        except subprocess.CalledProcessError:
            print(
                "Error: Setup failed. Please run 'python scripts/setup_project.py' manually.")
            sys.exit(1)

    # Check if .env file exists
    if not Path(".env").exists():
        print("Creating default .env file...")
        with open(".env", "w") as f:
            f.write("DATABASE_URL=sqlite:///./thinkalike.db\n")
            f.write("SECRET_KEY=developmentkey\n")
            f.write("ALGORITHM=HS256\n")
            f.write("ACCESS_TOKEN_EXPIRE_MINUTES=30\n")
        print("Created .env file with development settings")


def start_backend(host="127.0.0.1", port=8000, reload=True):
    """Start the backend server."""
    print(f"Starting ThinkAlike backend on http://{host}:{port}")

    reload_arg = "--reload" if reload else ""
    cmd = f"uvicorn backend.app.main:app --host {host} --port {port} {reload_arg}"

    try:
        subprocess.run(cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print("\nBackend server stopped")
    except subprocess.CalledProcessError:
        print("Error: Failed to start backend server.")
        sys.exit(1)


def start_frontend(port=3000):
    """Start the frontend development server."""
    if not Path("frontend/package.json").exists():
        print("Error: Frontend directory not found or incomplete.")
        print("Please make sure you have the frontend code and run 'npm install' in the frontend directory.")
        sys.exit(1)

    print(f"Starting ThinkAlike frontend on http://localhost:{port}")

    try:
        os.chdir("frontend")
        subprocess.run(f"npm start -- --port {port}", shell=True, check=True)
    except KeyboardInterrupt:
        print("\nFrontend server stopped")
    except subprocess.CalledProcessError:
        print("Error: Failed to start frontend server.")
        sys.exit(1)
    finally:
        os.chdir("..")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run ThinkAlike application")
    parser.add_argument("--backend-only", action="store_true",
                        help="Start only the backend server")
    parser.add_argument("--frontend-only", action="store_true",
                        help="Start only the frontend server")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Backend host address")
    parser.add_argument("--port", type=int, default=8000, help="Backend port")
    parser.add_argument("--frontend-port", type=int,
                        default=3000, help="Frontend port")
    parser.add_argument("--no-reload", action="store_true",
                        help="Disable auto-reload for backend")

    args = parser.parse_args()

    # Check environment first
    check_environment()

    # Determine what to start
    if args.backend_only:
        start_backend(host=args.host, port=args.port,
                      reload=not args.no_reload)
    elif args.frontend_only:
        start_frontend(port=args.frontend_port)
    else:
        # Start both
        print("Starting both backend and frontend servers...")
        print("Use Ctrl+C to stop the servers")
        print("To start them separately, use --backend-only or --frontend-only options")

        # Start backend in a separate process
        backend_cmd = f"uvicorn backend.app.main:app --host {args.host} --port {args.port}"
        if not args.no_reload:
            backend_cmd += " --reload"

        backend_process = subprocess.Popen(backend_cmd, shell=True)

        try:
            # Start frontend in the current process
            start_frontend(port=args.frontend_port)
        finally:
            # Make sure to terminate the backend process
            backend_process.terminate()
            print("Both servers stopped")


if __name__ == "__main__":
    main()

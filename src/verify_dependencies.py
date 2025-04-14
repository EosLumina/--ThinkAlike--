import sys
import importlib.metadata


def verify_dependencies(requirements_file="requirements.txt"):
    print("Verifying installed Python packages against", requirements_file)
    missing = []
    with open(requirements_file, "r") as rf:
        for line in rf:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Extract package name before any version specifiers
            pkg = line.split("==")[0].strip()
            try:
                version = importlib.metadata.version(pkg)
                print(f"Package {pkg} version {version} installed.")
            except importlib.metadata.PackageNotFoundError:
                missing.append(pkg)
                print(f"⚠️ Package {pkg} is missing.")

    if missing:
        print("Missing packages:", ", ".join(missing))
        sys.exit(1)
    else:
        print("All dependencies verified successfully.")


if __name__ == "__main__":
    verify_dependencies()

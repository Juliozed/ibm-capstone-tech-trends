"""
setup_project.py
================
Run this once when starting a new project.
It verifies your environment is set up correctly.

RUN: python setup_project.py
"""

import subprocess
import sys
import os


def check_python():
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or version.minor < 9:
        print("WARNING: Python 3.9+ recommended")
    else:
        print("✓ Python version OK")


def check_libraries():
    libraries = [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "sqlalchemy",
        "psycopg2",
        "openpyxl",
        "dbt",
        "dotenv",
        "requests",
    ]
    missing = []
    for lib in libraries:
        try:
            __import__(lib.replace("-", "_"))
            print(f"  ✓ {lib}")
        except ImportError:
            print(f"  ✗ {lib} — NOT INSTALLED")
            missing.append(lib)

    if missing:
        print(f"\nInstall missing libraries:")
        print(f"  pip install -r requirements.txt")
    else:
        print("\n✓ All libraries installed")


def check_env():
    if os.path.exists(".env"):
        print("✓ .env file found")
        from dotenv import load_dotenv

        load_dotenv()
        required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing = [k for k in required if not os.getenv(k)]
        if missing:
            print(f"  Missing in .env: {missing}")
        else:
            print("  ✓ All database credentials set")
    else:
        print("✗ .env file not found")
        print("  Copy .env.example to .env and fill in your credentials")


def check_db():
    try:
        from scripts.db_connect import test_connection

        test_connection()
    except Exception as e:
        print(f"✗ Database connection failed: {e}")


def check_dbt():
    try:
        result = subprocess.run(["dbt", "--version"], capture_output=True, text=True)
        print(f"✓ dbt: {result.stdout.strip()}")
    except FileNotFoundError:
        print("✗ dbt not found — run: pip install dbt-postgres")


def check_git():
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        print(f"✓ {result.stdout.strip()}")
    except FileNotFoundError:
        print("✗ git not found")


if __name__ == "__main__":
    print("=" * 50)
    print("  PROJECT ENVIRONMENT CHECK")
    print("=" * 50)

    print("\n── Python ──────────────────")
    check_python()

    print("\n── Libraries ───────────────")
    check_libraries()

    print("\n── Credentials (.env) ──────")
    check_env()

    print("\n── Database Connection ──────")
    check_db()

    print("\n── dbt ─────────────────────")
    check_dbt()

    print("\n── Git ─────────────────────")
    check_git()

    print("\n" + "=" * 50)
    print("  Setup check complete")
    print("=" * 50)

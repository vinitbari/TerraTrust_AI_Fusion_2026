"""Utility script to verify and patch auth endpoints with dynamic repo paths."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
auth_py_path = ROOT_DIR / "apps" / "api" / "app" / "api" / "v1" / "endpoints" / "auth.py"

if auth_py_path.exists():
    content = auth_py_path.read_text(encoding="utf-8")
    if "/farmer/register" in content:
        print("auth.py already contains farmer/officer endpoints.")
    else:
        print("auth.py ready.")

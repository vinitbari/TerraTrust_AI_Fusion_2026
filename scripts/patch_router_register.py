"""Utility script to verify register route in router.tsx with dynamic repo paths."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
router_path = ROOT_DIR / "apps" / "web" / "src" / "app" / "router.tsx"

if router_path.exists():
    content = router_path.read_text(encoding="utf-8")
    if "/register" in content:
        print("router.tsx already has /register routes configured.")
    else:
        print("router.tsx checked.")

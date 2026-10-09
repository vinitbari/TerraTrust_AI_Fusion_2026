"""Utility script to verify and patch Topbar with dynamic repo paths."""

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
topbar_path = ROOT_DIR / "apps" / "web" / "src" / "components" / "layout" / "Topbar.tsx"

if topbar_path.exists():
    content = topbar_path.read_text(encoding="utf-8")
    content = re.sub(r'to="/([^"]+)"', r'to="/officer/\1"', content)
    content = content.replace("link: '/crop", "link: '/officer/crop")
    topbar_path.write_text(content, encoding="utf-8")
    print("Topbar.tsx verified.")

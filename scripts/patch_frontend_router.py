"""Utility script to patch frontend router and sidebar with dynamic repo paths."""

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
router_path = ROOT_DIR / "apps" / "web" / "src" / "app" / "router.tsx"
sidebar_path = ROOT_DIR / "apps" / "web" / "src" / "components" / "layout" / "Sidebar.tsx"

if router_path.exists():
    content = router_path.read_text(encoding="utf-8")
    if "HomePage" not in content:
        content = content.replace(
            "import { LoginPage } from '@/features/auth/LoginPage';",
            "import { LoginPage } from '@/features/auth/LoginPage';\nimport { HomePage } from '@/features/public/HomePage';",
        )
        home_page_route = """  {
    path: '/',
    element: (
      <PublicOnlyRoute>
        <HomePage />
      </PublicOnlyRoute>
    ),
  },
"""
        content = content.replace("export const router = createBrowserRouter([", "export const router = createBrowserRouter([\n" + home_page_route)
        router_path.write_text(content, encoding="utf-8")
        print("router.tsx verified and patched.")
    else:
        print("router.tsx already has HomePage route.")

if sidebar_path.exists():
    sidebar_content = sidebar_path.read_text(encoding="utf-8")
    sidebar_content = sidebar_content.replace('to="/"', 'to="/officer"')
    sidebar_path.write_text(sidebar_content, encoding="utf-8")
    print("Sidebar.tsx verified.")

"""
Verify Playwright setup is working correctly.

Run this before running actual tests:
    uv run python tests/browser/verify_setup.py
"""

import sys
from pathlib import Path


def verify_playwright():
    """Verify Playwright is installed."""
    try:
        from playwright.sync_api import sync_playwright
        print("✓ Playwright installed successfully")
        return True
    except ImportError as e:
        print(f"✗ Playwright not installed: {e}")
        print("  Fix: uv pip install playwright pytest-playwright")
        return False


def verify_pytest_playwright():
    """Verify pytest-playwright plugin is installed."""
    try:
        import pytest_playwright
        print("✓ pytest-playwright plugin installed")
        return True
    except ImportError as e:
        print(f"✗ pytest-playwright not installed: {e}")
        print("  Fix: uv pip install pytest-playwright")
        return False


def verify_browser():
    """Verify Chromium browser is installed."""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print("✓ Chromium browser installed and working")
                return True
            except Exception as e:
                print(f"✗ Chromium browser not working: {e}")
                print("  Fix: uv run playwright install chromium")
                return False
    except Exception as e:
        print(f"✗ Browser check failed: {e}")
        return False


def verify_test_files():
    """Verify test files exist."""
    test_dir = Path(__file__).parent
    
    files_to_check = [
        "test_ui_smoke.py",
        "conftest.py",
        "__init__.py",
    ]
    
    all_exist = True
    for filename in files_to_check:
        filepath = test_dir / filename
        if filepath.exists():
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            all_exist = False
    
    return all_exist


def verify_config():
    """Verify pytest-playwright.ini exists."""
    config_path = Path(__file__).parent.parent.parent / "pytest-playwright.ini"
    
    if config_path.exists():
        print("✓ pytest-playwright.ini exists")
        return True
    else:
        print("✗ pytest-playwright.ini missing")
        print("  Create in project root with base_url=http://localhost:3000")
        return False


def main():
    """Run all verification checks."""
    print("Playwright Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Playwright library", verify_playwright),
        ("pytest-playwright plugin", verify_pytest_playwright),
        ("Chromium browser", verify_browser),
        ("Test files", verify_test_files),
        ("Configuration", verify_config),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        results.append(check_func())
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("\n✓ All checks passed! Playwright is ready to use.")
        print("\nNext steps:")
        print("  1. Start dev server: uv run reflex run")
        print("  2. Run tests: uv run pytest tests/browser -c pytest-playwright.ini")
        print("  3. Run with visible browser: uv run pytest tests/browser --headed")
        return 0
    else:
        print("\n✗ Some checks failed. Fix the issues above and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

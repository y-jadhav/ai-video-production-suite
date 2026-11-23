"""Persistent browser session manager — keeps cookies alive for days/weeks.

Instead of creating throwaway contexts from storage_state.json (which lose session cookies),
this uses launch_persistent_context() with a real Chrome user_data_dir. The browser profile
directory holds all cookies, localStorage, IndexedDB natively — just like a real Chrome install.

After each operation, we save storage_state back as a backup.
"""

import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, BrowserContext


# Persistent profile directory — survives across all launches
PROFILE_DIR = str(Path.home() / ".twitter-mcp" / "chrome-profile")
STORAGE_BACKUP = str(Path.home() / ".twitter-mcp" / "storage_state.json")

# Anti-detection args
BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-blink-features=AutomationControlled",
    "--disable-features=IsolateOrigins,site-per-process",
    "--disable-site-isolation-trials",
    "--disable-web-security",
    "--restore-last-session",  # CRITICAL: prevents Chromium from discarding session cookies on restart
]

IGNORE_ARGS = ["--enable-automation"]

# Twitter blocks headless browsers. Use Xvfb virtual display instead.
# Install: apt-get install -y xvfb
# Start: Xvfb :99 -screen 0 1280x720x24 & export DISPLAY=:99
USE_HEADLESS = False  # Set True only if Xvfb is NOT available


async def get_persistent_context() -> tuple:
    """Launch browser with persistent context.

    Returns (playwright, context) — caller must close both when done.

    The persistent context stores cookies in PROFILE_DIR, which persists
    between launches. This is how real browsers work — cookies survive
    because the profile directory keeps them.
    """
    os.makedirs(PROFILE_DIR, exist_ok=True)

    pw = await async_playwright().start()

    # If we have a storage_state backup but no profile yet, seed the profile
    # by importing cookies on first launch
    storage_path = Path(STORAGE_BACKUP)
    profile_cookies = Path(PROFILE_DIR) / "Default" / "Cookies"

    # Check if display is available — on Linux via DISPLAY/Xvfb, or natively on Windows/macOS
    import shutil
    import sys
    has_display = os.environ.get("DISPLAY") is not None or sys.platform in ('win32', 'darwin')
    if "TWITTER_HEADLESS" in os.environ:
        headless = os.environ["TWITTER_HEADLESS"].lower() in ("true", "1", "yes")
    else:
        headless = USE_HEADLESS if has_display else True  # Fallback to headless if no display

    context = await pw.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=headless,
        args=BROWSER_ARGS,
        ignore_default_args=IGNORE_ARGS,
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    )

    # Seed profile from storage_state.json on first run (if profile is fresh)
    if storage_path.exists() and not profile_cookies.exists():
        try:
            import json
            with open(storage_path) as f:
                state = json.load(f)
            if "cookies" in state:
                await context.add_cookies(state["cookies"])
        except Exception:
            pass  # Non-critical

    return pw, context


async def save_session(context: BrowserContext):
    """Save current session back to storage_state.json as backup."""
    try:
        os.makedirs(os.path.dirname(STORAGE_BACKUP), exist_ok=True)
        await context.storage_state(path=STORAGE_BACKUP)
    except Exception:
        pass  # Non-critical — profile dir is the primary store


async def close_session(pw, context: BrowserContext):
    """Save session and close browser cleanly."""
    await save_session(context)
    await context.close()
    await pw.stop()


async def import_fresh_cookies(cookies_path: str):
    """Import fresh cookies from a file into the persistent profile.

    Use this when you get new cookies from your real browser.
    It launches the profile, loads the cookies, visits Twitter to
    activate them, then saves.
    """
    pw, context = await get_persistent_context()
    try:
        # Load cookies from the provided file
        import json
        with open(cookies_path) as f:
            state = json.load(f)

        if "cookies" in state:
            await context.add_cookies(state["cookies"])

        # Visit Twitter to activate cookies and let them refresh
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://x.com/home", wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        # Save everything
        await save_session(context)
        return "Cookies imported and activated successfully"
    finally:
        await close_session(pw, context)


async def async_login():
    """Opens a real browser window to log in to Twitter/X manually and persists the session."""
    os.makedirs(PROFILE_DIR, exist_ok=True)
    pw = await async_playwright().start()

    print("=" * 65)
    print("  LAUNCHING CHROMIUM FOR TWITTER / X LOGIN")
    print("=" * 65)
    context = await pw.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=False,
        args=BROWSER_ARGS,
        ignore_default_args=IGNORE_ARGS,
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    )

    page = context.pages[0] if context.pages else await context.new_page()
    print("Navigating to https://x.com/login ...")
    try:
        await page.goto("https://x.com/login", wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        print(f"Navigation warning: {e}")

    print("\n" + "*" * 65)
    print("  ACTION REQUIRED:")
    print("  1. In the Chromium browser window that just popped up,")
    print("     enter your Twitter/X username & password and log in.")
    print("  2. When you reach your Home feed, come back here and")
    print("     PRESS ENTER (or wait ~10s for auto-detection).")
    print("*" * 65 + "\n")

    async def wait_for_enter():
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, input, "Press [ENTER] once you are logged in: ")
        except (EOFError, Exception):
            # Non-interactive shell / background task: sleep and let poll_login handle detection
            while True:
                await asyncio.sleep(3600)

    async def poll_login():
        while True:
            await asyncio.sleep(3)
            try:
                # Check if user closed the browser window
                if not context.pages or all(p.is_closed() for p in context.pages):
                    print("\n[INFO] Browser window closed by user.")
                    return

                cookies = await context.cookies()
                names = {c["name"] for c in cookies}
                pages = [p for p in context.pages if not p.is_closed()]
                current_url = pages[0].url if pages else ""
                
                if "auth_token" in names or "/home" in current_url:
                    print("\n[OK] Detected successful login (auth_token cookie present)!")
                    await asyncio.sleep(2)
                    return
            except Exception:
                pass

    done, pending = await asyncio.wait(
        [asyncio.create_task(wait_for_enter()), asyncio.create_task(poll_login())],
        return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()

    print("\nSaving session cookies and profile...")
    await save_session(context)
    print(f"[OK] Session saved successfully to:")
    print(f"    - {PROFILE_DIR}")
    print(f"    - {STORAGE_BACKUP}")
    await context.close()
    await pw.stop()
    print("\n[OK] Browser closed cleanly. Twitter MCP is now authenticated and ready!")


def login():
    """Synchronous entry point for manual browser login."""
    asyncio.run(async_login())


if __name__ == "__main__":
    login()


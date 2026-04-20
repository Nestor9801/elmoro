from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config import API_HOME_URL, API_USER, API_PASSWORD

STATE_FILE = Path("playwright_state.json")


def login_and_save_state(headless: bool = True) -> Path:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        page.goto(API_HOME_URL, wait_until="domcontentloaded")

        # Ajusta selectores según el login real
        possible_user_selectors = [
            'input[name="usuario"]',
            'input[name="user"]',
            'input[name="username"]',
            'input[type="text"]',
        ]
        possible_pass_selectors = [
            'input[name="password"]',
            'input[name="pass"]',
            'input[type="password"]',
        ]

        user_filled = False
        for sel in possible_user_selectors:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.fill(API_USER)
                user_filled = True
                break

        if not user_filled:
            browser.close()
            raise RuntimeError("No encontré el campo de usuario")

        pass_filled = False
        for sel in possible_pass_selectors:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.fill(API_PASSWORD)
                pass_filled = True
                break

        if not pass_filled:
            browser.close()
            raise RuntimeError("No encontré el campo de contraseña")

        # Intenta botón submit común
        clicked = False
        button_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Entrar")',
            'button:has-text("Login")',
            'button:has-text("Iniciar sesión")',
        ]

        for sel in button_selectors:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.click()
                clicked = True
                break

        if not clicked:
            # fallback: enter sobre password
            for sel in possible_pass_selectors:
                if page.locator(sel).count() > 0:
                    page.locator(sel).first.press("Enter")
                    clicked = True
                    break

        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except PlaywrightTimeoutError:
            pass

        html = page.content().lower()
        invalid_markers = ["password", "contraseña", "iniciar sesión", "login", "usuario"]

        # Ajusta esta validación si la página principal también contiene una de esas palabras
        if any(marker in html for marker in invalid_markers):
            browser.close()
            raise RuntimeError("El login no parece haber quedado autenticado")

        context.storage_state(path=str(STATE_FILE))
        browser.close()
        return STATE_FILE


if __name__ == "__main__":
    path = login_and_save_state(headless=False)
    print(f"Estado guardado en: {path}")
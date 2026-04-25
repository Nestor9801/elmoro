from auth_playwright import login_and_save_state
from api_requests import load_state, build_session_from_state


def get_valid_session():
    try:
        state = load_state()
        return build_session_from_state(state)
    except Exception:
        print("Sesion no valida. Regenerando login...")
        login_and_save_state(headless=True)
        state = load_state()
        return build_session_from_state(state)
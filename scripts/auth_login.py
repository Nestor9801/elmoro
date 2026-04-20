import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import API_USER, API_PASSWORD

USER = API_USER
PASSWORD = API_PASSWORD

HOME_URL = "https://eos.zetus.mx/elmoro/"


def debug_response(label, response, session):
    print(f"\n--- {label} ---")
    print("STATUS:", response.status_code)
    print("URL FINAL:", response.url)
    print("CONTENT-TYPE:", response.headers.get("Content-Type"))
    print("COOKIES:", session.cookies.get_dict())
    print("BODY:", response.text[:1000])


def find_login_form(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")

    if not forms:
        raise Exception("No encontré ningún formulario en la página")

    print(f"Formularios encontrados: {len(forms)}")

    # toma el primer form como intento inicial
    form = forms[0]

    action = form.get("action") or ""
    method = (form.get("method") or "post").lower()
    action_url = urljoin(base_url, action)

    inputs = form.find_all("input")
    form_data = {}

    for inp in inputs:
        name = inp.get("name")
        if not name:
            continue
        value = inp.get("value", "")
        form_data[name] = value

    print("FORM ACTION:", action_url)
    print("FORM METHOD:", method)
    print("FORM FIELDS:", list(form_data.keys()))

    return action_url, method, form_data


def inject_credentials(form_data):
    # intenta nombres comunes
    possible_user_fields = ["usuario", "user", "username", "login", "correo"]
    possible_pass_fields = ["password", "pass", "passwd", "contrasena", "contraseña"]

    user_field = None
    pass_field = None

    for key in form_data.keys():
        lk = key.lower()
        if lk in possible_user_fields and user_field is None:
            user_field = key
        if lk in possible_pass_fields and pass_field is None:
            pass_field = key

    # fallback si no encuentra nada
    if user_field is None:
        user_field = "usuario"
        form_data[user_field] = ""
    if pass_field is None:
        pass_field = "password"
        form_data[pass_field] = ""

    form_data[user_field] = USER
    form_data[pass_field] = PASSWORD

    print("USER FIELD:", user_field)
    print("PASS FIELD:", pass_field)

    return form_data


def looks_like_login_page(html):
    text = html.lower()
    markers = ["iniciar sesión", "iniciar sesion", "password", "contraseña", "usuario", "login"]
    return any(m in text for m in markers)


def login():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": HOME_URL,
        "Origin": "https://eos.zetus.mx"
    }

    # 1) Abrir página inicial
    r1 = session.get(HOME_URL, headers=headers, timeout=30)
    debug_response("GET HOME", r1, session)

    # 2) Detectar formulario real
    action_url, method, form_data = find_login_form(r1.text, HOME_URL)

    # 3) Inyectar credenciales y conservar hidden fields
    form_data = inject_credentials(form_data)

    # 4) Enviar login real
    if method == "post":
        r2 = session.post(
            action_url,
            headers=headers,
            data=form_data,
            timeout=30,
            allow_redirects=True
        )
    else:
        r2 = session.get(
            action_url,
            headers=headers,
            params=form_data,
            timeout=30,
            allow_redirects=True
        )

    debug_response("LOGIN SUBMIT", r2, session)

    if not session.cookies.get_dict():
        raise Exception("No se obtuvo cookie de sesión")

    if looks_like_login_page(r2.text):
        raise Exception("El login sigue regresando la página de acceso. Faltan campos, token o JS.")

    return session


def obtener_registros(axis, session):
    data_url = "https://eos.zetus.mx/elmoro/ventas@tabla_cuentas&axis="
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": HOME_URL,
        "Origin": "https://eos.zetus.mx",
    }

    response = session.post(
        data_url,
        headers=headers,
        data={"axis": axis},
        auth=(USER, PASSWORD),
        timeout=60
    )

    debug_response("DATA REQUEST", response, session)

    content_type = response.headers.get("Content-Type", "")
    if "json" not in content_type.lower():
        raise Exception("La API no regresó JSON; probablemente la sesión no quedó autenticada.")

    data = response.json()
    print("JSON KEYS:", list(data.keys()))
    return data


if __name__ == "__main__":
    axis = "2026-04-01|2026-04-08|1"

    try:
        session = login()
        data = obtener_registros(axis, session)
        print("\nOK, respuesta JSON recibida")
    except Exception as e:
        print("\nERROR:", e)
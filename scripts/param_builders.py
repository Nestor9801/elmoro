from datetime import datetime, timedelta

SUCURSALES = [
    20, 19, 4, 3, 23, 12, 24, 1, 2, 15, 21, 14,
    9, 11, 6, 22, 8, 7, 16, 10, 18, 5, 17, 13
]


def today_dash():
    return datetime.now().strftime("%Y-%m-%d")


def today_slash():
    return datetime.now().strftime("%Y/%m/%d")

def build_axis_all():
    hoy = today_dash()
    return {"axis": f"{hoy}|{hoy}|1"}


def build_movimientos_payload(tipo_mov, busc_fltr=""):
    fecha = today_slash()

    data = [
        ("fecha_ini", fecha),
        ("fecha_fin", fecha),
        ("busc_fltr", busc_fltr),
        ("tipo_mov", tipo_mov),
    ]

    for suc in SUCURSALES:
        data.append(("suc_ar[]", suc))

    return data

#########  YESTERDAY  #########

def yesterday_dash():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def yesterday_slash():
    return (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")

def build_axis_yesterday(branch_id):
    ayer = yesterday_dash()
    return {"axis": f"{ayer}|{ayer}|{branch_id}"}

def build_movimientos_payload_yesterday(tipo_mov, busc_fltr=""):
    fecha = yesterday_slash()

    data = [
        ("fecha_ini", fecha),
        ("fecha_fin", fecha),
        ("busc_fltr", busc_fltr),
        ("tipo_mov", tipo_mov),
    ]

    for suc in SUCURSALES:
        data.append(("suc_ar[]", suc))

    return data


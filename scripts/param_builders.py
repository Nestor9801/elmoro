SUCURSALES = [
    20, 19, 4, 3, 23, 12, 24, 1, 2, 15, 21, 14,
    9, 11, 6, 22, 8, 7, 16, 10, 18, 5, 17, 13
]


def build_tabla_cuentas_payload_for_day(fecha):
    data = [("fecha", fecha)]

    for suc in SUCURSALES:
        data.append(("suc_ar[]", suc))

    data.append(("suc_ar_TAMTOT", len(SUCURSALES)))
    return data


def build_movimientos_payload(fecha_ini, fecha_fin, tipo_mov, busc_fltr=""):
    data = [
        ("fecha_ini", fecha_ini),
        ("fecha_fin", fecha_fin),
        ("busc_fltr", busc_fltr),
        ("tipo_mov", tipo_mov),
    ]

    for suc in SUCURSALES:
        data.append(("suc_ar[]", suc))

    return data


def build_catalogo_categorias_payload(stat_fltr):
    return {
        "stat_fltr": stat_fltr,
        "busc_fltr": "",
    }


def build_catalogo_articulos_detalle_payload(stat_fltr):
    return {
        "stat_fltr": stat_fltr,
        "busc_fltr": "",
        "cat_fltr": "-1",
    }
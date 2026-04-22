ENDPOINTS = [
    {
        "name": "tabla_cuentas",
        "url": "https://eos.zetus.mx/elmoro/ventas@tabla_cuentas&axis=",
        "table": "consumos",
        "conflict_key": "id_c",
        "type": "axis_all",
    },
    {
        "name": "cortes_tabla_general",
        "url": "https://eos.zetus.mx/elmoro/ventas@cortes_tabla_general&axis=",
        "table": "cortes_dia",
        "conflict_key": "id_crt",
        "type": "axis_all",
    },
    {
        "name": "cortes_movimientos_fisicos",
        "url": "https://eos.zetus.mx/elmoro/ventas@r_movimientos_fisicos_manuales_tabla&axis=",
        "table": "cortes_movimientos_fisicos",
        "conflict_key": None,
        "type": "movimientos_all",
    },
    {
        "name": "resumen_diario",
        "url": "https://eos.zetus.mx/elmoro/ventas@r_resumen_por_dia__tabla&axis=",
        "table": "resumen_diario",
        "conflict_key": None,
        "type": "axis_all",
    },
]
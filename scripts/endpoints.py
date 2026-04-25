ENDPOINTS_TRANSACCIONALES = [
    {
        "name": "tabla_cuentas",
        "url": "https://eos.zetus.mx/elmoro/ventas@tabla_cuentas&axis=",
        "table": "transactional",
        "conflict_key": "id_c",
        "type": "tabla_cuentas_range",
        "load_mode": "append_upsert",
    }
]

ENDPOINTS_CATALOGOS = [
    {
        "name": "catalogo_categorias",
        "url": "https://eos.zetus.mx/elmoro/config.catalogos.art@tabla_cat&axis=",
        "table": "catalogo_articulos",
        "conflict_key": "id_art_c",
        "type": "catalogo_categorias",
        "load_mode": "catalog_refresh",
    },
    {
        "name": "catalogo_articulos_detalle",
        "url": "https://eos.zetus.mx/elmoro/config.catalogos.art@tabla_art&axis=",
        "table": "catalogo_articulos_detalle",
        "conflict_key": "id_art",
        "type": "catalogo_articulos_detalle",
        "load_mode": "catalog_refresh",
    },
    {
        "name": "catalogo_unidades_medida",
        "url": "https://eos.zetus.mx/elmoro/config.catalogos.art@tabla_med&axis=",
        "table": "catalogo_unidades_medida",
        "conflict_key": "id_med",
        "type": "catalogo_simple",        
      "load_mode": "catalog_refresh"
    },
]
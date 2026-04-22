CREATE TABLE IF NOT EXISTS consumos (
    id_c         VARCHAR(20) PRIMARY KEY,
    folio_c      INTEGER,
    nom_c        VARCHAR(20),
    nom_ms_c     VARCHAR(100),
    fecha_c      DATE,
    hora_c       TIME,
    fecha_a_c    DATE,
    hora_a_c     TIME,
    num_cli_c    INTEGER,
    stot_c       NUMERIC(12,2),
    i_c          NUMERIC(12,2),
    tot_c        NUMERIC(12,2),
    grat_c       NUMERIC(12,2),
    fac_c        INTEGER,
    nom_trm      VARCHAR(50),
    alias_usu    VARCHAR(50),
    abr_suc      VARCHAR(10),
    nom_cli      VARCHAR(150),
    btn_detalle  TEXT,
    efe          NUMERIC(12,2),
    tar          NUMERIC(12,2),
    fact         NUMERIC(12,2),
    duracion     VARCHAR(20),
    branch_id    INTEGER,
    loaded_at    TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_consumos_fecha_c ON consumos(fecha_c);
CREATE INDEX IF NOT EXISTS idx_consumos_abr_suc ON consumos(abr_suc);
CREATE INDEX IF NOT EXISTS idx_consumos_branch_id ON consumos(branch_id);

CREATE TABLE IF NOT EXISTS cortes_dia (
    id_crt               VARCHAR(30) PRIMARY KEY,
    dob_crt              DATE,
    suc_crt              INTEGER,
    trm_crt              INTEGER,
    crt_ant_crt          VARCHAR(30),
    stat_crt             VARCHAR(10),
    fecha_a_crt          DATE,
    hora_a_crt           TIME,
    usu_a_crt            INTEGER,
    sif_crt              NUMERIC(14,2),
    sff_crt              NUMERIC(14,2),
    fecha_c_crt          DATE,
    hora_c_crt           TIME,
    usu_c_crt            INTEGER,
    monto_capt_crt       NUMERIC(14,2),
    detalle_capt_crt     TEXT,
    direfencia_capt_crt  NUMERIC(14,2),
    nom_trm              VARCHAR(80),
    abr_suc              VARCHAR(20),
    alias_usu            VARCHAR(100),
    btn_detalle          TEXT,
    venta_efe            NUMERIC(14,2),
    devol_efe            NUMERIC(14,2),
    entradas             NUMERIC(14,2),
    salidas              NUMERIC(14,2),
    branch_id            INTEGER,
    loaded_at            TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cortes_dia_dob_crt ON cortes_dia(dob_crt);
CREATE INDEX IF NOT EXISTS idx_cortes_dia_abr_suc ON cortes_dia(abr_suc);
CREATE INDEX IF NOT EXISTS idx_cortes_dia_suc_crt ON cortes_dia(suc_crt);
CREATE INDEX IF NOT EXISTS idx_cortes_dia_branch_id ON cortes_dia(branch_id);
CREATE INDEX IF NOT EXISTS idx_cortes_dia_stat_crt ON cortes_dia(stat_crt);



CREATE TABLE IF NOT EXISTS cortes_movimientos_fisicos (
    id BIGSERIAL PRIMARY KEY,

    tipo_crt_mf    VARCHAR(5),
    stat_crt_mf    INTEGER,
    suc            VARCHAR(120),
    fecha          DATE,
    hrs            TIME,
    concepto       VARCHAR(255),
    crt            VARCHAR(30),
    monto_crt_mf   NUMERIC(14,2),
    nom_usu        VARCHAR(150),
    btn_detalle    TEXT,

    branch_id      INTEGER,
    loaded_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cortes_movimientos_fecha
    ON cortes_movimientos(fecha);

CREATE INDEX IF NOT EXISTS idx_cortes_movimientos_suc
    ON cortes_movimientos(suc);

CREATE INDEX IF NOT EXISTS idx_cortes_movimientos_crt
    ON cortes_movimientos(crt);

CREATE INDEX IF NOT EXISTS idx_cortes_movimientos_branch_id
    ON cortes_movimientos(branch_id);

CREATE INDEX IF NOT EXISTS idx_cortes_movimientos_stat
    ON cortes_movimientos(stat_crt_mf);



DROP TABLE IF EXISTS resumen_diario;

CREATE TABLE resumen_diario (
    id BIGSERIAL PRIMARY KEY,

    dob_c         DATE,
    num_cuentas   INTEGER,
    num_clientes  INTEGER,
    descu         NUMERIC(14,2),
    sub           NUMERIC(14,2),

    branch_id     INTEGER,
    loaded_at     TIMESTAMP DEFAULT NOW()
);


CREATE INDEX idx_resumen_diario_dob_c
    ON resumen_diario(dob_c);

CREATE INDEX idx_resumen_diario_branch_id
    ON resumen_diario(branch_id);


DROP TABLE IF EXISTS catalogo_articulos;

CREATE TABLE catalogo_articulos (
    id_art_c        INTEGER PRIMARY KEY,
    nom_art_c       VARCHAR(150),
    super_art_c     VARCHAR(150),

    c_art_c         INTEGER,
    cant            INTEGER,
    ord_art_c       INTEGER,

    stat_art_c      INTEGER,
    es_v_art_c      INTEGER,
    es_alcol_art_c  INTEGER,

    loaded_at       TIMESTAMP DEFAULT NOW()
);


CREATE INDEX idx_cat_art_nom
    ON catalogo_articulos(nom_art_c);

CREATE INDEX idx_cat_art_super
    ON catalogo_articulos(super_art_c);

CREATE INDEX idx_cat_art_status
    ON catalogo_articulos(stat_art_c);
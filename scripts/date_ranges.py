from datetime import date, datetime, timedelta


def parse_date(value):
    return datetime.strptime(value, "%Y/%m/%d").date()


def format_date_slash(value):
    return value.strftime("%Y/%m/%d")


def iter_days(fecha_inicio, fecha_fin):
    current = fecha_inicio
    while current <= fecha_fin:
        yield format_date_slash(current)
        current += timedelta(days=1)



def get_range(mode):
    today = date.today()

    if mode == "daily":
        d = today - timedelta(days=1)
        return d, d
    
    if mode == "daily_yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday, yesterday

    if mode == "weekly":
        end = today - timedelta(days=1)
        start = end - timedelta(days=6)
        return start, end

    if mode == "biweekly":
        end = today - timedelta(days=1)
        start = end - timedelta(days=14)
        return start, end

    if mode == "monthly":
        end = today - timedelta(days=1)
        start = end.replace(day=1)
        return start, end

    raise ValueError(f"Modo no soportado: {mode}")
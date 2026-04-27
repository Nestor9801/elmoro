import argparse
from datetime import datetime

from etl import get_valid_session
from date_ranges import get_range, parse_date
from runners.transactional import run_transaccionales
from runners.catalogs import run_catalogos


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["daily_yesterday","daily", "weekly", "biweekly", "monthly", "custom", "catalogs"],
        required=True,
    )

    parser.add_argument("--fecha-inicio")
    parser.add_argument("--fecha-fin")

    args = parser.parse_args()

    session = get_valid_session()

    if args.mode == "catalogs":
        run_catalogos(session)
        return

    if args.mode == "custom":
        if not args.fecha_inicio or not args.fecha_fin:
            raise ValueError("Para --mode custom debes enviar --fecha-inicio y --fecha-fin")

        fecha_inicio = parse_date(args.fecha_inicio)
        fecha_fin = parse_date(args.fecha_fin)

    else:
        fecha_inicio, fecha_fin = get_range(args.mode)

    print(f"[{datetime.now()}] Ejecutando modo {args.mode}: {fecha_inicio} a {fecha_fin}")

    run_transaccionales(
        session=session,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )


if __name__ == "__main__":
    main()
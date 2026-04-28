import gspread
import pandas as pd


def get_client(credentials_path: str):
    return gspread.service_account(filename=credentials_path)


def read_sheet(client, spreadsheet_id: str, worksheet_name: str) -> pd.DataFrame:
    sheet = client.open_by_key(spreadsheet_id)
    ws = sheet.worksheet(worksheet_name)

    data = ws.get_all_records()
    return pd.DataFrame(data)
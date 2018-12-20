import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_all_cards():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
        ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Gacha").worksheet('cards')

    cards = sheet.get_all_records()
    return cards

def get_all_series():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
        ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Gacha").worksheet('series')

    series = sheet.get_all_records()
    return series
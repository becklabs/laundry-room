from googleapiclient import discovery
import google.oauth2.service_account

class MySheet:
    def __init__(self, spreadsheet_id):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = google.oauth2.service_account.Credentials.from_service_account_file(
            'client_secret.json',
            scopes=SCOPES)
        self.service = discovery.build('sheets', 'v4', credentials=credentials)
        self.spreadsheet_id = spreadsheet_id
    
    def append(self, values):
        request = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='Sheet1!A:A',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body= {
            "majorDimension": "ROWS",
            "values": [[i] for i in values],
            })
        return request.execute()

#sheets = MySheet('my-spreadsheet-id')
#print(sheets.append(['Row 1', 'Row 2', 'Row 3']))



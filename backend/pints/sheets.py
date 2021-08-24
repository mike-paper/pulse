import os
import json
import string
import datetime
import pandas as pd
import time
# from googleapiclient import discovery
# from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from google.oauth2 import service_account
from logger import logger

j = os.environ.get('PAPER_GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
if j:
    service_account_info = json.loads(j)
    service_account_info['private_key'] = service_account_info['private_key'].replace('\\n', '\n')
    # service_account_info = j
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info)

LIMIT_ERROR = 'action would increase the number of cells in the workbook above the limit'
FULL_LIMIT_ERROR = 'This action would increase the number of cells in the workbook above the limit of 5000000 cells.'

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

alpha1 = dict(enumerate(string.ascii_lowercase, 1))
alpha2 = {}
i = 27
for v in alpha1.values():
    for v2 in alpha1.values():
        alpha2[i] = v+v2
        i+=1
alphabet = alpha1.copy()
alphabet.update(alpha2)
alphabetRev = {}
for k in alphabet.keys():
    alphabetRev[alphabet[k]] = k

def test(spreadsheetId):
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    d2 = {
        'df': df,
        'spreadsheetId': spreadsheetId,
        'startCell': 'B2',
        'sheet': 'test'
    }
    push(d2)
    return True

def pushAll(data, ssId):
    sheetNames = ['pulse_mrr', 'pulse_churn', 'pulse_customers']
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=d)
    for d in data:
        d2 = {
            'df': d['df'],
            'spreadsheetId': data['spreadsheetId'],
            'startCell': 'A1',
            'sheet': d['sheet']
        }
        push(d2)
    return True

def push(d):
    logger.info(f"sheets push...")
    df = d['df']
    totalRowsReturned = len(df)
    logger.info(f"sheets push rows: {totalRowsReturned}")
    df_dtypes = df.dtypes.to_dict()
    discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = build('sheets', 'v4', credentials=credentials, discoveryServiceUrl=discoveryUrl)
    # k = 'AIzaSyCvXb3IvQ4hk1CT-i447TA8NqzHtfM3W-Q'
    # service = build('sheets', 'v4', developerKey=k, discoveryServiceUrl=discoveryUrl)
    sheetName = d['sheet']
    spreadsheetId = d['spreadsheetId']
    startCell = d.get('startCell', 'A1')
    if len(startCell) < 2:
        startCell = 'A1'
        startCol = 'A'
        startRow = '1'
    elif hasNumbers(startCell[:2]):
        startCol = startCell[:1]
        startRow = startCell[1:]
    else:
        startCol = startCell[:2]
        startRow = startCell[2:]
    startColStr = startCol.upper()
    startCol = alphabetRev.get(startCol.lower(), 1)
    try:
        startRowNum = int(float(startRow))
    except:
        startRowNum = 1
    try:
        startColNum = int(float(startCol))
    except:
        startColNum = 1
    endRow = len(df.values) + startRowNum
    endCol = len(df.columns.tolist())+(startCol-1)
    if endCol == 0:
        return {'ok': False, 'reason': 'No columns', 'error': 'No columns'}
    endCol = alphabet[endCol].upper()
    endCell = endCol + str(endRow)
    rangeName = sheetName + '!' + startCell + ':' + endCell
    print('writing DF to sheets', rangeName, startCol, endCol,  flush = True)
    clearRangeName = sheetName + '!' + startCell + ':' + endCol
    clearSheetRangeName = sheetName
    colNames = df.columns.tolist()
    df = df.to_json(date_format = 'iso', orient='values', 
        default_handler=str)
    df = json.loads(df, strict=False)
    body = {
        'values': [colNames] + df
    }
    try: #try to clear the sheet, this also checks it exists
        result = service.spreadsheets().values().clear(
            spreadsheetId=spreadsheetId, range=clearRangeName, body={}).execute()
        print('cleared cols...', flush=True)
    except Exception as e: #if couldnt clear, check  if it's bc the sheet doesnt exist and add it
        print('googleapiclient.errors ', e, flush=True)
        e = str(e)
        if 'Unable to parse range' in e:
            newSheet = {
                "requests": {
                    "addSheet": {
                        "properties": {
                        "title": sheetName,
                        "gridProperties": {
                            "rowCount": 1000,
                            "columnCount": 100
                        },
                        "tabColor": {
                            "red": 0.0,
                            "green": 0.0,
                            "blue": 0.0
                        }
                        }
                    }
                }
            }
            try:
                result = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=newSheet).execute()
                print('add sheet result ', result, flush=True)
            except Exception as e: #if couldnt add sheet, check if it's bc 5m cell limit
                if LIMIT_ERROR in str(e):
                    return {'ok': False, 'reason': FULL_LIMIT_ERROR, 'error': str(e)}
                else:
                    return {'ok': False, 'reason': 'unknown', 'error': str(e)}
    writeResultsTry = 0
    result = False
    writeResultsToTry = 6
    while writeResultsTry <= writeResultsToTry:
        try:
            # result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheetId, range=rangeName,
                valueInputOption='USER_ENTERED', body=body).execute()
            print('write successful...', flush=True)
            writeResultsTry = 100
        except Exception as e:
            print('writeResultsTry #', writeResultsTry, e, flush = True)
            writeResultsTry+=1
            if LIMIT_ERROR in str(e):
                return {'ok': False, 'reason': FULL_LIMIT_ERROR, 'error': str(e)}
            if 'Invalid values' in str(e) and 'struct_value' in str(e):
                return {'ok': False, 'reason': 'JSON data in results', 'error': str(e)}
            if 'Invalid values' in str(e) and 'list_value' in str(e):
                return {'ok': False, 'reason': 'List / array in results', 'error': str(e)}
            if 'caller does not have permission' in str(e):
                return {'ok': False, 'reason': 'The caller does not have permission', 'error': str(e)}
            if writeResultsTry == writeResultsToTry:
                return {'ok': False, 'reason': 'maxAttempts', 'error': str(e)}
                # raise
            time.sleep(2)
    lastRunDt = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    note = f'Pulse updated {len(df)} rows at {lastRunDt} UTC\n\nMore info at https://pulse.trypaper.io/?ref=sheets'
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheetId = [sheet['properties']['sheetId'] for sheet in sheet_metadata['sheets'] if sheet['properties']['title'] == sheetName]
    if len(sheetId) == 0:
        return {'ok': True}
    body = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheetId[0],
                        "startRowIndex": startRowNum-1,
                        "endRowIndex": startRowNum,
                        "startColumnIndex": startColNum-1,
                        "endColumnIndex": startColNum,
                    },
                    "cell": {"note": note},
                    "fields": "note",
                }
            }
        ]
    }
    try:
        result = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheetId, body=body).execute()
        print('wrote note to sheet...', flush=True)
    except Exception as e:
        print('error writing note ', e, flush=True)
    return {'ok': True}
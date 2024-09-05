from typing import Final as Constant
from pydantic import HttpUrl, FilePath
from os import getenv
from taxi_data_core.common import actions as CommonActions
from taxi_data_core.google_sheets import actions as SheetsActions
from datetime import datetime
from types import LambdaType

READ_ONLY_SCOPE: Constant[HttpUrl] = "https://www.googleapis.com/auth/spreadsheets.readonly"
READ_WRITE_SCOPE: Constant[HttpUrl] = 'https://www.googleapis.com/auth/spreadsheets'

SPREADSHEET_ID: Constant[str] = '148J47DO_RZe-bbCbN_1yyqHB6MWS9JNKjvjPsg_5wlA'
CREDENTIALS_FILE: Constant[FilePath] = FilePath(f'{getenv("HOME")}/sheets-api-credentials.json')

TOTALS_RANGE: Constant[str] = 'Totals!B5:G5'
DOCKETS_RANGE: Constant[str] = 'Dockets!A2:W'
VOUCHERS_RANGE: Constant[str] = 'Vouchers!A2:I'
CABCHARGE_RANGE: Constant[str] = 'Cabcharge!A2:G'
EFT_STATEMENT_RANGE: Constant[str] = 'EFTPOS Statements!A2:D'
DOCKET_STATEMENT_RANGE: Constant[str] = 'Docket Statements!A2:E'

LAMBDA_CONVERT_TO_FLOAT: Constant[LambdaType] = lambda x: CommonActions.string_to_float(x) if x else 0.0
LAMBDA_CONVERT_JOB_NUMBER: Constant[LambdaType] = lambda x: 0 if x == "Various" or x == '' else int(x)
LAMBDA_CONVERT_TIME: Constant[LambdaType] = lambda x: datetime.strptime(x, '%H:%M') if x else None
LAMBDA_CONVERT_COLLECTED_VOUCHER: Constant[LambdaType] = lambda x: SheetsActions.set_docket_status("Completed") if x == "Collected" else SheetsActions.set_docket_status(x)
LAMBDA_NONE_IF_EMPTY_ELSE_INT: Constant[LambdaType] = lambda x: None if x == '' else int(x)
LAMBDA_STATEMENT_TYPE: Constant[LambdaType] = lambda x: CommonActions.set_statement_type(x.rstrip("1")) if x.endswith("1") else CommonActions.set_statement_type(x)

from typing import Tuple, List, Optional, Union, Dict
from pydantic import HttpUrl, FilePath
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

from taxi_data_core.google_sheets import constants as SheetsConstants
from taxi_data_core.common import constants as CommonConstants
from taxi_data_core.google_sheets import schema as Schema
from taxi_data_core.common import actions as CommonActions

def set_docket_status(status: str) -> Schema.DocketStatus:
    """
    Set the DocketStatus to the correct object based on a string input.

    Args:
        status (str): The status string to convert to DocketStatus.

    Returns:
        DocketStatus: The corresponding DocketStatus object.

    Raises:
        ValueError: If the provided status is not valid.
    """
    match status.strip().capitalize():
        case "Completed":
            return Schema.DocketStatus.COMPLETED
        case "Lodged":
            return Schema.DocketStatus.LODGED
        case "Logged":
            return Schema.DocketStatus.LOGGED
        case "Paid":
            return Schema.DocketStatus.PAID
        case "Disputed":
            return Schema.DocketStatus.DISPUTED
        case "Finalised":
            return Schema.DocketStatus.FINALISED
        case _:
            # Raise an exception with an additional note for invalid status
            error = ValueError(f"Invalid status '{status}'. Must be one of: Completed, Lodged, Logged, Paid, Disputed, Finalised.")
            error.add_note(
                "Please provide a valid status from the DocketStatus options."
            )
            raise error

def set_docket_type(docket_type: str) -> Schema.DocketType:
    """
    Set the DocketType to the correct object based on a string input.

    Args:
        docket_type (str): The docket type string to convert to DocketType.

    Returns:
        DocketType: The corresponding DocketType object.

    Raises:
        ValueError: If the provided docket type is not valid.
    """
    match docket_type.strip().capitalize():
        case "App booking":
            return Schema.DocketType.APP_BOOKING
        case "Bwc account":
            return Schema.DocketType.ACCOUNT
        case "Dva":
            return Schema.DocketType.DVA
        case "Ndis":
            return Schema.DocketType.NDIS
        case "Pre paid":
            return Schema.DocketType.PRE_PAID
        case "Groups":
            return Schema.DocketType.GROUPS
        case "Internal":
            return Schema.DocketType.INTERNAL
        case _:
            # Raise an exception with an additional note for invalid docket type
            error = ValueError(
                f"Invalid docket type '{docket_type}'. Must be one of: App booking, BWC Account, DVA, NDIS, Pre Paid, Groups, Internal."
            )
            error.add_note(
                "Please provide a valid docket type from the DocketType options."
            )
            raise error

def set_voucher_type(voucher_type: str) -> Schema.VoucherType:
    """
    Set the VoucherType to the correct object based on a string input.

    Args:
        voucher_type (str): The voucher type string to convert to VoucherType.

    Returns:
        VoucherType: The corresponding VoucherType object.

    Raises:
        ValueError: If the provided voucher type is not valid.
    """
    match voucher_type.strip().capitalize():
        case "Pre-paid":
            return Schema.VoucherType.PRE_PAID
        case "Interstate tss":
            return Schema.VoucherType.INTERSTATE_TSS
        case "Manual eft":
            return Schema.VoucherType.MANUAL_EFT
        case "Manual tss":
            return Schema.VoucherType.MANUAL_TSS
        case _:
            # Raise an exception with an additional note for invalid voucher type
            error = ValueError(
                f"Invalid voucher type '{voucher_type}'. Must be one of: pre-paid, interstate TSS, Manual EFT, Manual TSS."
            )
            error.add_note(
                "Please provide a valid voucher type from the VoucherType options."
            )
            raise error

def initialize_sheets(SCOPES: Tuple[HttpUrl], credentials_file: FilePath) -> Resource:
    creds = None
    try:
        # Try to load existing credentials
        creds = Credentials.from_authorized_user_file(credentials_file, SCOPES)
    except (ValueError, FileNotFoundError):
        # If credentials file does not exist or is in the wrong format, create new credentials
        pass

    # If there are no valid credentials available, initiate the authorization flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the credentials if expired
            creds.refresh(Request())
        else:
            # Run the OAuth flow to get new credentials
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)

            # Save the newly authorized credentials to the credentials file
            with open(credentials_file, "w") as token:
                token.write(creds.to_json())

    try:
        # Build the service object
        service = build("sheets", "v4", credentials=creds)
        sheets_app: Resource = service.spreadsheets()
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

    return sheets_app

def get_range(app: Resource, spreadsheetId: str, range: str) -> List[List[str]]:
    result = app.values().get(spreadsheetId=spreadsheetId, range=range).execute()
    return result.get("values", [])

def parse_date_or_string(value: Optional[Union[str, datetime]], date_format: str = "%Y-%m-%d") -> Optional[Union[str, datetime]]:
    """
    Parses a value to return a datetime object if the string is a valid date,
    otherwise returns the string or None if it's empty.
    
    Args:
    - value (Optional[Union[str, datetime]]): The value to be parsed.
    - date_format (str): The format to use for date parsing.
    
    Returns:
    - Optional[Union[str, datetime]]: Parsed datetime object, original string, or None.
    """
    if not value:  # None or empty string case
        return None
    if isinstance(value, datetime):  # Already a datetime
        return value
    try:
        # Try to parse it as a datetime
        return datetime.strptime(value, date_format)
    except (ValueError, TypeError):
        # If parsing fails, return it as a string
        return value


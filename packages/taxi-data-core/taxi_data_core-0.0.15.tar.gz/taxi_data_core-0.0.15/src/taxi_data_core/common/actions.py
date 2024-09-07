from platform import system
from shutil import which
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.service import Service as EdgeService

from taxi_data_core.common import schema as Schema

def set_browser() -> webdriver:
    # Detect the operating system
    os_name = system().lower()
    
    # Initialize a list to check available browsers in priority order
    available_browsers = []

    # Check for Firefox
    if which("firefox"):
        available_browsers.append('firefox')
    
    # Check for Chrome/Chromium
    if which("chrome") or which("chromium"):
        available_browsers.append('chrome')
    
    # Check for Safari (only available on macOS)
    if os_name == "darwin" and which("safaridriver"):
        available_browsers.append('safari')
    
    # Check for Microsoft Edge (only available on Windows)
    if os_name == "windows" and which("msedge"):
        available_browsers.append('edge')

    # Initialize WebDriver in priority order: Firefox > Chrome > Safari > Edge
    if 'firefox' in available_browsers:
        return webdriver.Firefox(service=FirefoxService())
    elif 'chrome' in available_browsers:
        return webdriver.Chrome(service=ChromeService())
    elif 'safari' in available_browsers:
        return webdriver.Safari(service=SafariService())
    elif 'edge' in available_browsers:
        return webdriver.Edge(service=EdgeService())
    else:
        raise EnvironmentError("No supported browsers found on the system. Please install Firefox, Chrome, Safari, or Edge.")

def string_to_float(string: str) -> float:

    # Regular expression to validate the string as a valid dollar amount
    pattern = r'^\$?-?\d{1,3}(,\d{3})*(\.\d{2})?$'

    # Check if the string matches the dollar amount pattern
    if not re.match(pattern, string):
        raise ValueError("Invalid string. Converstion to float must be a Currency value")
    # Create a translation table that maps '$' and ',' to None
    translation_table = str.maketrans('', '', '$,')

    # Apply the translation table to remove unwanted characters
    cleaned_string = string.translate(translation_table)

    # Convert the cleaned string to a float
    converted_float = float(cleaned_string)

    return converted_float

def set_statement_type(statement_type: str) -> Schema.StatementType:
    """
    Set the StatementType to the correct object based on a string input.

    Args:
        statement_type (str): The statement_type string to convert to StatementType.

    Returns:
        StatementType: The corresponding StatementType object.

    Raises:
        ValueError: If the provided statement_type is not valid.
    """
    match statement_type.strip().upper():
        case "AC":
            return Schema.StatementType.ACCOUNT
        case "VOU":
            return Schema.StatementType.VOUCHER
        case "GRP":
            return Schema.StatementType.GROUP
        case "DV2":
            return Schema.StatementType.DVA
        case "NDI":
            return Schema.StatementType.NDIS
        case "DKT":
            return Schema.StatementType.DOCKET
        case _:
            # Raise an exception with an additional note for invalid statement_type
            error = ValueError(f"Invalid statement_type '{statement_type}'. Must be one of: AC, VOU, GRP, DV2, NDI.")
            error.add_note(
                "Please provide a valid statement_type from the StatementType options."
            )
            raise error
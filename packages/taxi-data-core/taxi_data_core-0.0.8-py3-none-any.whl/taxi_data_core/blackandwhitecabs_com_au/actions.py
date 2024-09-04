from selenium import webdriver
from taxi_data_core.blackandwhitecabs_com_au import constants as BwcConstants
from taxi_data_core.common import constants as CommonConstants
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from taxi_data_core.common.actions import set_browser
from datetime import datetime
from taxi_data_core.blackandwhitecabs_com_au import schema as Schema
from bs4.element import Tag
from typing import Tuple
from pydantic import HttpUrl
import re

def login() -> webdriver.Firefox:
    
    #browser = webdriver.Firefox()
    browser = set_browser()
    # Open the login page
    browser.get(BwcConstants.WEB_UI_URL)

    # Log in
    username = browser.find_element(By.ID, BwcConstants.ID_USERNAME_FIELD)
    password = browser.find_element(By.ID, BwcConstants.ID_PASSWORD_FIELD)

    username.send_keys(BwcConstants.WEB_UI_USERNAME)
    password.send_keys(BwcConstants.WEB_UI_PASSWORD)

    login_button = browser.find_element(By.ID, BwcConstants.ID_LOGON_BUTTON)
    login_button.click()
    return browser

def close_last_login_window(browser: webdriver.Firefox) -> None:

    # Wait for the page to load and close last login dialog
    WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, BwcConstants.CLASS_LAST_LOGIN_MSG_CLOSE)))
    last_login_close = browser.find_element(By.CLASS_NAME, BwcConstants.CLASS_LAST_LOGIN_MSG_CLOSE)
    last_login_close.click()
    
def select_operator_from_drop_down(browser: webdriver) -> None:

    # Wait for operator page to load then select operator and click on car
    WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_OPERATOR)))
    operator_menu = Select(browser.find_element(By.ID, BwcConstants.ID_OPERATOR))
    operator_menu.select_by_visible_text(BwcConstants.TEXT_WAYNE_BENNETT)

def shifts_for_vehicle_set_date_range(browser: webdriver, from_date: datetime, to_date: datetime) -> None:

    WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_SHIFTS_FOR_VEHICLE)))
    from_date_field = browser.find_element(By.ID, BwcConstants.ID_FROM_DATE)
    from_date_field.clear()
    from_date_field.send_keys(datetime.strftime(from_date, BwcConstants.MONTH_FIRST_DATE_FORMAT))
    to_date_field = browser.find_element(By.ID, BwcConstants.ID_TO_DATE)
    to_date_field.clear()
    to_date_field.send_keys(datetime.strftime(to_date, BwcConstants.MONTH_FIRST_DATE_FORMAT))
    go_button = browser.find_element(By.XPATH, BwcConstants.XPATH_GO_BUTTON)
    go_button.click()

    #Wait for filtered list to load and click on shift
    WebDriverWait(browser, CommonConstants.SHORT_TIMEOUT).until(EC.presence_of_element_located((By.ID, BwcConstants.ID_SHIFTS_FOR_VEHICLE)))

def use_nav_menu(browser: webdriver, link_text: str) -> None:

    # Go to Vehicle for operator page
    jobs_link = browser.find_element(By.LINK_TEXT, link_text)
    jobs_link.click()

def initialize_browser() -> webdriver:
    browser = login()
    close_last_login_window(browser)
    return browser

def set_statement_type(type: str) -> Schema.StatementType:
    match type:
        case "VOU":
            return Schema.StatementType.VOUCHER
        case "GRP":
            return Schema.StatementType.GROUP
        case "DV2":
            return Schema.StatementType.DVA
        case "AC":
            return Schema.StatementType.ACCOUNT
        case "NDI":
            return Schema.StatementType.NDIS
        case _:
            raise Exception.add_note("Statement Type not defined")

def url_from_cell(cell: Tag, url_prefix: str) -> Tuple[HttpUrl, str]:
    """
    Extract both URL and text from the hyperlink in the given table cell.

    Args:
        cell (Tag): A BeautifulSoup Tag object representing a <td> element.

    Returns:
        Tuple[str, str]: A tuple containing the extracted URL and text.
    """
    link_tag = cell.find(CommonConstants.TAG_ANCHOR)  # Find the <a> tag within the column
    if link_tag:  # Ensure the <a> tag is found
        link_url = f"{url_prefix}{link_tag[CommonConstants.TAG_HREF]}"  # Extract the href attribute for the URL
        link_text = link_tag.text.strip()  # Extract the displayed text
    else:
        link_url = f"{url_prefix}"
        link_text = cell.text.strip()
    
    return link_url, link_text

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

def set_docket_status(status: str) -> Schema.PaperDocketStatus:
    match status:
        case "Posted":
            return Schema.PaperDocketStatus.POSTED
        case "Pending":
            return Schema.PaperDocketStatus.PENDING
        case _:
            raise Exception.add_note("Docket status not set correctly")
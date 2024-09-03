from selenium import webdriver
from taxi_data_core.blackandwhitecabs_com_au import constants as Constants
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from taxi_data_core.browser_init import set_browser
from datetime import datetime

def login() -> webdriver.Firefox:
    
    #browser = webdriver.Firefox()
    browser = set_browser()
    # Open the login page
    browser.get(Constants.WEB_UI_URL)

    # Log in
    username = browser.find_element(By.ID, Constants.ID_USERNAME_FIELD)
    password = browser.find_element(By.ID, Constants.ID_PASSWORD_FIELD)

    username.send_keys(Constants.WEB_UI_USERNAME)
    password.send_keys(Constants.WEB_UI_PASSWORD)

    login_button = browser.find_element(By.ID, Constants.ID_LOGON_BUTTON)
    login_button.click()
    return browser

def close_last_login_window(browser: webdriver.Firefox) -> None:

    # Wait for the page to load and close last login dialog
    WebDriverWait(browser, Constants.TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, Constants.CLASS_LAST_LOGIN_MSG_CLOSE)))
    last_login_close = browser.find_element(By.CLASS_NAME, Constants.CLASS_LAST_LOGIN_MSG_CLOSE)
    last_login_close.click()
    
def select_operator_from_drop_down(browser: webdriver) -> None:

    # Wait for operator page to load then select operator and click on car
    WebDriverWait(browser, Constants.TIMEOUT).until(EC.presence_of_element_located((By.ID, Constants.ID_OPERATOR)))
    operator_menu = Select(browser.find_element(By.ID, Constants.ID_OPERATOR))
    operator_menu.select_by_visible_text(Constants.TEXT_WAYNE_BENNETT)

def shifts_for_vehicle_set_date_range(browser: webdriver, from_date: datetime, to_date: datetime) -> None:

    WebDriverWait(browser, Constants.TIMEOUT).until(EC.presence_of_element_located((By.ID, Constants.ID_SHIFTS_FOR_VEHICLE)))
    from_date_field = browser.find_element(By.ID, Constants.ID_FROM_DATE)
    from_date_field.clear()
    from_date_field.send_keys(datetime.strftime(from_date, Constants.MONTH_FIRST_DATE_FORMAT))
    to_date_field = browser.find_element(By.ID, Constants.ID_TO_DATE)
    to_date_field.clear()
    to_date_field.send_keys(datetime.strftime(to_date, Constants.MONTH_FIRST_DATE_FORMAT))
    go_button = browser.find_element(By.XPATH, Constants.XPATH_GO_BUTTON)
    go_button.click()

    #Wait for filtered list to load and click on shift
    WebDriverWait(browser, Constants.TIMEOUT).until(EC.presence_of_element_located((By.ID, Constants.ID_SHIFTS_FOR_VEHICLE)))

def use_nav_menu(browser: webdriver, link_text: str) -> None:

    # Go to Vehicle for operator page
    jobs_link = browser.find_element(By.LINK_TEXT, link_text)
    jobs_link.click()


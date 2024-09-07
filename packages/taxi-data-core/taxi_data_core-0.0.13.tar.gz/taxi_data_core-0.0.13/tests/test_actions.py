import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from taxi_data_core.blackandwhitecabs_com_au.actions import (
    login, close_last_login_window, select_operator_from_drop_down,
    shifts_for_vehicle_set_date_range, use_nav_menu, initialize_browser,
    url_from_cell, set_docket_status
)
from taxi_data_core.blackandwhitecabs_com_au import constants as BwcConstants
from taxi_data_core.common import constants as CommonConstants
from taxi_data_core.blackandwhitecabs_com_au import schema as Schema

class TestActions(unittest.TestCase):

    @patch('taxi_data_core.blackandwhitecabs_com_au.actions.set_browser')
    def test_login(self, mock_set_browser):
        mock_browser = MagicMock()
        mock_set_browser.return_value = mock_browser

        browser = login()

        mock_browser.get.assert_called_with(BwcConstants.WEB_UI_URL)
        mock_browser.find_element.assert_any_call(By.ID, BwcConstants.ID_USERNAME_FIELD)
        mock_browser.find_element.assert_any_call(By.ID, BwcConstants.ID_PASSWORD_FIELD)
        mock_browser.find_element.assert_any_call(By.ID, BwcConstants.ID_LOGON_BUTTON)
        self.assertEqual(browser, mock_browser)

    @patch('taxi_data_core.blackandwhitecabs_com_au.actions.WebDriverWait')
    def test_close_last_login_window(self, mock_webdriver_wait):
        mock_browser = MagicMock()
        mock_wait = MagicMock()
        mock_webdriver_wait.return_value = mock_wait

        close_last_login_window(mock_browser)

        mock_wait.until.assert_called_once()
        mock_browser.find_element.assert_called_with(By.CLASS_NAME, BwcConstants.CLASS_LAST_LOGIN_MSG_CLOSE)
        mock_browser.find_element().click.assert_called_once()

    @patch('taxi_data_core.blackandwhitecabs_com_au.actions.WebDriverWait')
    def test_select_operator_from_drop_down(self, mock_webdriver_wait):
        mock_browser = MagicMock()
        mock_wait = MagicMock()
        mock_webdriver_wait.return_value = mock_wait

        # Mock the find_element method to return a mock element with tag_name 'select'
        mock_element = MagicMock()
        mock_element.tag_name = 'select'
        mock_browser.find_element.return_value = mock_element

        # Mock the options in the select element
        mock_option = MagicMock()
        mock_option.text = BwcConstants.TEXT_WAYNE_BENNETT
        mock_element.options = [mock_option]

        select_operator_from_drop_down(mock_browser)

        mock_wait.until.assert_called_once()
        mock_browser.find_element.assert_called_with(By.ID, BwcConstants.ID_OPERATOR)
        mock_select = Select(mock_browser.find_element())
        mock_select.select_by_visible_text.assert_called_with(BwcConstants.TEXT_WAYNE_BENNETT)

    @patch('taxi_data_core.blackandwhitecabs_com_au.actions.WebDriverWait')
    def test_shifts_for_vehicle_set_date_range(self, mock_webdriver_wait):
        mock_browser = MagicMock()
        mock_wait = MagicMock()
        mock_webdriver_wait.return_value = mock_wait
        from_date = datetime(2023, 1, 1)
        to_date = datetime(2023, 1, 31)

        shifts_for_vehicle_set_date_range(mock_browser, from_date, to_date)

        # Adjust the assertion to expect two calls
        self.assertEqual(mock_wait.until.call_count, 2)
        mock_browser.find_element.assert_any_call(By.ID, BwcConstants.ID_FROM_DATE)
        mock_browser.find_element.assert_any_call(By.ID, BwcConstants.ID_TO_DATE)
        mock_browser.find_element.assert_any_call(By.XPATH, BwcConstants.XPATH_GO_BUTTON)
        mock_browser.find_element().clear.assert_called()
        mock_browser.find_element().send_keys.assert_called()
        mock_browser.find_element().click.assert_called_once()

    def test_use_nav_menu(self):
        mock_browser = MagicMock()
        link_text = "Jobs"

        use_nav_menu(mock_browser, link_text)

        mock_browser.find_element.assert_called_with(By.LINK_TEXT, link_text)
        mock_browser.find_element().click.assert_called_once()

    @patch('taxi_data_core.blackandwhitecabs_com_au.actions.login')
    @patch('taxi_data_core.blackandwhitecabs_com_au.actions.close_last_login_window')
    def test_initialize_browser(self, mock_close_last_login_window, mock_login):
        mock_browser = MagicMock()
        mock_login.return_value = mock_browser

        browser = initialize_browser()

        mock_login.assert_called_once()
        mock_close_last_login_window.assert_called_once_with(mock_browser)
        self.assertEqual(browser, mock_browser)

    def test_url_from_cell(self):
        html = '<td><a href="/test">Test Link</a></td>'
        cell = BeautifulSoup(html, 'html.parser').td
        url_prefix = "http://example.com"

        url, text = url_from_cell(cell, url_prefix)

        self.assertEqual(url, "http://example.com/test")
        self.assertEqual(text, "Test Link")

    def test_set_docket_status(self):
        self.assertEqual(set_docket_status("Posted"), Schema.PaperDocketStatus.POSTED)
        self.assertEqual(set_docket_status("Pending"), Schema.PaperDocketStatus.PENDING)
        with self.assertRaises(Exception):
            set_docket_status("Invalid")

if __name__ == '__main__':
    unittest.main()
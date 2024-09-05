from selenium import webdriver
from taxi_data_core.nextechgps_com import constants as GpsConstants
from taxi_data_core.common import constants as CommonConstants
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from taxi_data_core.nextechgps_com.schema import PlaybackSpeed, PlaybackButtons, RawEvent
from selenium.webdriver.common.action_chains import ActionChains
from typing import List, Tuple
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, UnexpectedAlertPresentException
from os import rename, getenv
from typing import Final
from taxi_data_core.common.actions import set_browser
from pathlib import Path
from time import time, sleep

def login() -> webdriver:
    driver: webdriver = set_browser()

    # Open the login page
    driver.get(GpsConstants.WEB_UI_URL)

    iframe = driver.find_element(By.ID, GpsConstants.ID_LOGIN_IFRAME)
    driver.switch_to.frame(iframe)

    # Log in
    username = driver.find_element(By.ID, GpsConstants.ID_USERNAME_FIELD)
    password = driver.find_element(By.ID, GpsConstants.ID_PASSWORD_FIELD)

    username.send_keys(GpsConstants.WEB_UI_USERNAME)
    password.send_keys(GpsConstants.WEB_UI_PASSWORD)

    login_button = driver.find_element(By.ID, GpsConstants.ID_LOGIN_BUTTON)
    login_button.click()
    return driver

def switch_to_main_box_iframe(driver: webdriver) -> None:
    WebDriverWait(driver, CommonConstants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.ID, GpsConstants.ID_MAIN_BOX_IFRAME)))
    iframe = driver.find_element(By.ID, GpsConstants.ID_MAIN_BOX_IFRAME)
    driver.switch_to.frame(iframe)
    
def click_on_tracker(driver) -> WebElement:

    #Wait for device list to load
    WebDriverWait(driver, CommonConstants.LONG_TIMEOUT).until(EC.presence_of_element_located((By.ID, GpsConstants.ID_DEVICE_LIST)))
    tracker = driver.find_element(By.ID, GpsConstants.ID_DEVICE_LIST)

    # Click on device
    element_to_click = tracker.find_element(By.XPATH, GpsConstants.XPATH_GPS_TRACKER)
    WebDriverWait(tracker, CommonConstants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, GpsConstants.XPATH_GPS_TRACKER)))
    element_to_click.click()

    return tracker

def nav_to_tracking_report(driver: webdriver, tracker: WebElement) -> None:
    #Click on more
    element_to_click = tracker.find_element(By.XPATH, GpsConstants.XPATH_MORE_OPTIONS)
    WebDriverWait(tracker, 60).until(EC.presence_of_element_located((By.XPATH, GpsConstants.XPATH_MORE_OPTIONS)))
    element_to_click.click()

    #Click on tracking report
    element_to_click = tracker.find_element(By.XPATH, GpsConstants.XPATH_TRACKING_REPORT)
    WebDriverWait(tracker, 60).until(EC.presence_of_element_located((By.XPATH, GpsConstants.XPATH_TRACKING_REPORT)))
    element_to_click.click()

    # Wait for report download window to load
    WebDriverWait(driver, CommonConstants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.ID, GpsConstants.ID_REPORT_DOWNLOAD_WINDOW)))
    iframe = driver.find_element(By.ID, GpsConstants.ID_REPORT_DOWNLOAD_WINDOW)
    driver.switch_to.frame(iframe)
    
def set_tracking_report_date_and_go(driver: webdriver, date: str, destination: str) -> Path | None:

    downloads_folder: Final[str] = f"{getenv('HOME')}/Downloads"
    #parent_dir: Final[str] = f"{getenv('HOME')}/taxi_data"
    file_name: Final[str] = f"{GpsConstants.FILE_NAME_STRING}{date}.kml"

    old_name: Final[Path] = f"{downloads_folder}/{file_name}"
    new_name: Final[Path] = f"{destination}/{file_name}"

    if not Path(new_name).exists():
        #Find date field and enter date
        WebDriverWait(driver, CommonConstants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, GpsConstants.CLASS_DOWNLOAD_DATE)))
        date_box = driver.find_element(By.CLASS_NAME, GpsConstants.CLASS_DOWNLOAD_DATE)
        date_box.clear()
        date_box.send_keys(date)

        driver.find_element(By.ID, GpsConstants.ID_DOWNLOAD_GO_BUTTON).click()
    

        rename(old_name,new_name)
        return new_name
    else:
        return None

def open_playback(driver: webdriver, tracker: WebElement) -> None:
        # Store the current window handle
        main_window = driver.current_window_handle
        #driver.switch_to.default_content()
        iframe = driver.find_element(By.ID, GpsConstants.ID_MAIN_BOX_IFRAME)
        driver.switch_to.frame(iframe)

        # Click Playback
        tracker = driver.find_element(By.ID, GpsConstants.ID_DEVICE_LIST)
        tracker.find_element(By.XPATH, GpsConstants.XPATH_PLAYBACK_BUTTON).click()

        #Wait for tab to load
        WebDriverWait(driver, CommonConstants.DEFAULT_TIMEOUT).until(EC.new_window_is_opened([main_window]))

        # Get all window handles (there should be two now)
        window_handles = driver.window_handles
        # Switch to the new window handle
        for handle in window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                break
        
        #Wait for playback page to load
        WebDriverWait(driver, CommonConstants.DEFAULT_TIMEOUT).until(EC.presence_of_element_located((By.ID, GpsConstants.ID_PLAYBACK_START_DATE)))

def set_playback_date(driver: webdriver, date: str) -> None:

        #Find date boxes and enter date
        date_box = driver.find_element(By.ID, GpsConstants.ID_PLAYBACK_START_DATE)
        date_box.clear()
        date_box.send_keys(f"{date} 00:00")   

        date_box = driver.find_element(By.ID, GpsConstants.ID_PLAYBACK_END_DATE)
        date_box.clear()
        date_box.send_keys(f"{date} 23:59")
    
def set_plaback_speed(driver: webdriver, speed: PlaybackSpeed) -> None:

        # Play speed slow
        slider = driver.find_element(By.ID, GpsConstants.ID_SLIDER)    
        # Initialize ActionChains
        actions = ActionChains(driver)

        match speed:
            case PlaybackSpeed.FAST:
                offset = -slider.size['width']
            case PlaybackSpeed.SLOW:
                offset = slider.size['width']
            case _:
                raise "Slider offset not correctly set"
        # Move the slider to the right by clicking and dragging
        actions.click_and_hold(slider).move_by_offset(offset, 0).release().perform()
    
def get_info_pane_text(driver: webdriver, 
                   playback_buttons: PlaybackButtons) -> str | None:

    def get_info_pane(driver: webdriver) -> WebElement:
        info_pane: WebElement = driver.find_element(By.XPATH, GpsConstants.XPATH_INFO_PANE)
    
        if info_pane.text != None:
#                text = info_pane.text
            return info_pane    

    try:
        text = None
        WebDriverWait(driver, CommonConstants.DEFAULT_TIMEOUT).until(EC.element_to_be_clickable((By.ID, GpsConstants.ID_PAUSE_BUTTON)))
        playback_buttons.Pause.click()

        info_pane: WebElement = get_info_pane(driver)

    except TimeoutException:
        try:
            driver.switch_to.alert.accept()
        except NoAlertPresentException:
            info_pane: WebElement = get_info_pane(driver)
            return info_pane.text         

    return info_pane.text

def get_playback_buttons(driver: webdriver) -> PlaybackButtons:
   
    play_button = driver.find_element(By.ID, GpsConstants.ID_PLAY_BUTTON)
    pause_button = driver.find_element(By.ID, GpsConstants.ID_PAUSE_BUTTON)
    continue_button = driver.find_element(By.ID, GpsConstants.ID_CONTINUE_BUTTON)
    
    return PlaybackButtons(Play=play_button, Continue=continue_button, Pause=pause_button)

def play_to_end(driver: webdriver, playback_buttons: PlaybackButtons) -> None:

    playback_buttons.Play.click()
    WebDriverWait(driver, CommonConstants.JUST_FUCKING_WAIT_TIMEOUT).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    driver.switch_to.default_content()
   
def get_raw_events(driver: webdriver) -> List[RawEvent]:

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    events_table = soup.find(CommonConstants.TAG_TABLE, {CommonConstants.TAG_ID: GpsConstants.ID_EVENT_LIST})
    raw_events = []

    for row in events_table.find_all(CommonConstants.TAG_ROW)[CommonConstants.SLICE_REMOVE_HEADER]:  # Skip header  & Footer row
        cols = row.find_all(CommonConstants.TAG_COLUMN)
        event = RawEvent(event_type=cols[0].text.strip(),
                from_time=cols[1].text.strip(),
                to_time=cols[2].text.strip(),
                duration=cols[3].text.strip())
        raw_events.append(event)

    return raw_events

def setup_playback(driver: webdriver, shift_date: str) -> PlaybackButtons:

    set_playback_date(driver, date=shift_date)
    set_plaback_speed(driver, speed=PlaybackSpeed.SLOW)
    playback_buttons = get_playback_buttons(driver)

    return playback_buttons

def nav_to_playback(shift_date: str) -> webdriver:
    driver = login()
    driver.switch_to.default_content()
    switch_to_main_box_iframe(driver)
    tracker = click_on_tracker(driver)
    nav_to_tracking_report(driver, tracker)
    set_tracking_report_date_and_go(driver, date=shift_date)
    driver.switch_to.default_content()
    open_playback(driver, tracker)

    return driver

def get_raw_data(driver: webdriver, playback_buttons: PlaybackButtons) -> List[str]:

    raw_data = []

    playback_buttons.Play.click()
    # Get First Entry
    raw_data.append(get_info_pane_text(driver, playback_buttons))

    # Locate the div element 
    location_pin: WebElement = driver.find_element(By.XPATH, GpsConstants.XPATH_GREEN_LOCATION_PIN)

    # Get the initial position
    initial_left = location_pin.value_of_css_property('left')
    initial_top = location_pin.value_of_css_property('top')

    # Continuous loop
    i = 0
    while True:
        try:
            
            # Check if alert is present
            alert = driver.switch_to.alert
            print("Alert is present!")
            break  # Exit the loop if the alert is found
        except NoAlertPresentException:
            try:
                print("No alert present yet...")
                # If continue is disabled break
                if playback_buttons.Continue.is_enabled() == True:
                    playback_buttons.Continue.click()  
                    if i > CommonConstants.LOOP_LIMIT:
                        break 
                else:
                    break

                current_left = initial_left
                current_top = initial_top

                initial_left, initial_top = wait_for_pin_movement(driver, initial_left, initial_top)

                if current_left == initial_left and current_top == initial_top:
                    i += 1               
                else:
                    i = 0               

                raw_data.append(get_info_pane_text(driver, playback_buttons))

            except UnexpectedAlertPresentException:
                break
    return raw_data

def wait_for_pin_movement(driver: webdriver, initial_left: int, initial_top: int, timeout: int = CommonConstants.SHORT_TIMEOUT) -> Tuple[int, int]:

    start_time = time()  # Record the start time

    spinner = ['|', '/', '-', '\\']  # Spinner characters for the animation
    spinner_index = 0  # Initial spinner index

    while True:
        
        try:
            # Check if the timeout has been exceeded
            elapsed_time = time() - start_time
            if elapsed_time > timeout:
                print(f"\nTimeout reached after {timeout} seconds.")
                break        
  
            location_pin: WebElement = driver.find_element(By.XPATH, GpsConstants.XPATH_GREEN_LOCATION_PIN)

            current_left = location_pin.value_of_css_property('left')
            current_top = location_pin.value_of_css_property('top')

            # Check if the position has changed
            if current_left != initial_left or current_top != initial_top:
                print(f"\nPosition changed! New position: left={current_left}, top={current_top}")
                # Update initial position to detect further changes
                initial_left = current_left
                initial_top = current_top
                break
            else: 

                print(f"\rWaiting for position change... {spinner[spinner_index]}", end='')
                spinner_index = (spinner_index + 1) % len(spinner)  # Update spinner index

                # Small delay to make the animation visible
                sleep(0.1)


        except UnexpectedAlertPresentException:
            break

    return initial_left, initial_top


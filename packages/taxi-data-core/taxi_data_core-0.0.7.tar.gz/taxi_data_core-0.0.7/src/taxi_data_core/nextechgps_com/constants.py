from typing import Final as Constant
from os import getenv

WEB_UI_USERNAME: Constant[str] = getenv("GPS_UI_USERNAME")
WEB_UI_PASSWORD: Constant[str] = getenv("GPS_UI_PASSWORD")
WEB_UI_URL: Constant[str] = "http://www.nextechgps.com/"

FILE_NAME_STRING: Constant[str] = "CC888-63677-"
DOWNLOADS_FOLDER: Constant[str] = "/home/wayne/Downloads/"

ID_MAIN_BOX_IFRAME: Constant[str] = 'MainBox'
ID_DEVICE_LIST: Constant[str] = 'divTabDevice147309'
ID_REPORT_DOWNLOAD_WINDOW: Constant[str] = 'ifmPage'
ID_PLAYBACK_START_DATE: Constant[str] = 'txtStartDate'
ID_PAUSE_BUTTON: Constant[str] = 'btnNext'
ID_LOGIN_IFRAME: Constant[str] = 'ifm'
ID_USERNAME_FIELD: Constant[str] = 'txtUserName'
ID_PASSWORD_FIELD: Constant[str] = 'txtUserPassword'
ID_LOGIN_BUTTON: Constant[str] = 'accountLoign'
ID_DOWNLOAD_GO_BUTTON: Constant[str] = 'btnSubmit'
ID_PLAYBACK_END_DATE: Constant[str] = 'txtEndDate'
ID_SLIDER: Constant[str] = 'PlaySpeed'
ID_PLAY_BUTTON: Constant[str] = 'btnPlay'
ID_EVENT_LIST: Constant[str] = 'tblEvent'
ID_LOADING_DATA: Constant[str] = 'spanMsg'
ID_CONTINUE_BUTTON: Constant[str] = 'btnPause'

XPATH_GPS_TRACKER: Constant[str] = '/html/body/form/div[17]/div[1]/div/div[5]/div[2]/div/div[1]'
XPATH_MORE_OPTIONS: Constant[str] = '/html/body/form/div[17]/div[1]/div/div[5]/div[2]/div/div[3]/a[3]'
XPATH_TRACKING_REPORT: Constant[str] = '/html/body/form/div[15]/div/div/div[11]/div[1]/a'
XPATH_PLAYBACK_BUTTON: Constant[str] = '/html/body/form/div[17]/div[1]/div/div[5]/div[2]/div/div[3]/a[2]'
XPATH_INFO_PANE: Constant[str] = '/html/body/form/div[3]/div[3]/div[3]/div[4]'
XPATH_GREEN_LOCATION_PIN: Constant[str] = "/html/body/form/div[3]/div[3]/div[2]"

CLASS_DOWNLOAD_DATE: Constant[str] = 'Wdate'

STR_LOADING_DATA: Constant[str] = 'Loading data!'

DATE_TIME_Y_M_D_H_M_S: Constant[str] = '%Y-%m-%d %H:%M:%S'
DATE_TIME_YEAR_FIRST: Constant[str] = "%Y-%m-%d"
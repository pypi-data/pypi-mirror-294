from pydantic import BaseModel
from typing import Final as Constant
from os import getenv

WEB_UI_USERNAME: Constant[str] = getenv("BWC_UI_USERNAME")
WEB_UI_PASSWORD: Constant[str] = getenv("BWC_UI_PASSWORD")
WEB_UI_URL: Constant[str] = "https://operators.blackandwhitecabs.com.au/"

ID_USERNAME_FIELD: Constant[str] = 'userName'
ID_PASSWORD_FIELD: Constant[str] = 'userPassword'
ID_LOGON_BUTTON: Constant[str] = 'logon-button'
ID_OPERATOR: Constant[str] = 'operator'
ID_VEHICLES_LIST: Constant[str] = 'VehiclesForOperatorList'
ID_SHIFTS_FOR_VEHICLE: Constant[str] = 'shiftsForVehicle'
ID_FROM_DATE: Constant[str] = 'fromDate'
ID_TO_DATE: Constant[str] = 'toDate'
ID_JOBS_FOR_SHIFT: Constant[str] = 'jobsForShift'
ID_DRIVER_DETAILS: Constant[str] = "mainContent"
ID_GROUP_DOCKETS_LODGED_TABLE: Constant[str] = 'GroupDocketsLodgedList'
ID_DOCKETS_LODGED_TABLE: Constant[str] = 'DocketsLodgedList'

CLASS_LAST_LOGIN_MSG_CLOSE: Constant[str] = 'dijitDialogCloseIcon'

LINK_TEXT_VEHICLES_FOR_OPERATOR: Constant[str] = 'Vehicles for Operator'
LINK_TEXT_CAR_NUMBER: Constant[str] = 'G6609'
LINK_TEXT_DRIVERS_FOR_OPERATOR: Constant[str] = 'Drivers for Operator'
LINK_TEXT_GROUP_DOCKETS_LODGED: Constant[str] = 'Group Dockets Lodged'
LINK_TEXT_DOCKETS_LODGED: Constant[str] = 'Dockets Lodged'
LINK_TEXT_ELECTRONIC_JOBS: Constant[str] = 'Electronic Jobs'
LINK_TEXT_DOCKET_STATEMENTS: Constant[str] = 'Docket Statements'
LINK_TEXT_EFTPOS_STATEMENTS: Constant[str] = 'Eftpos Statements'
LINK_TEXT_MY_ACCOUNT: Constant[str] = 'My Account'

TEXT_WAYNE_BENNETT: Constant[str] = 'Wayne Bennett'

XPATH_GO_BUTTON: Constant[str] = "//*[contains(text(), 'Go')]"
XPATH_SHIFT_ROW: Constant[str] = '//*[@id="shiftsForVehicle"]/tbody/tr'
XPATH_DRIVER_ROW: Constant[str] = '//*[@id="driversForOperatorList"]/tbody/tr'
XPATH_VEHICLE_ROW: Constant[str] = '//*[@id="VehiclesForOperatorList"]/tbody/tr'
XPATH_DRIVER_DETAILS: Constant[str] = "/html/body/div[4]/form/table"

TAG_ANCHOR: Constant[str] = 'a'

TIMEOUT: Constant[int] = 10
DEFAULT_DATE_FORMAT: Constant[str] = "%d/%m/%Y"
MONTH_FIRST_DATE_FORMAT: Constant[str] = "%m/%d/%Y"

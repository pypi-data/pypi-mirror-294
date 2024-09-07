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
ID_ELECTRONIC_JOBS: Constant[str] = 'ElectronicJobsList'
ID_DOCKET_STATEMENTS: Constant[str] = 'myForm'

CLASS_LAST_LOGIN_MSG_CLOSE: Constant[str] = 'dijitDialogCloseIcon'

LINK_TEXT_VEHICLES_FOR_OPERATOR: Constant[str] = 'Vehicles for Operator'
LINK_TEXT_CAR_NUMBER: Constant[str] = 'G6609'
LINK_TEXT_DRIVERS_FOR_OPERATOR: Constant[str] = 'Drivers for Operator'
LINK_TEXT_GROUP_DOCKETS_LODGED: Constant[str] = 'Group Dockets Lodged'
LINK_TEXT_DOCKETS_LODGED: Constant[str] = 'Dockets Lodged'
LINK_TEXT_ELECTRONIC_JOBS: Constant[str] = 'Electronic Jobs'
LINK_TEXT_DOCKET_STATEMENTS: Constant[str] = 'Docket Statements'
LINK_TEXT_EFTPOS_STATEMENTS: Constant[str] = 'Eftpos Statements'
LINK_TEXT_MY_ACCOUNT: Constant[str] = 'My Accounts'

TEXT_WAYNE_BENNETT: Constant[str] = 'Wayne Bennett'

XPATH_GO_BUTTON: Constant[str] = "//*[contains(text(), 'Go')]"
XPATH_SHIFT_ROW: Constant[str] = '//*[@id="shiftsForVehicle"]/tbody/tr'
XPATH_DRIVER_ROW: Constant[str] = '//*[@id="driversForOperatorList"]/tbody/tr'
XPATH_VEHICLE_ROW: Constant[str] = '//*[@id="VehiclesForOperatorList"]/tbody/tr'
XPATH_DRIVER_DETAILS: Constant[str] = "/html/body/div[4]/form/table"
XPATH_DOCKET_STATEMENT: Constant[str] = '/html/body/div[4]/form/table'

DRIVER_DETAILS_NUMBER: Constant[str] = 'Driver number'
DRIVER_DETAILS_NAME: Constant[str] = 'Driver name'
DRIVER_DETAILS_GREETING: Constant[str] = 'Greeting'
DRIVER_DETAILS_ADDRESS: Constant[str] = "Address"
DRIVER_DETAILS_SUBURB: Constant[str] = 'Suburb'
DRIVER_DETAILS_POST_CODE: Constant[str] = "Post Code"
DRIVER_DETAILS_DOB: Constant[str] = "Date of Birth"
DRIVER_DETAILS_MOBILE: Constant[str] = "Mobile"
DRIVER_DETAILS_CITY: Constant[str] = "City"
DRIVER_DETAILS_DA_EXPIRY: Constant[str] = "Authority Expiry"
DRIVER_DETAILS_LICENSE_EXPIRY: Constant[str] = "License Expiry"
DRIVER_DETAILS_CONDITIONS: Constant[str] = "Conditions"
DRIVER_DETAILS_CREATED: Constant[str] = "Created date"
DRIVER_DETAILS_FIRST_LOGON: Constant[str] = "First log on date"
DRIVER_DETAILS_LAST_LOGON: Constant[str] = "Last log on date"
DRIVER_DETAILS_FIRST_OPERATOR_LOGON: Constant[str] = "First log on for operator date"
DRIVER_DETAILS_LOGON_LAST_180: Constant[str] = "Logons for operator last 180 days"
DRIVER_DETAILS_HOURS_LAST_180: Constant[str] = "Hours for operator last 180 days"
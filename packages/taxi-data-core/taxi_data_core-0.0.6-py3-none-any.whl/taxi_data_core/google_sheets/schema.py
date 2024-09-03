from typing import Final as Constant
from enum import Enum
from pydantic import BaseModel
from datetime import time
from pydantic import BaseModel
from typing import Final as Constant
from datetime import time, date
from enum import Enum



class DocketType(str, Enum):
    APP_BOOKING: Constant[str]  = "App booking"
    ACCOUNT: Constant[str] = "BWC Account"
    DVA: Constant[str] = "DVA"
    NDIS: Constant[str] = "NDIS"
    PRE_PAID: Constant[str] = "Pre Paid"
    GROUPS: Constant[str] = "Groups"
    INTERNAL: Constant[str] = "Internal"

class DocketStatus(str, Enum):
    COMPLETED: Constant[str] = "Completed"
    LODGED: Constant[str] = "Lodged"
    LOGGED: Constant[str] = "Logged"
    PAID: Constant[str] = "Paid"
    DISPUTED: Constant[str] = "Disputed"
    FINALISED: Constant[str] = "Finalised"

class Docket(BaseModel):
    docket_date: date
    docket_type: DocketType
    job_number: int
    account_number: str
    order_number: str
    group_number: str 
    start_time: time
    finish_time: time
    passenger_name: str
    pickup_area: str
    destination_area: str
    meter_total: float
    eft_surcharge: float
    extras: float
    paid_by_passenger_tss: float
    amount_owing: float
    car_number: int
    status: DocketStatus
    lodgment_date: date
    statement_date: date

class VoucherType(str, Enum):
    PRE_PAID: Constant[str] = "pre-paid"
    INTERSTATE_TSS: Constant[str] = "Interstate TSS"
    MANUAL_EFT: Constant[str] = "manual EFT"
    MANUAL_TSS: Constant[str] = "manual TSS"

class Voucher(BaseModel):
    voucher_date: date
    car: int
    amount: float
    voucher_number: int
    voucher_type: VoucherType
    status: DocketStatus
    lodgment_date: date | str
    statement_date: date

class CabCharge(BaseModel):
    docket_date: date
    car: int
    amount: float
    reference: int
    status: DocketStatus
    statement: date
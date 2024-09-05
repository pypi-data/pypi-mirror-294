from typing import Final as Constant
from enum import Enum
from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import Optional
from taxi_data_core.common.schema import StatementType


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

class VoucherType(str, Enum):
    PRE_PAID: Constant[str] = "pre-paid"
    INTERSTATE_TSS: Constant[str] = "Interstate TSS"
    MANUAL_EFT: Constant[str] = "manual EFT"
    MANUAL_TSS: Constant[str] = "manual TSS"

class Docket(BaseModel):
    docket_date: date
    docket_type: DocketType
    job_number: int
    account_number: str
    order_number: str
    group_number: str 
    start_time: Optional[datetime]
    finish_time: Optional[datetime]
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
    lodgment_date: Optional[datetime] | Optional[str] = None
    statement: Optional[str] = None
    driver: str
    driver_id: int
    driver_abn: int

class Voucher(BaseModel):
    voucher_date: date
    car: int
    amount: float
    voucher_number: int
    voucher_type: VoucherType
    status: DocketStatus
    lodgment_date: Optional[datetime] | Optional[str] = None
    statement: Optional[str] = None

class CabCharge(BaseModel):
    docket_date: date
    car: int
    amount: float
    reference: int
    status: DocketStatus
    statement: Optional[int] = None

class EftStatement(BaseModel):
    statement: int
    statement_date: date
    statement_amount: float
    amount_allocated: float

class DocketStatement(BaseModel):
    statement_date: date
    statement_type: StatementType
    statement_amount: float
    allocated_amount: float
    reference: str
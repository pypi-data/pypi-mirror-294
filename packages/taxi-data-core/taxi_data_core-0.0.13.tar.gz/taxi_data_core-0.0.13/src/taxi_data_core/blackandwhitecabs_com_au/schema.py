from typing import Final as Constant
from enum import Enum
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from typing import Final as Constant
from datetime import time, datetime, date
from enum import Enum

class StatementType(str, Enum):
    VOUCHER: Constant[str] = "VOU"
    GROUP: Constant[str] = "GRP"
    DVA: Constant[str] = "DV2"
    ACCOUNT: Constant[str] = "AC"
    NDIS: Constant[str] = "NDI"

class PaperDocketStatus(str, Enum):
    PENDING: Constant[str] = "Pending"
    POSTED: Constant[str] = "Posted"

class Taxi(BaseModel):
    number: str
    primary_fleet: str
    rego: str
    rego_expiry: date
    coi_expiry: date
    fleets: str
    conditions: str
    make: str
    model: str
    build_date: str
    pax: int
    validation: Optional[str] = None
    until: Optional[date] = None
    reason: Optional[str] = None

class Driver(BaseModel):
    number: int
    name: str
    greeting: str
    address: str
    suburb: str
    post_code: int
    dob: date
    mobile: str
    city: str
    da_expiry: date
    license_expiry: date
    auth_wheelchair: Optional[bool] = None
    auth_bc: Optional[bool] = None
    auth_redcliffe: Optional[bool] = None
    auth_london: Optional[bool] = None
    auth_mandurah: Optional[bool] = None
    refer_fleet_ops: Optional[bool] = None
    conditions: str
    create_date: date
    first_logon: date
    last_logon: date
    first_operator_logon: date
    logons_for_operator: int
    hours_for_operator: int
    validation_active: Optional[bool] = None
    validation_until: Optional[date] = None
    validation_reason: Optional[str] = None
    
class Shift(BaseModel):
    car_id: Taxi | int
    driver_id: Driver | int
    name: str
    log_on: datetime
    log_off: datetime
    duration: int
    distance: int
    offered: int
    accepted: int
    rejected: int
    recalled: int
    completed: int
    total_fares: float
    total_tolls: float

class Job(BaseModel):
    booking_id: int	
    driver_id: Driver | int
    status: str
    accepted: time
    meter_on: time
    meter_off: time
    pick_up_suburb: str
    destination_suburb: str
    fare: float
    toll: float
    account: Optional[str]
    taxi_id: Taxi | int
    shift_id: Shift | int

class EftStatement(BaseModel):
    statement_ref: 	int
    statement_url: str
    statement_date: date	
    statement_amount: float	

class VoucherStatement(BaseModel):
    statement_date: date
    statement_url: HttpUrl
    vehicle: int
    reference: int
    cross_reference: str
    count: int
    statement_amount: float	
    batch: int
    status: PaperDocketStatus

class GroupStatement(BaseModel):
    statement_date: date
    statement_url: HttpUrl
    vehicle: int
    reference: int
    amount: float
    batch: int
    status: PaperDocketStatus

class AutoJob(BaseModel):
    date: date
    count: int
    amount: float

class DocketStatement(BaseModel):
    statement_date: date
    statement_url: HttpUrl
    type: StatementType
    amount: float
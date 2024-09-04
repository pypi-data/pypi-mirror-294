from typing import Final as Constant
from typing import NamedTuple
from enum import Enum
from pydantic import BaseModel
from datetime import time
from selenium.webdriver.remote.webelement import WebElement
from pydantic import BaseModel, HttpUrl
from typing import Optional, NamedTuple, List
from typing import Final as Constant
from datetime import time, date
from enum import Enum
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path

class GpsTrackerEvent(str,Enum):
    STAY: Constant[str] = "Stay"

class ProcessedEvent(BaseModel):
    event_type: GpsTrackerEvent
    from_time: time
    to_time: time
    duration: int

class RawEvent(BaseModel):
    event_type: str
    from_time: str
    to_time: str
    duration: str

class PlaybackSpeed(str,Enum):
    FAST: Constant[str] = "FAST"
    SLOW: Constant[str] = "SLOW"

class PlaybackButtons(NamedTuple):
    Play: WebElement
    Pause: WebElement
    Continue: WebElement

class TrackerEntry(BaseModel):
    timestamp: time
    distance: float
    latitude: float
    longitude: float
    direction: Optional[str] = None
    speed: Optional[float] = None
    stop_time: Optional[int] = None

class GpsRecord(BaseModel):
    date: date
    kml_file: Optional[Path] = None
    events: Optional[List[ProcessedEvent]] = None
    gps_data: Optional[List[TrackerEntry]] = None


from enum import Enum
from typing import Final as Constant


class StatementType(str, Enum):
    ACCOUNT: Constant[str] = "AC"
    VOUCHER: Constant[str] = "VOU"
    GROUP: Constant[str] = "GRP"
    DVA: Constant[str] = "DV2"
    NDIS: Constant[str] = "NDI"
    DOCKET: Constant[str] = "DKT"
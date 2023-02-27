from enum import Enum
from typing import Optional, List
from datetime import date
from pydantic import BaseModel

class IncomeType(str):
    BANK_BCA='BANK BCA'
    BANK_ALADIN='BANK ALADIN'
    GIFT='GIFT'
    CASH='CASH'
    GOPAY='GOPAY'
    OVO='OVO'
    SHOPEE_PAY='SHOPEE PAY'
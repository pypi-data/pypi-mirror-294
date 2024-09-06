from typing import Dict

from pydantic import BaseModel


class PaymentMethodAmounts(BaseModel):
    RUB: float
    UAH: float
    USD: float
    EUR: float


class PaymentMethod(BaseModel):
    name: str
    min: PaymentMethodAmounts
    max: PaymentMethodAmounts
    commission_percent: float
    commission_user_percent: float
    commission_merchant_percent: float
    commission_type: str


class PaymentMethods(BaseModel):
    list: Dict[str, PaymentMethod]

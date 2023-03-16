import decimal

from pydantic import BaseModel


class _AddTradeBase(BaseModel):
    side_indicator: str
    shares: str
    stock_symbol: str
    price: decimal.Decimal

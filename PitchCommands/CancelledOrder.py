from BaseClasses.OrderBase import _OrderBase
from pydantic import BaseModel


class CancelledOrder(_OrderBase):
    cancelled_shares: str

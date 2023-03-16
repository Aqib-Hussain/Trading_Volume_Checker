from typing import Any

from BaseClasses.AddOrderTradeMessageBase import _AddTradeBase
from BaseClasses.ExecutedOrderTradeMessageBase import _ExecutedTradeBase
from BaseClasses.OrderBase import _OrderBase


class TradeMessage(_OrderBase, _AddTradeBase, _ExecutedTradeBase):

    def __init__(self, **data: Any):
        super().__init__(**data)

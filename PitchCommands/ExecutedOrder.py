from BaseClasses.OrderBase import _OrderBase
from BaseClasses.ExecutedOrderTradeMessageBase import _ExecutedTradeBase


class ExecutedOrder(_OrderBase, _ExecutedTradeBase):
    executed_shares: str

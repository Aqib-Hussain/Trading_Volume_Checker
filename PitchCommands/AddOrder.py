from BaseClasses.AddOrderTradeMessageBase import _AddTradeBase
from BaseClasses.OrderBase import _OrderBase


class AddOrder(_OrderBase, _AddTradeBase):
    display: str

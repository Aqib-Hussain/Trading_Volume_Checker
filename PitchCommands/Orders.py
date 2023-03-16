import typing

from pydantic import BaseModel
from typing import List, Optional, Dict
from collections import Counter

from PitchCommands.AddOrder import AddOrder
from PitchCommands.TradeMessage import TradeMessage
from PitchCommands.ExecutedOrder import ExecutedOrder
from PitchCommands.CancelledOrder import CancelledOrder


class Orders(BaseModel):
    add_orders: List[AddOrder] = []
    cancelled_orders: List[CancelledOrder] = []
    trade_messages: List[TradeMessage] = []
    executed_orders: List[ExecutedOrder] = []

    def get_top_ten_by_executed_volume(self):
        all_shares_with_quantity = self.calculate_volume_of_all_shares()
        top_ten = dict(Counter(all_shares_with_quantity).most_common(10))

        final_result = ""
        for share, quantity in top_ten.items():
            final_result += share + "   " + str(quantity) + "\n"
        return final_result

    def calculate_volume_of_all_shares(self):
        all_shares_with_quantity: Dict[str, int] = dict()

        if len(self.executed_orders) > 0:
            for order in self.executed_orders:
                order_to_be_modified = self.cross_reference_order_id(order.order_id)
                stock_change = order.executed_shares
                index_to_change = self.get_index_of_add_order_with_order(order_to_be_modified)
                order_to_be_modified.shares = stock_change
                self.add_orders[index_to_change] = order_to_be_modified

        if len(self.add_orders) > 0:
            for order in self.add_orders:
                stock_symbol = order.stock_symbol
                stock_amount = order.shares

                if stock_symbol in all_shares_with_quantity:
                    all_shares_with_quantity.update(
                        {stock_symbol: all_shares_with_quantity.get(stock_symbol) + int(stock_amount)})
                else:
                    all_shares_with_quantity[stock_symbol] = int(stock_amount)

        if len(self.cancelled_orders) > 0:
            for order in self.cancelled_orders:
                try:
                    stock_symbol = self.cross_reference_order_id(order.order_id).stock_symbol
                    stock_amount = order.cancelled_shares

                    if stock_symbol in all_shares_with_quantity:
                        all_shares_with_quantity.update(
                            {stock_symbol: all_shares_with_quantity.get(stock_symbol) - int(stock_amount)})
                except AttributeError:
                    raise Exception("Cannot cancel order that didn't exist in the first place")

        if len(self.trade_messages) > 0:
            for order in self.trade_messages:
                stock_symbol = order.stock_symbol
                stock_amount = order.shares

                if stock_symbol in all_shares_with_quantity:
                    all_shares_with_quantity.update(
                        {stock_symbol: all_shares_with_quantity.get(stock_symbol) + int(stock_amount)})
                else:
                    all_shares_with_quantity[stock_symbol] = int(stock_amount)

        return all_shares_with_quantity

    def cross_reference_order_id(self, order_id):
        for order in self.add_orders:
            if order.order_id == order_id:
                return order

    def get_index_of_add_order_with_order(self, order_reference):
        for index, order in enumerate(self.add_orders):
            if order.order_id == order_reference.order_id:
                return index

from PitchCommands.Orders import Orders
from PitchCommands.AddOrder import AddOrder
from PitchCommands.ExecutedOrder import ExecutedOrder
from PitchCommands.CancelledOrder import CancelledOrder
from PitchCommands.TradeMessage import TradeMessage

import unittest


class TestOrders(unittest.TestCase):

    def test_cross_reference_order_id(self):
        orders_test_data = Orders(add_orders=[
            AddOrder(timestamp=28963624, message_type="A", order_id="BK27GA0001CL", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001CM", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y"),
            AddOrder(timestamp=28963626, message_type="A", order_id="BK27GA0001CN", side_indicator="S",
                     shares="000001", stock_symbol="ADP", price="0000611100", display="Y")])

        actual = orders_test_data.cross_reference_order_id("BK27GA0001CL")
        self.assertEqual(AddOrder(timestamp=28963624, message_type="A", order_id="BK27GA0001CL", side_indicator="S",
                                  shares="001000", stock_symbol="TGT", price="0000611100", display="Y"), actual)

    def test_calculate_volume_add_orders_only(self):
        orders_test_data = Orders(add_orders=[
            AddOrder(timestamp=28963624, message_type="A", order_id="BK27GA0001CL", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001CM", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y"),
            AddOrder(timestamp=28963626, message_type="A", order_id="BK27GA0001CN", side_indicator="S",
                     shares="000001", stock_symbol="ADP", price="0000611100", display="Y")])

        actual = orders_test_data.calculate_volume_of_all_shares()
        self.assertEqual(actual, {'ADP': 1, 'TGT': 2000})

    def test_calculate_volume_with_executed_order(self):
        orders_test_data = Orders(add_orders=[
            AddOrder(timestamp=28963624, message_type="A", order_id="BK27GA0001CL", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y")],
            executed_orders=[
                ExecutedOrder(timestamp=28963626, message_type="E", order_id="BK27GA0001CL", executed_shares="500",
                              execution_id="AAAAAAAAAAAA")])

        actual = orders_test_data.calculate_volume_of_all_shares()
        self.assertEqual(actual, {'TGT': 500})

    def test_calculate_volume_with_cancelled_order_part(self):
        orders_test_data = Orders(add_orders=[
            AddOrder(timestamp=28963624, message_type="A", order_id="BK27GA0001CL", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y")],
            cancelled_orders=[CancelledOrder(timestamp=28963626, message_type="X", order_id="BK27GA0001CL",
                                             cancelled_shares="000500")])

        actual = orders_test_data.calculate_volume_of_all_shares()
        self.assertEqual(actual, {'TGT': 500})

    def test_calculate_volume_with_cancelled_order_whole(self):
        orders_test_data = Orders(add_orders=[
            AddOrder(timestamp=28963624, message_type="A", order_id="BK27GA0001CL", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y")],
            cancelled_orders=[CancelledOrder(timestamp=28963626, message_type="X", order_id="BK27GA0001CL",
                                             cancelled_shares="0001000")])

        actual = orders_test_data.calculate_volume_of_all_shares()
        self.assertEqual(actual, {'TGT': 0})

    def test_calculate_volume_with_trade_message(self):
        orders_test_data = Orders(trade_messages=[
            TradeMessage(timestamp=28963624, message_type="P", order_id="BK27GA0001CL", side_indicator="B",
                         shares="001000", stock_symbol="TGT", price="0000611100", execution_id="AAAAAAAAAAAA")])

        actual = orders_test_data.calculate_volume_of_all_shares()
        self.assertEqual({'TGT': 1000}, actual)

    def test_cancel_order_without_add_order_counterpart(self):
        orders_test_data = Orders(
            cancelled_orders=[CancelledOrder(timestamp=28963626, message_type="X", order_id="BK27GA0001CL",
                                             cancelled_shares="000500")])
        with self.assertRaises(Exception) as error:
            actual = orders_test_data.calculate_volume_of_all_shares()

        self.assertEqual(str(error.exception), "Cannot cancel order that didn't exist in the first place")

    def test_get_index_of_add_order_with_order(self):
        orders_test_data = Orders(add_orders=[
            AddOrder(timestamp=28963624, message_type="A", order_id="BK27GA0001CL", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001CM", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y"),
            AddOrder(timestamp=28963626, message_type="A", order_id="BK27GA0001CN", side_indicator="S",
                     shares="000001", stock_symbol="ADP", price="0000611100", display="Y")])

        actual = orders_test_data.get_index_of_add_order_with_order(
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001CM", side_indicator="S",
                     shares="001000", stock_symbol="TGT", price="0000611100", display="Y"))

        self.assertEqual(actual, 1)

    def test_get_top_ten_by_executed_volume(self):
        orders_test_data = Orders(add_orders=[
            AddOrder(timestamp=28963624, message_type="A", order_id="BK27GA0001CA", side_indicator="S",
                     shares="001000", stock_symbol="AAAAA", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001CB", side_indicator="S",
                     shares="000500", stock_symbol="BBBBB", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001C", side_indicator="S",
                     shares="000250", stock_symbol="CCCCC", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001D", side_indicator="S",
                     shares="000100", stock_symbol="DDDDD", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001E", side_indicator="S",
                     shares="000099", stock_symbol="EEEEE", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001F", side_indicator="S",
                     shares="000088", stock_symbol="FFFFF", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001G", side_indicator="S",
                     shares="000077", stock_symbol="GGGGG", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001H", side_indicator="S",
                     shares="000066", stock_symbol="HHHHH", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001I", side_indicator="S",
                     shares="000055", stock_symbol="IIIII", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001J", side_indicator="S",
                     shares="000044", stock_symbol="JJJJJ", price="0000611100", display="Y"),
            AddOrder(timestamp=28963625, message_type="A", order_id="BK27GA0001K", side_indicator="S",
                     shares="000033", stock_symbol="KKKKK", price="0000611100", display="Y")],
            trade_messages=[
                TradeMessage(timestamp=28963624, message_type="P", order_id="BK27GA0001K", side_indicator="B",
                             shares="001001", stock_symbol="LLLLL", price="0000611100", execution_id="AAAAAAAAAAAA")],
            cancelled_orders=[CancelledOrder(timestamp=28963626, message_type="X", order_id="BK27GA0001K",
                                             cancelled_shares="000033")],
            executed_orders=[
                ExecutedOrder(timestamp=28963626, message_type="E", order_id="BK27GA0001J", executed_shares="000056",
                              execution_id="AAAAAAAAAAAA")])

        actual = orders_test_data.get_top_ten_by_executed_volume()
        expected = "LLLLL   1001\n" \
                   "AAAAA   1000\n" \
                   "BBBBB   500\n" \
                   "CCCCC   250\n" \
                   "DDDDD   100\n" \
                   "EEEEE   99\n" \
                   "FFFFF   88\n" \
                   "GGGGG   77\n" \
                   "HHHHH   66\n" \
                   "JJJJJ   56\n"

        self.assertEqual(actual, expected)

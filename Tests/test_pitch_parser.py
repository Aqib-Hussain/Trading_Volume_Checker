import unittest
import PitchParser

from PitchCommands.Orders import Orders
from PitchCommands.AddOrder import AddOrder
from PitchCommands.CancelledOrder import CancelledOrder
from PitchCommands.ExecutedOrder import ExecutedOrder
from PitchCommands.TradeMessage import TradeMessage

from decimal import Decimal


class TestPitchParser(unittest.TestCase):

    def test_check_if_txt_file(self):
        with self.assertRaises(ValueError) as error:
            actual = PitchParser.check_if_txt_file("not_txt.csv")

        self.assertEqual(str(error.exception), "File extension should be .txt")

    def test_remove_first_s_character(self):
        actual = PitchParser.remove_first_s_character("S28800297X1K27GA00000Y000100")
        self.assertEqual(actual, "28800297X1K27GA00000Y000100")

    def test_convert_pitch_commands_to_lists(self):
        actual = PitchParser.convert_pitch_commands_to_lists(
            ["28800312ABK27GA00000XB000100URE   0000379200Y", "28800318E1K27GA00000X00010000001AQ00001",
             "28800319X1K27GA00000Y000100", "28803240P4K27GA00003PB000100DXD   0000499600000N4AQ00003"])

        expected = Orders(add_orders=[
            AddOrder(timestamp=28800312, message_type="A", order_id="BK27GA00000X", side_indicator="B", shares="000100",
                     stock_symbol="URE", price="0000379200", display="Y")],
            executed_orders=[ExecutedOrder(timestamp=28800318, message_type='E', order_id='1K27GA00000X',
                                           executed_shares='000100', execution_id='00001AQ00001')],
            cancelled_orders=[CancelledOrder(timestamp=28800319, message_type='X', order_id='1K27GA00000Y',
                                             cancelled_shares='000100')],
            trade_messages=[
                TradeMessage(timestamp=28803240, message_type='P', order_id='4K27GA00003P', side_indicator='B',
                             shares='000100', stock_symbol='DXD', price=Decimal('499600'),
                             execution_id='000N4AQ00003')])

        self.assertEqual(actual, expected)

    def test_convert_pitch_commands_to_lists_error(self):
        with self.assertRaises(Exception) as error:
            actual = PitchParser.convert_pitch_commands_to_lists(
                ["28800312ABK27GA00000XB000100URE   0000379200Y", "28800318E1K27GA00000X00010000001AQ00001",
                 "28800", "28803240P4K27GA00003PB000100DXD   0000499600000N4AQ00003"])

        self.assertEqual(str(error.exception), "There was an error parsing the data")

    def test_parse_pitch_data_error(self):
        with self.assertRaises(Exception) as error:
            actual = PitchParser.parse_pitch_data("doesnotexist.txt")

        self.assertEqual(str(error.exception), "File does not exist, the file should be at the root of the Resources folder")
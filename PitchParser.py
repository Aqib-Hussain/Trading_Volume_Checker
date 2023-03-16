from decimal import Decimal
from typing import List

from PitchCommands.Orders import Orders
from PitchCommands.AddOrder import AddOrder
from PitchCommands.ExecutedOrder import ExecutedOrder
from PitchCommands.TradeMessage import TradeMessage
from PitchCommands.CancelledOrder import CancelledOrder


def parse_pitch_data(file_name: str):
    list_of_all_commands = []
    try:
        with open("Resources/" + file_name) as pitch_data:
            check_if_txt_file(file_name)
            for line in pitch_data:
                line = remove_first_s_character(line.rstrip())
                list_of_all_commands.append(line)
        return convert_pitch_commands_to_lists(list_of_all_commands)
    except FileNotFoundError:
        raise FileNotFoundError("File does not exist, the file should be at the root of the Resources folder")


def check_if_txt_file(file_name: str):
    if not file_name[-3:] == "txt":
        raise ValueError("File extension should be .txt")


def remove_first_s_character(line: str):
    if line[0].lower() == "s":
        return line[1::]


def convert_pitch_commands_to_lists(list_of_all_commands: [str]):
    add_orders: List[AddOrder] = []
    executed_orders: List[ExecutedOrder] = []
    trade_messages: List[TradeMessage] = []
    cancelled_orders: List[CancelledOrder] = []
    try:
        for pitch_command in list_of_all_commands:
            timestamp = pitch_command[0:8]
            message_type = pitch_command[8:9]
            order_id = pitch_command[9:21]

            if pitch_command[8].lower() == "a":
                side_indicator = pitch_command[21:22]
                shares = pitch_command[22:28]
                stock_symbol = pitch_command[28: pitch_command.index(" ")]
                price = pitch_command[pitch_command.rfind(" "): len(pitch_command) - 1]
                display = pitch_command[-1]

                add_order = AddOrder(timestamp=timestamp, message_type=message_type, order_id=order_id,
                                     side_indicator=side_indicator, shares=shares, stock_symbol=stock_symbol, price=price,
                                     display=display)
                add_orders.append(add_order)

            elif pitch_command[8].lower() == "p":
                side_indicator = pitch_command[21:22]
                shares = pitch_command[22:28]
                stock_symbol = pitch_command[28: pitch_command.index(" ")]
                price = pitch_command[pitch_command.rfind(" "): pitch_command.rfind(" ") + 11]
                execution_id = pitch_command[pitch_command.rfind(" ") + 11:]

                trade_message = TradeMessage(timestamp=timestamp, message_type=message_type, order_id=order_id,
                                             side_indicator=side_indicator, shares=shares,
                                             stock_symbol=stock_symbol, price=Decimal(price),
                                             execution_id=execution_id)
                trade_messages.append(trade_message)

            elif pitch_command[8].lower() == "x":
                cancelled_shares = pitch_command[21:]

                cancelled_order = CancelledOrder(timestamp=timestamp, message_type=message_type, order_id=order_id,
                                                 cancelled_shares=cancelled_shares)
                cancelled_orders.append(cancelled_order)

            elif pitch_command[8].lower() == "e":
                executed_shares = pitch_command[21:27]
                execution_id = pitch_command[27:]

                executed_order = ExecutedOrder(timestamp=timestamp, message_type=message_type, order_id=order_id,
                                               executed_shares=executed_shares, execution_id=execution_id)
                executed_orders.append(executed_order)

        return Orders(add_orders=add_orders, trade_messages=trade_messages, cancelled_orders=cancelled_orders,
                      executed_orders=executed_orders)
    except Exception:
        raise Exception("There was an error parsing the data")

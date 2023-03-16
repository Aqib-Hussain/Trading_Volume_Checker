from decimal import Decimal

from PitchCommands.AddOrder import AddOrder

from PitchParser import parse_pitch_data

if __name__ == '__main__':
    all_orders = parse_pitch_data("pitch_example_data.txt")

    try:
        print(all_orders.get_top_ten_by_executed_volume())
    except Exception as error:
        print(error)

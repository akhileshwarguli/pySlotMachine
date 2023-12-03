import random

MAX_LINES: int = 3
MIN_BET: int = 1
MAX_BET: int = 10

ROWS = 3
COLUMNS = 3

SYMBOLS_PROBABILITY = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}

SYMBOLS_VALUE = {
    'A': 8,
    'B': 6,
    'C': 4,
    'D': 2
}


def get_slot_machine_spin(rows, cols, symbols):
    all_possible_symbols = []
    for symbol, probability in SYMBOLS_PROBABILITY.items():
        for s in range(probability):
            all_possible_symbols.append(symbol)
    # print(all_possible_symbols)

    columns = []
    for col in range(cols):
        column = []
        possible_symbols = all_possible_symbols[:]
        for row in range(rows):
            value = random.choice(possible_symbols)
            possible_symbols.remove(value)  # Removing the value from possible symbols
            column.append(value)
        columns.append(column)
    # print(columns)
    return columns


def print_slot_columns(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], " | ", end="")
            else:
                print(column[row])


def calculate_win_lose(current_balance, columns, lines, bet, values) -> int:
    slot_row = []
    for row in range(len(columns[0])):
        if columns[0][row] == columns[1][row] == columns[2][row]:
            slot_row.append(columns[0][row])
            slot_row.append(columns[1][row])
            slot_row.append(columns[2][row])
    # print(slot_row)
    if len(slot_row) != 0:
        print('Bingo!!')
        win_amount: int = 1
        for line in range(lines):
            win_amount += values.get(slot_row[line]) * bet
        win_amount -= 1  # Adjusting winning amount
        print(f'Won : ${win_amount}')
        print(f'Total balance : ${current_balance + win_amount}')
        current_balance += win_amount
    else:
        lost_amount = bet * lines
        print(f'Sorry you lost ${lost_amount} bet. ')
        print(f'Current balance : ${current_balance}')
        # print(f'Total balance : ${current_balance - lost_amount}')
        # current_balance -= lost_amount
    return current_balance


def get_deposit_amount() -> int:
    while True:
        amount = input(f'Enter the amount you want to deposit : $ ')
        if amount.isdigit():
            amount = int(amount)
            if amount <= 0:
                print(f'Deposit amount should be greate than ZERO. ')
            else:
                break
        else:
            print('Deposit amount should be digits.')
    return amount


def get_lines_to_bet():
    while True:
        lines = input(f'Enter the no. of lines you want to bet : # ')
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(f'No. of lines should be between 1 and {MAX_LINES}.')
        else:
            print('No. of lines should be digits.')
    return lines


def get_bet_amount():
    while True:
        amount = input(f'Enter the amount you want to bet, per line : $ ')
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f'Bet amount should be between {MIN_BET} - {MAX_BET}. ')
        else:
            print('Bet amount should be digits.')
    return amount


def roll_the_machine(current_balance) -> int:
    while True:
        lines = get_lines_to_bet()
        bet = get_bet_amount()
        total_bet = lines * bet
        if total_bet <= current_balance:
            break
        else:
            print(f'You dont have enough $ to place this bet of ${total_bet}, current balance : ${current_balance}')
            return current_balance
    current_balance -= total_bet  # Updating current balance
    print(f'{lines} x ${bet} => betting ${total_bet}. Remaining balance ${current_balance}')
    print('--\(^ ^)/-- --\(^ ^)/-- Rolling the slot machine --\(^ ^)/-- --\(^ ^)/-- ')
    columns = get_slot_machine_spin(ROWS, COLUMNS, SYMBOLS_PROBABILITY)
    print_slot_columns(columns)
    return calculate_win_lose(current_balance, columns, lines, bet, SYMBOLS_VALUE)


def print_closing_amount(start_balance, closing_balance):
    print(f'Thank you for playing !! Visit again')
    if start_balance < closing_balance:
        print(f'===> You earned ${closing_balance - start_balance}')
    else:
        print(f'===> You lost ${start_balance - closing_balance}')
    print(f'Your Closing balance : ${closing_balance}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        balance = get_deposit_amount()
        starting_balance = balance
        while True:
            balance = roll_the_machine(balance)
            reply = input(f'Want to play another round? Y/N : ')
            if reply.lower() == 'n' or reply.lower() == 'no':
                print_closing_amount(starting_balance, balance)
                break
            else:
                if balance < (MIN_BET * 1):
                    print(f'Your balance : ${balance} is not enough to place even minimum bet.')
                    print('Please deposit more if you want to continue.')
                    play = input(f'Do you wish to continue? Y/N : ')
                    if play.lower() == 'n' or play.lower() == 'no':
                        print_closing_amount(starting_balance, balance)
                        break
                    else:
                        print('============ Trying again ============')
                        balance = get_deposit_amount()
                        starting_balance += balance
                else:
                    print('============ NEXT ROUND ============')
    except KeyboardInterrupt:
        print()
        print(f'Program ended abruptly...')

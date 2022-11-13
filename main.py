import os  # for colors
import random  # for 1 vs PC mode

os.system("")  # enable colors

dic_main_options = {
    'player1': 'Игрок 1',
    'player2': 'Игрок 2',
    'p1_score': 0,
    'p2_score': 0,
    'is_p1_turn': False,
    'is_game': 1,  # collect number of games played
    'is_turn': 0,
    'is_ai': False,  # game mode 1 vs PC or 1 vs 1
    'is_p1_start_game': True,
}
dic_menu_help = {
    'main_menu': '''
    --- Выберите режим игры ---
    - [ 1 ] Против компьютера
    - [ 2 ] 2 игрока
    - [ E ] Выход 
    ---------------------------: ''',
    'player_name': '''
    --- Задать имена игрокам ---
    - [ Y ] Да
    - [ N ] Без имени
    - [ B ] Назад
    ---------------------------: ''',
    'difficult': '''
    --- Выберите сложность ---
    - [ H ] Сложный (5% на ошибку)
    - [ N ] Нормальный (30% на ошибку)
    - [ E ] Легкий (75% на ошибку)
    ---------------------------: ''',
    'in_game': '''
    --- Введите номер клетки [1-9] или пункт меню ---
    - [ N ] Новая партия (ничья)
    - [ R ] Новая игра и новый счет
    - [ M ] В главное меню
    ---------------------------: ''',
    'is_over': '''
    --- Игра окончена (нажмите Enter или введите команду) ---
    - [ N ] Новая игра
    - [ M ] В главное меню
    ---------------------------: ''',
    'player1': '-- Введите имя игрока 1: ',
    'player2': '-- Введите имя игрока 2: ',
}
dic_ai = {
    'chance_to_lose': 0,  # chance that pc will miss potentially winning combination of player (max 100)
    'tactic': '',  # angle or side
    'step': 1,
    'move': [],  # collect pc moves
    'cell_square': [1, 3, 7, 9],
    'cell_line': [2, 4, 5, 6, 8],
}
dic_player_combination = {  # potentially winner combination (need for 1 vs pc)
    1: [[2, 3], [5, 9], [7, 4]],
    2: [[1, 3], [5, 8]],
    3: [[1, 2], [5, 7], [6, 9]],
    4: [[1, 7], [5, 6]],
    5: [[2, 8], [4, 6]],
    6: [[4, 5], [3, 9]],
    7: [[1, 4], [8, 9], [3, 5]],
    8: [[2, 5], [7, 9]],
    9: [[3, 6], [7, 8], [1, 5]]
}
dic_color = {
    'reset': '\033[0m',
    'green': '\033[92m',
    'yellow': '\033[33m',
    'red': '\033[31m',
    'purple': '\033[35m',
    'white': '\033[37m',
}
dic_game_field = {}
nl = '\n'  # New line


# -- SYSTEM WITH MODULE --
def clear_window():
    os.system('cls')  # Delete everything from window


def colored(text, color):  # make color for text
    return f'{dic_color[color]}{text}{dic_color["reset"]}'


def c_field(num):  # make color for field characters
    if dic_game_field[num] == 'X':
        return colored(dic_game_field[num], 'yellow')
    elif dic_game_field[num] == 'O':
        return colored(dic_game_field[num], 'purple')
    else:
        return colored(dic_game_field[num], 'white')
# --------------------------


# ------ MAIN OPTIONS ------
def set_player_name():
    player1 = (input(dic_menu_help['player1']))
    player2 = (input(dic_menu_help['player2']))
    dic_main_options['player1'] = player1[:15].capitalize()
    dic_main_options['player2'] = player2[:15].capitalize()
    new_game(True)


def new_game(reset_score=False):
    dic_main_options['is_turn'] = 0
    dic_ai['step'] = 1
    dic_ai['move'] = []
    for i in range(1, 10):  # Generate new game field
        dic_game_field[i] = i

    if dic_main_options['is_game'] % 2 == 0:  # One game will start with 1 player, second game - 2 player
        dic_main_options['is_p1_turn'] = True  # it will be flip on the first turn
        dic_main_options['is_p1_start_game'] = False
    else:
        dic_main_options['is_p1_turn'] = False  # it will be flip on the first turn
        dic_main_options['is_p1_start_game'] = True

    if reset_score:  # Reset game and score from in game_menu
        dic_main_options['p1_score'] = dic_main_options['p2_score'] = 0

    make_head_of_field()
# ----------------------------


# ------- INPUT --------------
def make_center_input(name):
    result = input(dic_menu_help[name]).upper()
    # Main Menu
    if name == 'main_menu':
        if result:  # check that result is not empty
            if result == '1':  # 1 vs PC
                dic_main_options['is_ai'] = True
                dic_main_options['player1'] = 'Человек'
                dic_main_options['player2'] = 'Компьютер'
                print_title(state=3)  # menu with difficult
            elif result == '2':  # 1 vs 1
                dic_main_options['is_ai'] = False
                print_title(state=1)  # menu with change names
            elif result == 'E':
                quit()  # Exit from game
            else:
                print_title()
        else:
            print_title()

    # Do you want to choose name for players?
    if name == 'player_name':
        if result:
            if result == 'Y':  # With Name
                print_title(state=2)
            elif result == 'N':  # Without Names
                dic_main_options['player1'] = 'Игрок 1'
                dic_main_options['player2'] = 'Игрок 2'
                new_game(True)
            elif result == 'B':  # Without Names
                print_title()
            else:
                print_title()  # Err command -> Go to Main menu
        else:
            print_title()  # No keyword -> Go to Main menu

    # Do you want to choose name for players?
    if name == 'difficult':
        if result:
            if result == 'H':  # Hard mode
                dic_ai['chance_to_lose'] = 5
            elif result == 'N':  # Normal mode
                dic_ai['chance_to_lose'] = 30
            elif result == 'E':  # Easy mode
                dic_ai['chance_to_lose'] = 75
            new_game(True)
        else:
            print_title()  # No keyword -> Go to Main menu

    # In game menu
    if name == 'in_game':
        if result:
            if result == 'N':  # New game
                dic_main_options['is_game'] += 1
                new_game()
            elif result == 'R':  # New game and reset score
                dic_main_options['is_game'] += 1
                new_game(True)
            if result == 'M':  # Go to menu
                dic_main_options['is_game'] = 1
                print_title()
            if result in list(map(str, range(1, 10))):  # str array 1, 2...9
                make_decision(int(result))  # Make turn
            else:
                make_head_of_field(is_err='Вы ввели некорректную команду. Будьте внимательны!')  # err command
        else:
            make_head_of_field(is_err='Вы забыли указать команду!')  # no keyword -> restart field with err

    # In end of game
    if name == 'is_over':
        if result:
            if result == 'N':  # New game
                dic_main_options['is_game'] += 1
                new_game()
            if result == 'M':  # Go to menu
                dic_main_options['is_game'] = 1
                print_title()
            else:
                dic_main_options['is_game'] += 1
                new_game()  # if zero character -> simple restart the game
        else:
            dic_main_options['is_game'] += 1
            new_game()  # if zero character -> simple restart the game
# --------------------


# ------ TURN --------
def change_turn():  # Change turn to another player and return his name
    if dic_main_options['is_p1_turn']:
        dic_main_options['is_p1_turn'] = False
        return dic_main_options['player2']
    else:
        dic_main_options['is_p1_turn'] = True
        return dic_main_options['player1']


def check_winner(char):
    win_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9],  # Combination for win
                [1, 4, 7], [2, 5, 8], [3, 6, 9],
                [1, 5, 9], [3, 5, 7]]
    # get all index in field, where value content 'char'
    list_index = [idx+1 for idx, i in enumerate(list(dic_game_field.values())) if i == char]
    for i in range(len(win_list)):
        if set(win_list[i]).issubset(list_index):  # if winner combination include in field
            return True
    return False


def make_decision(position):
    if dic_game_field[position] != 'X' and dic_game_field[position] != 'O':  # check that current cell is free
        dic_main_options['is_turn'] += 1
        if dic_main_options['is_p1_turn']:
            dic_game_field[position] = 'X'
            make_head_of_field(check_winner('X'))  # check if player 1 win
        else:
            dic_game_field[position] = 'O'
            make_head_of_field(check_winner('O'))  # check if player 2 win
    else:
        make_head_of_field(is_err='Это поле уже занято другим игроком. Введите другое!')
# ----------------------------


# ------- GAME FIELD ---------
def make_head_of_field(is_end=False, is_err=''):
    player_msg = ''
    if is_end and not is_err:  # if some player win -> change score or make a new turn
        if dic_main_options['is_p1_turn']:
            dic_main_options['p1_score'] += 1
            player_msg = dic_main_options['player1']
        else:
            dic_main_options['p2_score'] += 1
            player_msg = dic_main_options['player2']
    elif not is_err:
        player_msg = change_turn()  # get name and make turn

    clear_window()  # remove all info from console
    print(('*' * 33).center(90))
    print(f'* [{colored("X","yellow")}] {dic_main_options["player1"]:15} : [ {dic_main_options["p1_score"]:2}  ] *'.center(98))
    print(f'* [{colored("O","purple")}] {dic_main_options["player2"]:15} : [ {dic_main_options["p2_score"]:2}  ] *'.center(98))
    print(('*' * 33).center(90))
    print(nl)
    if dic_main_options['is_turn'] != 9 or is_end:
        if is_err:  # check errors and print them
            print((f'{colored("Ошибка: ","red")} {is_err}'.center(98)))
        if is_end:  # check the winner and print him
            print(f' Победитель - [ {dic_color["green"]}{player_msg}{dic_color["reset"]} ] !!! '.center(98, '-'))
        else:  # print who will play on this turn
            if dic_main_options['is_ai']:  # if 1 vs PC -> print only one msg
                print(f' [ {colored("Ваш ход!", "yellow")} ] '.center(102, '-'))
            else:  # if 1 vs 1
                if dic_main_options['is_p1_turn']:
                    color = 'yellow'
                else:
                    color = 'purple'
                print(f' Следующий ход за [ {dic_color[color]}{player_msg}{dic_color["reset"]} ] '.center(102, '-'))
    elif dic_main_options['is_turn'] == 9:
        print(f'{colored(" [ Ничья! ] ","green")}'.center(102, '-'))
        print(nl)
        make_game_field(True)
    print(nl)
    make_game_field(is_end)  # is it game over or is it new turn?


def make_game_field(is_end=False):
    align_help = ' ' * 30
    empty_line = align_help + (' ' * 7) + '┃' + (' ' * 7) + '┃' + (' ' * 7)
    line = align_help + '━' * 23
    str_field = f'''
    {empty_line}
    {align_help}   {c_field(1)}   ┃   {c_field(2)}   ┃   {c_field(3)}  
    {empty_line}
    {line}
    {empty_line}
    {align_help}   {c_field(4)}   ┃   {c_field(5)}   ┃   {c_field(6)}  
    {empty_line}
    {line}
    {empty_line}
    {align_help}   {c_field(7)}   ┃   {c_field(8)}   ┃   {c_field(9)}  
    {empty_line}
    
    '''
    print(str_field)

    if is_end:
        make_center_input('is_over')
    else:
        # check game mode and will player play on the first turn
        if dic_main_options['is_ai'] and not dic_main_options['is_p1_turn']:
            ai_turn()
        else:
            make_center_input('in_game')
# ---------------------------


# ------ MAIN MENU ----------
def print_title(is_game=False, state=0):
    clear_window()  # remove all info from console

    arr_menu_state = [' ГЛАВНОЕ МЕНЮ ', ' НАСТРОЙКИ ', ' ВЫБОР ИМЕН ', ' ВЫБОР СЛОЖНОСТИ ']
    align_help_small = " " * 17
    title = f'''{dic_color['yellow']}
     {align_help_small} _____ _         _____             _____          
     {align_help_small}|_   _(_) ___   |_   _|_ _  ___   |_   _|__   ___ 
     {align_help_small}  | | | |/ __|____| |/ _` |/ __|____| |/ _ \ / _ |
     {align_help_small}  | | | | (_|_____| | (_| | (_|_____| | (_) |  __/
     {align_help_small}  |_| |_|\___|    |_|\__,_|\___|    |_|\___/ \___|
                                                    {dic_color['reset']}'''
    if is_game:
        pass
    else:
        print(nl * 2)
        print(('*' * 90 + nl) * 2, end='')
        print(title + nl)
        print('*' * 90)
        print(nl * 5)
        print(arr_menu_state[state].center(90, '-'))
        if state == 0:  # Main menu
            make_center_input('main_menu')
        elif state == 1:  # Option for 1 vs 1
            make_center_input('player_name')
        elif state == 2:  # Set players name
            set_player_name()
        elif state == 3:
            make_center_input('difficult')
# ----------------------------


# ----------- AI -------------
def ai_turn():
    def ai_make_move(cell):
        dic_game_field[cell] = 'O'
        dic_ai['step'] += 1
        dic_main_options['is_turn'] += 1
        last_move = dic_ai['move']
        last_move.append(cell)
        dic_ai['move'] = last_move  # collect pc moves
        make_head_of_field(check_winner('O'))

    def ai_defeat_player():
        def check_combination(search_char):
            # get all index that contain 'char' in the field
            list_index = [idx + 1 for idx, i in enumerate(list(dic_game_field.values())) if i == search_char]
            for i in list(range(1, 10)):
                for ex in dic_player_combination[i]:
                    # Check if player have potentially winning combination -> check if it's possible
                    if set(ex).issubset(list_index) and dic_game_field[i] != 'X' and dic_game_field[i] != 'O':
                        return i  # return key of field for turn
            return False

        can_pc_win_cell = check_combination('O')  # can pc win in next step?
        if can_pc_win_cell:
            return can_pc_win_cell
        else:
            if random.randrange(1, 100) > dic_ai['chance_to_lose']:  # will pc miss winner combination?
                can_p_win_cell = check_combination('X')  # can player win in next step?
                if can_p_win_cell:
                    return can_p_win_cell
                else:
                    return ai_simple_move()  # if no winner combination found

    def ai_simple_move():
        can_use_cell = []
        for i in list(range(1, 10)):
            for ex in dic_player_combination[i]:  # check can pc make potentially winner combination
                if set(dic_ai['move']).issubset(ex) and dic_game_field[i] != 'X' and dic_game_field[i] != 'O':
                    can_use_cell.append(i)  # collect every good cell for combination
        if can_use_cell:
            return random.choice(can_use_cell)  # choose random cell from list of combination
        else:
            # if it's no good cells -> make random move
            # first at all check free cells of field -> than randomly take one of them
            ai_make_move(random.choice(is_cell_clear(list(range(1, 10)))))

    def is_cell_clear(array):
        arr_field = list(dic_game_field.values())  # get data of field
        move_cell = [i for i in arr_field if i in array]  # check which cells free to use
        if move_cell:  # if empty -> use it; if not -> try to generate random step
            return move_cell
        else:
            return random.choice([i for i in arr_field if i != 'X' and i != 'O'])  # search in arr 1-9

    def ai_step():
        correct_move = ''
        if dic_ai['step'] == 1:
            if random.randrange(1, 3) == 1:  # 1 - move by angle; 2 - move by side
                dic_ai['tactic'] = 'angle'  # use corners
                correct_move = is_cell_clear(dic_ai['cell_square'])
            else:
                dic_ai['tactic'] = 'side'  # use sides or center
                correct_move = is_cell_clear(dic_ai['cell_line'])
            ai_make_move(random.choice(correct_move))
        if dic_ai['step'] == 2:
            if dic_main_options['is_p1_start_game']:
                destroy_combination = ai_defeat_player()  # check if pc need to broke player's winner combination
                if destroy_combination:
                    ai_make_move(destroy_combination)
            # player doesn't have potentially winner combination
            if random.randrange(1, 3) == 1:  # 1 - move by angle; 2 - move by side
                correct_move = is_cell_clear(dic_ai['cell_square'])
            else:
                if dic_ai['tactic'] == 'angle':
                    if dic_ai['move'][0] == 1:  # left corner up
                        correct_move = is_cell_clear([2, 4])
                    if dic_ai['move'][0] == 3:  # right corner up
                        correct_move = is_cell_clear([2, 6])
                    if dic_ai['move'][0] == 7:  # left corner down
                        correct_move = is_cell_clear([4, 8])
                    if dic_ai['move'][0] == 9:  # right corner down
                        correct_move = is_cell_clear([6, 8])
                else:
                    if dic_ai['move'][0] == 2:  # up
                        correct_move = is_cell_clear([1, 5, 3])
                    if dic_ai['move'][0] == 4:  # left
                        correct_move = is_cell_clear([1, 5, 7])
                    if dic_ai['move'][0] == 6:  # right
                        correct_move = is_cell_clear([3, 5, 9])
                    if dic_ai['move'][0] == 8:  # down
                        correct_move = is_cell_clear([7, 5, 9])
                    if dic_ai['move'][0] == 5:  # center
                        correct_move = is_cell_clear([1, 2, 3, 4, 6, 7, 8, 9])
            ai_make_move(random.choice(correct_move))
        if dic_ai['step'] > 2:
            destroy_combination = ai_defeat_player()  # check if pc need to broke player's winner combination
            if destroy_combination:
                ai_make_move(destroy_combination)
            else:
                ai_make_move(ai_defeat_player())  # pc will try to create potentially winner combination
        else:
            ai_make_move(ai_defeat_player())
    ai_step()  # let's launch ai
# --------------------------


# -------- LAUNCH ---------
print_title()

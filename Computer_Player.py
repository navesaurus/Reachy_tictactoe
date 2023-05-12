import copy
import random

# Wahrscheinlichkeiten für bestimmte Züge abhängig vom Level
winning = {
    0: 10,
    1: 50,
    2: 100
}

preventing = {
    0: 10,
    1: 50,
    2: 100
}

good = {
    0: 20,
    1: 50,
    2: 100
}

board = []
level = 1
reachy_moveCounter = 0
player_moveCounter = 0

# hier können die Zielkoordinaten für die Bewegung abgelegt werden
coordinates = []

# alle möglichen Gewinnkombinationen
wincombinations = [
    [[0,0], [0,1], [0,2]],
    [[1,0], [1,1], [1,2]],
    [[2,0], [2,1], [2,2]],

    [[0,0], [1,0], [2,0]],
    [[0,1], [1,1], [2,1]],
    [[0,2], [1,2], [2,2]],

    [[0,2], [1,1], [2,0]],
    [[0,0], [1,1], [2,2]]
]
corners = [
    [0,0], [0,2], [2,0], [2,2]
]


# berechnet die Summe der Einträge einer Gewinnkombination
def combovalue(k):
    wert = board[wincombinations[k][0][0]][wincombinations[k][0][1]] + board[wincombinations[k][1][0]][wincombinations[k][1][1]] + board[wincombinations[k][2][0]][wincombinations[k][2][1]];
    return wert


# versuche zu gewinnen (2) oder einen Gewinn zu verhindern (-2)
def make_combo_move(n, p):
    # Gewinn verhindern nur mit gewisser Wahrscheinlichkeit
    if n == -2:
        if p < (100 - preventing[level]):
            return False
    # Gewinnen nur mit gewisser Wahrscheinlichkeit
    if n == 2:
        if p < (100 - winning[level]):
            return False
    print("trying to make combo move")
    # prüfe, ob eine Kombination passt
    for combo in range(len(wincombinations)):
        if combovalue(combo) == n:
            # setze auf das freie Feld in der Kombination
            for i in range(3):
                if board[wincombinations[combo][i][0]][wincombinations[combo][i][1]] == 0:
                    board[wincombinations[combo][i][0]][wincombinations[combo][i][1]] = 1
                    return True
    return False


def corner_move():
    print("trying to make corner_move")
    free_corner = False
    for k in range(4):
        if board[corners[k][0]][corners[k][1]] == 0:
            free_corner = True
    while free_corner:
        i = random.randint(0, 4)
        if board[corners[i][0]][corners[i][1]] == 0:
            board[corners[i][0]][corners[i][1]] = 1
            return True
    return False


def make_good_move(p):
    # nur mit bestimmter Wahrscheinlichkeit guten Zug machen
    if p < (100 - good[level]):
        return False
    print("trying to make good move")

    if reachy_moveCounter == 0 and player_moveCounter == 1:
        # try the middle cell and make move if possible
        if board[1][1] == 0:
            board[1][1] = 1
            return True
        else:
            if corner_move():
                return True

    elif reachy_moveCounter == 1 and player_moveCounter == 1:
        if corner_move():
            return True

    elif reachy_moveCounter == 1 and player_moveCounter == 2:
        # FALLE VERHINDERN
        print("HIER!!")
        if combovalue(board, 6) == -1 or combovalue(board, 7) == -1:
            x = 1
            y = random.randint(0, 2)
            randfeld = [x, y]
            a = random.sample(randfeld, 2)
            board[a[0]][a[1]] = 1
            return True
    # TODO: Zug == 2.1: bei 4+1+4:Rand Feld, sonst Gewinnkombination mit Summe = 1 = 1+0+0
    # if board[1][1] == 0:
    #     board[1][1] = 1
    #     check_state()
    #     return True
    # # else try to get into a corner cell
    # else:
    #     if board[0][0] == 0 or board[0][2] == 0 or board[2][0] == 0 or board[2][2] == 0:
    #         print("picking a corner")
    #         while 1 != 0:
    #             x = random.randint(0, 3)
    #             if x == 0 and board[0][0] == 0:
    #                 board[0][0] = 1
    #                 check_state()
    #                 return True
    #             elif x == 1 and board[0][2] == 0:
    #                 board[0][2] = 1
    #                 check_state()
    #                 return True
    #             elif x == 2 and board[2][0] == 0:
    #                 board[2][0] = 1
    #                 check_state()
    #                 return True
    #             elif x == 3 and board[2][2] == 0:
    #                 board[2][2] = 1
    #                 check_state()
    #                 return True
    #     else:
    #         return False
    return False


def make_random_move():
    print("trying to make random move")
    # generate new coordinates until a free spot is found and place the mark
    target = "start"
    while target != 0:
        # pick two random numbers between 0 and 2
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        # make move if possible
        target = board[x][y]
    else:
        board[x][y] = 1


def make_first_move(currentboard):
    print("trying to make first move")
    tmp_board = copy.deepcopy(currentboard)

    x = random.randint(0, 2)
    if x == 1:
        tmp_board[1][1] = 1
    else:
        y = random.randint(0, 1)
        tmp_board[x][y * 2] = 1
    return tmp_board


# Funktion: Gegner macht auch strategisch gewichtet gute Züge
def make_computer_move(currentboard, currentlevel, reachy_moves, player_moves):
    global board, level, reachy_moveCounter, player_moveCounter
    board = copy.deepcopy(currentboard)
    level = currentlevel
    reachy_moveCounter = reachy_moves
    player_moveCounter = player_moves
    # welcher Zug gemacht wird abh. von p
    p = random.randint(0, 100)
    if not make_combo_move(2, p):
        if not make_combo_move(-2, p):
            if not make_good_move(p):
                make_random_move()
    reachy_moveCounter = reachy_moveCounter + 1
    return board
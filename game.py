import copy


def digits(inp):
    return len(str(inp))


def get_board():
    while True:
        try:
            i, j = map(int, input("Enter your board dimensions: ").split())
            if 0 < i and 0 < j:
                return [[digits(i * j) * '_' for _ in range(1, i + 1)] for _ in range(j, 0, -1)]
            else:
                raise ValueError
        except ValueError:
            print('Invalid dimensions!')


def coord(inp_board, initial=True, message1="Enter the knight's starting position: ", message2='Invalid position!'):
    n, m = len(inp_board), len(inp_board[0])
    while True:
        try:
            i, j = map(int, input(message1).split())
            if 0 < i <= m and 0 < j <= n and (initial or any(n.isdigit() for n in inp_board[-j][i - 1])):
                return i, j
            else:
                raise ValueError
        except ValueError:
            print(message2, end=' ')


def position(inp_board):
    for j, row in enumerate(inp_board):
        for i, cell in enumerate(row):
            if 'X' in cell:
                return i + 1, len(inp_board) - j


def clear(inp_board):
    for j, row in enumerate(inp_board):
        for i, cell in enumerate(row):
            if cell.isdigit():
                inp_board[j][i] = digits(len(inp_board) * len(inp_board[0])) * '_'
    return inp_board


def count_symbol(inp_board, symbol):
    count = 0
    for j, row in enumerate(inp_board):
        for i, cell in enumerate(row):
            if symbol in cell or (symbol == 'digits' and any(n.isdigit() for n in cell)):
                count += 1
    return str(count)


def moves(inp_board, taken=None):
    if not taken:
        taken = []
    i, j = position(inp_board)
    for move in [(i - 2, j + 1), (i - 2, j - 1), (i + 2, j + 1), (i + 2, j - 1),
                 (i + 1, j - 2), (i - 1, j - 2), (i + 1, j + 2), (i - 1, j + 2)]:
        try:
            if move[0] > 0 and move[-1] > 0 and move not in taken:
                inp_board[-move[-1]][move[0] - 1] = 'O'
        except IndexError:
            ...
    return inp_board


def get_moves_count(inp_board, empty_board, taken=None):
    if not taken:
        n, m = position(inp_board)
        taken = [(m, n)]
    for j, row in enumerate(inp_board):
        for i, cell in enumerate(row):
            if 'O' in cell:
                temp = copy.deepcopy(empty_board)
                temp[j][i] = 'X'
                inp_board[j][i] = str(count_symbol(moves(temp, taken), 'O'))
    return inp_board


def check_game(inp_board, path_board=None, hide_solution=False):
    if not int(count_symbol(inp_board, 'digits')):
        coverage = int(count_symbol(inp_board, '*')) + 1
        if coverage == len(inp_board) * len(inp_board[0]):
            if not path_board:
                print('What a great tour! Congratulations!')
                exit()
            if not hide_solution:
                print("Here's the solution!")
                print_board(path_board)
                exit()
            else:
                return 'break'
        else:
            print(f'No more possible moves!\nYour knight visited {coverage} squares!' if not path_board else 'No solution exists!')
            exit()


def print_board(inp_board):
    cell_size = digits(len(inp_board) * len(inp_board[0]))
    print(digits(len(inp_board)) * ' ', end='')
    print((len(inp_board[0]) * (cell_size + 1) + 3) * '-')
    for i, row in enumerate(inp_board):
        print((digits(len(inp_board)) - digits(len(inp_board) - i)) * ' ', end='')
        print(f'{len(inp_board) - i}|', *[(cell_size - len(ij)) * ' ' + ij if ij in ['X', 'O', '*'] or ij.isdigit() else ij for ij in row], '|')
    print(digits(len(inp_board)) * ' ', end='')
    print((len(inp_board[0]) * (cell_size + 1) + 3) * '-')
    print(2 * ' ', *[(cell_size - digits(i)) * ' ' + str(i + 1) for i, col in enumerate(inp_board[0])], '\n')


def play(inp_board, visited_squares, board_copy):
    get_moves_count(moves(inp_board, visited_squares), board_copy, visited_squares)
    print_board(inp_board)
    check_game(inp_board)
    while True:
        i, j = position(inp_board)
        inp_board[-j][i - 1] = '*'
        i, j = coord(inp_board, False, 'Enter your next move: ', 'Invalid move!')
        inp_board = clear(inp_board)
        inp_board[-j][i - 1] = 'X'
        visited_squares.append((i, j))
        get_moves_count(moves(inp_board, visited_squares), board_copy, visited_squares)
        print_board(inp_board)
        check_game(inp_board)


def get_min_no(inp_board):
    min_no = 100
    for j, row in enumerate(inp_board):
        for i, cell in enumerate(row):
            if cell.isdigit() and int(cell) < min_no and int(cell):
                min_no = int(cell)
    return str(min_no) if min_no < 100 else '0'


def get_best_move(inp_board, min_no):
    for j, row in enumerate(inp_board):
        for i, cell in enumerate(row):
            if min_no in cell:
                return i + 1, len(inp_board) - j


def solve(inp_board, visited_squares, board_copy, hide_solution=False):
    move = 1
    path_board = copy.deepcopy(board_copy)
    get_moves_count(moves(inp_board, visited_squares), board_copy, visited_squares)
    check_game(inp_board)
    while True:
        i, j = position(inp_board)
        inp_board[-j][i - 1] = '*'
        path_board[-j][i - 1] = str(move)
        i, j = get_best_move(inp_board, get_min_no(inp_board))
        inp_board = clear(inp_board)
        inp_board[-j][i - 1] = 'X'
        path_board[-j][i - 1] = str(move + 1)  # not so nice
        visited_squares.append((i, j))
        get_moves_count(moves(inp_board, visited_squares), board_copy, visited_squares)
        move += 1
        if hide_solution and check_game(inp_board, path_board, hide_solution) == 'break':
            break
        else:
            check_game(inp_board, path_board)


def yes_or_no():
    while True:
        command = input('Do you want to try the puzzle? (y/n): ')
        if command in ['y', 'n']:
            return command
        else:
            print('Invalid option')


board = get_board()
visited = []
deepcopy = copy.deepcopy(board)
x, y = coord(board)
board[-y][x - 1] = 'X'
visited.append((x, y))

if yes_or_no() == 'y':
    solve(copy.deepcopy(board), copy.deepcopy(visited), deepcopy, True)
    play(board, visited, deepcopy)
else:
    solve(board, visited, deepcopy)

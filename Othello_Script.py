import copy

N = 8

EMPTY = 0
BLACK = 1
WHITE = -1

def initialize_board():
    board = [[EMPTY] * N for _ in range(N)]
    board[3][3] = BLACK
    board[3][4] = WHITE
    board[4][3] = WHITE
    board[4][4] = BLACK
    return board

def print_board(board):
    print("  A B C D E F G H")
    print("  0 1 2 3 4 5 6 7")
    for i in range(N):
        row = str(i) + " "
        for j in range(N):
            if board[i][j] == EMPTY:
                row += ". "
            elif board[i][j] == BLACK:
                row += "X "
            else:
                row += "O "
        print(row)

def is_valid_move(valid_moves, move):
    if move in valid_moves:
        return True
    return False

def get_player_tokens(board, player):
    player_tokens = []
    for row in range(N):
        for column in range(N):
            if board[row][column] == player:
                player_tokens.append((row, column))
    return player_tokens

def get_valid_moves(board, player):
    valid_moves = []
    for token in get_player_tokens(board, player):
        for differenceRow in [-1, 0, 1]: 
            for differenceColumn in [-1, 0, 1]:
                if differenceRow == 0 and differenceColumn == 0:
                    continue
                adyRow = token[0] + differenceRow
                adyCol = token[1] + differenceColumn
                
                if 0 <= adyRow < N and 0 <= adyCol < N and board[adyRow][adyCol] == -player:
                    while 0 <= adyRow < N and 0 <= adyCol < N and board[adyRow][adyCol] == -player:
                        adyRow += differenceRow
                        adyCol += differenceColumn
                        
                    if 0 <= adyRow < N and 0 <= adyCol < N and board[adyRow][adyCol] == EMPTY:
                        valid_moves.append((adyRow, adyCol))
    return valid_moves

def make_move(board, player, move):
    row = move[0]
    col = move[1]
    if not is_valid_move(get_valid_moves(board,player), move):
        return False
    board[row][col] = player
    for differenceRow in [-1, 0, 1]:
        for differenceColumn in [-1, 0, 1]:
            if differenceRow == 0 and differenceColumn == 0:
                continue
            newRow, newColumn = row + differenceRow, col + differenceColumn
            to_flip = []
            while 0 <= newRow < N and 0 <= newColumn < N and board[newRow][newColumn] == -player:
                to_flip.append((newRow, newColumn))
                newRow += differenceRow
                newColumn += differenceColumn
            if 0 <= newRow < N and 0 <= newColumn < N and board[newRow][newColumn] == player:
                for flip_row, flip_col in to_flip:
                    board[flip_row][flip_col] = player
    return True

def get_score(board):
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    return black_score, white_score

def terminal_test(board):
    return all(all(cell != EMPTY for cell in row) for row in board)

def heuristic_weak(board, player):
    black_score, white_score = get_score(board)
    if player == BLACK:
        return black_score - white_score
    else:
        return white_score - black_score

def heuristic_look_for_corners_and_center(board, player):
    value = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                if (i == 0 and j == 0) or (i == 7 and j == 7) or \
                   (i == 0 and j == 7) or (i == 7 and j == 0):
                    value += 20 # Cornes value = 20
                elif (i == 3 and j == 3) or (i == 3 and j == 4) or \
                     (i == 4 and j == 3) or (i == 4 and j == 4):
                    value += 5 # Centers value = 5
                elif (i == 0 and j == 1) or (i == 1 and j == 0) or \
                     (i == 7 and j == 1) or (i == 6 and j == 0) or \
                     (i == 0 and j == 6) or (i == 1 and j == 7) or \
                     (i == 7 and j == 6) or (i == 6 and j == 7) or \
                     (i == 1 and j == 1) or (i == 6 and j == 6) or \
                     (i == 6 and j == 1) or (i == 1 and j == 6):
                    value += 0 # positions adjacent to corners, value = 0
                else:
                    value += 10 # any other position, value = 10
    return value

def heuristic_look_for_corners_and_borders(board, turn):
    value = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == turn:
                if (i == 0 and j == 0) or (i == 7 and j == 7) or \
                   (i == 0 and j == 7) or (i == 7 and j == 0):
                    value += 50 #corners, value = 50
                elif (i == 3 and j == 3) or (i == 3 and j == 4) or \
                     (i == 4 and j == 3) or (i == 4 and j == 4):
                    pass # centers no value
                elif (i == 0 and j == 1) or (i == 1 and j == 0) or \
                     (i == 7 and j == 1) or (i == 6 and j == 0) or \
                     (i == 0 and j == 6) or (i == 1 and j == 7) or \
                     (i == 7 and j == 6) or (i == 6 and j == 7):
                     value -= 1 #positions adjacent to corners, value = -1
                elif (i == 1 and j == 1) or (i == 6 and j == 6) or \
                     (i == 6 and j == 1) or (i == 1 and j == 6):
                     value -= 10 #adjacent diagonal to the corner, value = -10
                elif (i == 0 and j == 2) or (i == 0 and j == 5) or \
                     (i == 7 and j == 2) or (i == 7 and j == 5) or \
                     (i == 2 and j == 0) or (i == 5 and j == 0) or \
                     (i == 2 and j == 7) or (i == 5 and j == 7):
                     value += 5 # border column, value = 5
                elif (i == 0 and j == 3) or (i == 0 and j == 4) or \
                     (i == 7 and j == 3) or (i == 7 and j == 4) or \
                     (i == 3 and j == 0) or (i == 4 and j == 0) or \
                     (i == 3 and j == 7) or (i == 4 and j == 7):
                     value += 2 # border row, value = 2
                else:
                     value += 1 # any other position, value = 1
    return value



def Min_Max_Alpha_Beta_Heuristic_Pruning_heuristic_1(board, depth, player, alpha, beta, maximizing_player):
    if depth == 0 or terminal_test(board):
        return heuristic_look_for_corners_and_center(board, player), 0
    
    valid_moves = get_valid_moves(board, player)
    if maximizing_player:
        max_val = float('-inf')
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, player, move)
            evaluation, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning_heuristic_1(new_board, depth - 1, player, alpha, beta, False)
            
            if evaluation > max_val:
                max_val = evaluation
                best_move = move

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_val, best_move
    else:
        min_val = float('inf')
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, -player, move)
            evaluation, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning_heuristic_1(new_board, depth - 1, player, alpha, beta, True)

            if evaluation < min_val:
                min_val = evaluation
                best_move = move

            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_val, best_move

def Min_Max_Alpha_Beta_Heuristic_Pruning_heuristic_2(board, depth, player, alpha, beta, maximizing_player):
    if depth == 0 or terminal_test(board):
        return heuristic_look_for_corners_and_borders(board, player), 0
    
    valid_moves = get_valid_moves(board, player)
    if maximizing_player:
        max_val = float('-inf')
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, player, move)
            evaluation, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning_heuristic_2(new_board, depth - 1, player, alpha, beta, False)
            
            if evaluation > max_val:
                max_val = evaluation
                best_move = move

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_val, best_move
    else:
        min_val = float('inf')
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, -player, move)
            evaluation, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning_heuristic_2(new_board, depth - 1, player, alpha, beta, True)

            if evaluation < min_val:
                min_val = evaluation
                best_move = move

            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_val, best_move

def get_min_max_move(board, player, depth):
    valid_moves = get_valid_moves(board, player)

    if len(valid_moves) > 0:
        eval, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning_heuristic_1(board, depth, player, float('-inf'), float('inf'), False)
        print(best_move)
        if best_move == 0:
            return get_valid_moves(board, player)[0]
        else:
            return best_move
    else:
        return (-1, -1)

def get_min_max_move_heuristic_2(board, player, depth):
    valid_moves = get_valid_moves(board, player)

    if len(valid_moves) > 0:
        eval, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning_heuristic_2(board, depth, player, float('-inf'), float('inf'), False)
        print(best_move)
        if best_move == 0:
            return get_valid_moves(board, player)[0]
        else:
            return best_move
    else:
        return (-1, -1)

def play_othello_vs_AI():
    board = initialize_board()
    current_player = BLACK
    while True:
        print_board(board)
        print("Actual player:", "X" if current_player == BLACK else "O")
        
        if current_player == WHITE:
            row, col = get_min_max_move(board, current_player, 3)
            if row == -1 and col == -1:
                print("O HAS NO MOVEMENTS")
                current_player = -current_player
                continue
        else:
            while True:
                try:
                    print("My Movements: ",get_valid_moves(board,current_player))
                    if len(get_valid_moves(board,current_player)) == 0:
                        print("You have no movements available")
                        break
                    row = int(input("ROW: "))
                    col = int(input("COLUMN: "))
                    if is_valid_move(get_valid_moves(board,current_player), (row,col)):
                        break
                    print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid entry. Enter valid numbers.")
        
        make_move(board, current_player, (row,col))
        current_player = -current_player
        
        if terminal_test(board):
            print_board(board)
            black_score, white_score = get_score(board)
            if black_score > white_score:
                print("X Won.")
            elif white_score > black_score:
                print("O Won.")
            else:
                print("Tie.")
            break

def play_othello_vs_player():
    board = initialize_board()
    current_player = BLACK
    while True:
        print_board(board)
        print("Actual player:", "X" if current_player == BLACK else "O")
        
        if current_player == BLACK:
            while True:
                try:
                    row = int(input("ROW: "))
                    col = int(input("COLUMN: "))
                    if is_valid_move(get_valid_moves(board,current_player), (row,col)):
                        break
                    else:
                        if len(get_valid_moves(board,current_player)) == 0:
                            current_player = -current_player
                            continue
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid entry. Enter valid numbers.")
            make_move(board, current_player, (row,col))
            current_player = -current_player
        else:
            while True:
                try:
                    row = int(input("ROW: "))
                    col = int(input("COLUMN: "))
                    if is_valid_move(get_valid_moves(board,current_player), (row,col)):
                        break
                    else:
                        if len(get_valid_moves(board,current_player)) == 0:
                            current_player = -current_player
                            continue
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid entry. Enter valid numbers.")
            make_move(board, current_player, (row,col))
            current_player = -current_player
        
        if terminal_test(board):
            print_board(board)
            black_score, white_score = get_score(board)
            if black_score > white_score:
                print("X won.")
            elif white_score > black_score:
                print("O won.")
            else:
                print("Tie.")
                break

def play_othello_AI_vs_AI():
    board = initialize_board()
    current_player = BLACK
    while True:
        print_board(board)
        print("Actual player:", "X" if current_player == BLACK else "O")
        
        if current_player == WHITE:
            row, col = get_min_max_move(board, current_player, 3)
            if row == -1 and col == -1:
                print("O HAS NO MOVEMENTS")
                current_player = -current_player
                continue
        else:
            row, col = get_min_max_move_heuristic_2(board, current_player, 3)
            if row == -1 and col == -1:
                print("X HAS NO MOVEMENTS")
                current_player = -current_player
                continue

        make_move(board, current_player, (row,col))
        current_player = -current_player
        
        if terminal_test(board):
            print_board(board)
            black_score, white_score = get_score(board)
            if black_score > white_score:
                print("X (ROBOCOP) WON. (HEURISTIC 2)")
                print("Total X tokens:", get_score(board)[0])
                print("Total O tokens:", get_score(board)[1])
            elif white_score > black_score:
                print("O (TERMINATOR) WON. (HEURISTIC 1)")
                print("Total X tokens:", get_score(board)[0])
                print("Total O tokens:", get_score(board)[1])
            else:
                print("Tie.")
            break

if __name__ == "__main__":
    opcion = 0
    print("1. PLAYER VS IA")
    print("2. PLAYER VS PLAYER")
    print("3. ROBOCOP 'X' VS TERMINATOR 'O' -> AI vs AI jajaj")
    opcion = int(input("Select a gamemode: "))
    if opcion == 1:
        play_othello_vs_AI()
    elif opcion == 2:
        play_othello_vs_player()
    else:
        play_othello_AI_vs_AI()
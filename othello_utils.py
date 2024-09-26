def is_valid_move(valid_moves, move):
    if move in valid_moves:
        return True
    return False

def get_player_tokens(board, player, board_size):
    player_tokens = []
    for row in range(board_size):
        for column in range(board_size):
            if board[row][column] == player:
                player_tokens.append((row, column))
    return player_tokens

def get_score(board, black, white):
    black_score = sum(row.count(black) for row in board)
    white_score = sum(row.count(white) for row in board)
    return black_score, white_score

def terminal_test(board, EMPTY):
    return all(all(cell != EMPTY for cell in row) for row in board)

def update_max_values(evaluation, max_val, move, best_move):
    if evaluation > max_val:
        return evaluation, move
    return max_val, best_move

def update_min_values(evaluation, min_val, move, best_move):
    if evaluation < min_val:
        return evaluation, move
    return min_val, best_move
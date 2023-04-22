import chess
import chess.pgn

import utils

num_moves_consider = 5
def minmax(board, alpha=-1000, beta=1000, maximize=True, depth=2):
    if depth == 0:
        eval = evaluate_board(board)
        return eval
    if maximize:
        max_eval = - 1000
        legal_moves = list(board.legal_moves)
        for move in legal_moves:#,_ in pairs:
            board.push(move)
            eval = minmax(board, alpha, beta, False,depth-1)
            max_eval = max(max_eval,eval)
            alpha = max(alpha,eval)
            board.pop()
            if beta <= alpha:
                break
        return max_eval
    if not maximize:
        min_eval = 1000
        legal_moves = list(board.legal_moves)
        for move in legal_moves:#,_ in pairs:
            board.push(move)
            eval = minmax(board, alpha, beta, True,depth-1)
            min_eval = min(min_eval,eval)
            beta = min(beta,eval)
            board.pop()
            if beta <= alpha:
                break
        return min_eval


def evaluate_board(position):
    running_eval = 0
    board_matrix = utils.make_matrix(board)
    for row in range(8):
        for col in range(8):
            if board_matrix[row][col] == 'r':
                running_eval -= 5
            if board_matrix[row][col] == 'n':
                running_eval -= 3
            if board_matrix[row][col] == 'b':
                running_eval -= 3
            if board_matrix[row][col] == 'q':
                running_eval -= 9
            if board_matrix[row][col] == 'k':
                running_eval -= 200
            if board_matrix[row][col] == 'p':
                running_eval -= 1
            if board_matrix[row][col] == 'R':
                running_eval += 5
            if board_matrix[row][col] == 'N':
                running_eval += 3
            if board_matrix[row][col] == 'B':
                running_eval += 3
            if board_matrix[row][col] == 'Q':
                running_eval += 9
            if board_matrix[row][col] == 'K':
                running_eval += 200
            if board_matrix[row][col] == 'P':
                running_eval += 1
    return running_eval

if __name__ == "__main__":
    board = chess.Board()
    while True:
        legal_moves = list(board.legal_moves)
        if len(legal_moves) == 0:
            print("You Lose!")
            break
        move_valid = True
        print(board)
        print("What move would you like to play?\n")
        input_from_person = input("prompt")
        try:
            move = board.parse_san(input_from_person)
            board.push(move)
            print("Your move has been registered. Waiting for opponent.")
            legal_moves = list(board.legal_moves)
            best_move = None
            best_eval = 1000
            for enemy_move in legal_moves:
                if len(legal_moves) == 0:
                    print("You Win!")
                    break
                board.push(enemy_move)
                eval = minmax(board,maximize=True)
                if eval <= best_eval:
                    best_move = enemy_move
                    best_eval = eval
                board.pop()
            board.push(best_move)
            print("Enemy Played: ")
            print(best_move)
        # except chess.IllegalMoveError:
        #     pass
        except Exception:
            print("This move was invalid! \n")

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
        move_evals = []
        for move in legal_moves:
            board.push(move)
            current_eval = evaluate_board(board)
            board.pop()
            move_evals.append(current_eval)
        pairs = [(legal_moves[i],move_evals[i]) for i in range(len(legal_moves))]
        pairs.sort(key=lambda x:x[1])
        if len(legal_moves)>num_moves_consider:
            pairs = pairs[0:num_moves_consider]
        for move,_ in pairs:
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
        move_evals = []
        for move in legal_moves:
            board.push(move)
            current_eval = evaluate_board(board)
            board.pop()
            move_evals.append(current_eval)
        pairs = [(legal_moves[i], move_evals[i]) for i in range(len(legal_moves))]
        pairs.sort(key=lambda x:x[1],reverse=True)
        if len(legal_moves) > num_moves_consider:
            pairs = pairs[0:num_moves_consider]
        for move,_ in pairs:
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
                # if row>0:
                #     for other_row in range(row+1, 8):
                #         if board_matrix[other_row][col] == "p":
                #             running_eval +=0.5
                # if 0 < col < 7:
                #     has_pawn = False
                #     for other_row in range(8):
                #         if board_matrix[other_row][col-1] == "p":
                #             has_pawn = True
                #         if board_matrix[other_row][col + 1] == "p":
                #             has_pawn = True
                #     if not has_pawn:
                #         running_eval+= 0.5
                # if row < 7:
                #     if not board_matrix[row+1][col] == '.':
                #         running_eval += 0.5
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
                # if row>0:
                #     for other_row in range(row):
                #         if board_matrix[other_row][col] == "P":
                #             running_eval -=0.5
                # if 0 < col < 7:
                #     has_pawn = False
                #     for other_row in range(8):
                #         if board_matrix[row][col-1] == "P":
                #             has_pawn = True
                #         if board_matrix[row][col + 1] == "P":
                #             has_pawn = True
                #     if not has_pawn:
                #         running_eval -= 0.5
                # if row>0:
                #     if not board_matrix[row-1][col] == '.':
                #         running_eval -= 0.5
    return running_eval

if __name__ == "__main__":
    board = chess.Board()
    while True:
        legal_moves = list(board.legal_moves)
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
                board.push(enemy_move)
                eval = minmax(board,maximize=True)
                if eval <= best_eval:
                    best_move = enemy_move
                    best_eval = eval
                board.pop()
            board.push(best_move)
            print("Enemy Played: ")
            print(best_move)
        except chess.IllegalMoveError:
            pass
        # except Exception:
        #     print("This move was invalid! \n")
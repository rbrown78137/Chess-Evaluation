import pickle

import stockfish
import chess.pgn
positions = []
engine = chess.engine.SimpleEngine.popen_uci("/home/ryan/dev/Class Stuff/371/chessai/stockfish-ubuntu-20.04-x86-64")

for pgn_idx in range(25000):
    pgn = open("/media/ryan/3826-AC45/LICHESS/Small Set/Test/"+str(pgn_idx+1)+".pgn")
    first_game = chess.pgn.read_game(pgn)
    board = first_game.board()
    print("Reading Game: " + str(pgn_idx+1))
    move_idx = 0
    for move in first_game.mainline_moves():
        board.push(move)
        info = engine.analyse(board, chess.engine.Limit(depth=10))
        eval = 0.0
        if hasattr(info["score"].relative, 'moves'):
            mate_string = str(info["score"].relative)[1:-1]
            mate_string_turn = info["score"].turn
            if mate_string == "+":
                if mate_string_turn:
                    eval = 10
                else:
                    eval = -10

            if mate_string == "-":
                if mate_string_turn:
                    eval = -10
                else:
                    eval = 10

            test = 1
        else:
            eval = info["score"].relative.cp * (-1 + 2 *int(info['score'].turn))/100
            if eval < -10:
                eval = -10
            if eval > 10:
                eval = 10
        # print(board.fen())
        positions.append((board.fen(), eval))
        print("  Move IDX: "+str(move_idx)+ " eval: "+str(eval))
        move_idx+=1
with open('position_data.pkl', 'wb') as f:
        pickle.dump(positions, f)
print("Pickle Finished")
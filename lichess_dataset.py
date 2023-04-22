import math
import pickle
import matplotlib
import torch
from torch.utils.data import Dataset
import os
import cv2 as cv
import matplotlib.pyplot as plt
import chess


class ChessDataset(Dataset):
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.data =[]
        with open('position_data.pkl', 'rb') as f:
            self.data = pickle.load(f)
        # Set File Count and Maps To Files
        self.total_images = len(self.data)

    def __len__(self):
        return self.total_images

    def __getitem__(self, idx):
        # print(idx)
        image = torch.zeros(12, 8, 8, dtype=torch.float).to(self.device)
        chess_position = self.data[idx]
        label = torch.tensor([chess_position[1]]).to(self.device).to(torch.float)
        board = chess.Board(chess_position[0])
        turn = board.turn
        board_matrix = make_matrix(board)
        for row in range(8):
            for col in range(8):
                if board_matrix[row][col] == 'r':
                    image[0][row][col] = 1
                if board_matrix[row][col] == 'n':
                    image[1][row][col] = 1
                if board_matrix[row][col] == 'b':
                    image[2][row][col] = 1
                if board_matrix[row][col] == 'q':
                    image[3][row][col] = 1
                if board_matrix[row][col] == 'k':
                    image[4][row][col] = 1
                if board_matrix[row][col] == 'p':
                    image[5][row][col] = 1
                if board_matrix[row][col] == 'R':
                    image[6][row][col] = 1
                if board_matrix[row][col] == 'N':
                    image[7][row][col] = 1
                if board_matrix[row][col] == 'B':
                    image[8][row][col] = 1
                if board_matrix[row][col] == 'Q':
                    image[9][row][col] = 1
                if board_matrix[row][col] == 'K':
                    image[10][row][col] = 1
                if board_matrix[row][col] == 'P':
                    image[11][row][col] = 1
        if not turn:
            image = image * -1
        return image, label


def make_matrix(board): #type(board) == chess.Board()
    pgn = board.epd()
    foo = []  #Final board
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []  #This is the row I make
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('.')
            else:
                foo2.append(thing)
        foo.append(foo2)
    return foo
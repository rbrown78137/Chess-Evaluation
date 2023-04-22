import pickle

import utils
from model import EvaluationModel
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

if __name__ == "__main__":
    model = EvaluationModel().to(device)
    model.load_state_dict(torch.load("saved_models/network.pth"))

    data = []
    with open('position_data.pkl', 'rb') as f:
        data = pickle.load(f)

    # Test case 1
    print("Test Case 1: \n")
    print("Game ")
    print(data[0][0])
    print("Prediction")
    print(model(utils.convert_board_to_tensor(data[0][0])).to("cpu").item())
    print("Truth")
    print(data[0][1])

    print("Test Case 2: \n")
    print("Game ")
    print(data[17][0])
    print("Prediction")
    print(model(utils.convert_board_to_tensor(data[17][0])).to("cpu").item())
    print("Truth")
    print(data[17][1])

    print("Test Case 3: \n")
    print("Game ")
    print(data[1100][0])
    print("Prediction")
    print(model(utils.convert_board_to_tensor(data[1100][0])).to("cpu").item())
    print("Truth")
    print(data[1100][1])

    print("Test Case 4: \n")
    print("Game ")
    print(data[80][0])
    print("Prediction")
    print(model(utils.convert_board_to_tensor(data[80][0])).to("cpu").item())
    print("Truth")
    print(data[80][1])
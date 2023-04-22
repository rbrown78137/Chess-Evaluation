import torch
from torch import nn

from model import EvaluationModel
from lichess_dataset import ChessDataset

device = "cuda" if torch.cuda.is_available() else "cpu"

batch_size = 32
num_epochs = 1000
learning_rate = 0.001  # was 0.00001 for 200 epoch model

dataset = ChessDataset()

train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

model = EvaluationModel().to(device)
model.load_state_dict(torch.load("saved_models/network.pth"))
loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=0)

num_total_steps = len(train_loader)
num_total_steps_in_test = len(test_loader)
lowest_validation_loss = 1000

for epoch in range(num_epochs):
    lossForEpoch = 0
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        loss = loss_function(outputs, labels)
        lossForEpoch += loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch: {epoch} Loss: {lossForEpoch/train_size*batch_size}")
    if epoch > 0:
        with torch.no_grad():
            validation_loss_total = 0
            for i, (images, labels) in enumerate(test_loader):
                labels = labels.to(device)
                predictions = model(images.to(device))
                ground_truths = labels.to(device)
                validation_loss = loss_function(predictions, ground_truths)
                validation_loss_total += validation_loss * batch_size

            average_validation_loss = validation_loss_total/ test_size

            print(f"Epoch: {epoch} Validation Loss: {average_validation_loss}")

            if average_validation_loss < lowest_validation_loss:
                lowest_validation_loss = average_validation_loss
                PATH = './saved_models/network' + '.pth'  # + str(epoch) + '.pth'
                torch.save(model.state_dict(), PATH)
                print('Saved Model')

print('Finished Training')
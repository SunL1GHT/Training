import torch
import torchvision
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision import transforms
from torch.autograd import Variable
from torch import optim
import torch.nn as nn
import torch.nn.functional as F
from model import LeNet
from train import Trainer
import time

learning_rate = 1e-3
batch_size = 64
epoches = 50

trans_img = transforms.ToTensor()

trainset = MNIST('./data', train=True, download=False, transform=trans_img)
testset = MNIST('./data', train=False, download=False, transform=trans_img)

trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=4)
testloader = DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=4)

lenet = LeNet()

criterion = nn.CrossEntropyLoss(size_average=False)
optimizer = optim.SGD(lenet.parameters(), lr=learning_rate)

trainer = Trainer(lenet, criterion)
print('starting train......')
trainer.train(10, trainloader, optimizer)

print('finish train..................')
print()
print()
sum = 0
runloss = 0
correct = 0
for _, batch in enumerate(testloader):
    input, target = batch

    sum += len(target)

    input = Variable(input)
    target = Variable(target)
    output = lenet(input)
    loss = criterion(output, target)

    runloss += loss.data[0]
    _, predict = torch.max(output, 1)
    correctnum = (predict == target).sum()
    correct += correctnum.data[0]

epoch_loss = runloss / sum
epoch_correct = correct / sum
print("test:  epoch loss {:f}   epoch_correct {:f}".format(epoch_loss, epoch_correct))

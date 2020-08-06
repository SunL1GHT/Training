import numpy as np
import torch
from torchvision.datasets import MNIST
from torch.autograd import Variable


class Trainer(object):
    def __init__(self, model, criterion):
        super(Trainer, self).__init__()
        self.model = model
        self.criterion = criterion

    def train(self, epoch, dataloader, optimizer):
        self.model.train()

        for i in range(epoch):
            sum = 0
            runloss = 0
            correct = 0
            for _, batch in enumerate(dataloader):
                input, target = batch

                sum += len(target)

                input = Variable(input)
                target = Variable(target)
                output = self.model(input)
                loss = self.criterion(output, target)
                optimizer.zero_grad()

                loss.backward()
                optimizer.step()
                runloss += loss.data[0]
                _, predict = torch.max(output, 1)
                correctnum = (predict == target).sum()
                correct += correctnum.data[0]

            epoch_loss = runloss / sum
            epoch_correct = correct / sum
            print("epoch {:d}  epoch loss {:f}   epoch_correct {:f}".format(i, epoch_loss, epoch_correct))


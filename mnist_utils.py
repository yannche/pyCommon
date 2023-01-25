
import torch
from   torch.utils.data.dataloader import DataLoader
from   torchvision import datasets
from   torchvision import transforms
from   torch.nn.functional import softmax

import numpy as np
import matplotlib.pyplot as plt



def visualize_pytorch_classifier(X, y, predict=None,**kwargs):
    if len(y.shape) == 2:
        y = y.squeeze()
 
    X_ = X.data.numpy()
    y_ = y.data.numpy()
    
    ax = plt.gca()
    
    # Plot the training points
    ax.scatter(X_[:, 0], X_[:, 1], c=y_, s=30, cmap='rainbow',
               clim=(y_.min(), y_.max()), zorder=3)
    ax.axis('tight')
    #ax.axis('off')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    if predict:
        xx, yy = np.meshgrid(np.linspace(*xlim, num=200),
                             np.linspace(*ylim, num=200))
        xxyy   = np.c_[xx.ravel(), yy.ravel()]
        Z      = np.array([predict((torch.from_numpy(d)).float()).data.numpy()
                           for d in xxyy]).reshape(xx.shape)

        # Create a color plot with the results
        n_classes = len(np.unique(y.data.numpy()))
        contours = ax.contourf(xx, yy, Z, alpha=0.3,
                               levels=np.arange(n_classes + 1) - 0.5,
                               cmap='rainbow', #clim=(y_.min(), y_.max()),
                               zorder=1)

        ax.set(xlim=xlim, ylim=ylim)

        if kwargs['return_arrays']: return xx,yy,Z

        

def load_mnist():
    train_dataset = datasets.MNIST(root='./data/',
                                           train=True, 
                                           transform=transforms.ToTensor(),
                                           download=True)

    test_dataset = datasets.MNIST(root='./data/',
                                          train=False, 
                                          transform=transforms.ToTensor(),
                                          download=True)

    train_loader = DataLoader( dataset=train_dataset,
                               batch_size=100000, 
                               shuffle=True)

    test_loader = DataLoader( dataset=test_dataset,
                              batch_size=100000,
                              shuffle=False)

    mnist_data = next(iter(train_loader))
    X,Y = mnist_data[0].squeeze(),mnist_data[1]
    
    test_mnist_data = next(iter(test_loader))
    X_test,Y_test = test_mnist_data[0].squeeze(),test_mnist_data[1]
    return X-0.13,Y,X_test-0.13,Y_test  # centrage, mais pas de réduction


def multiclass_accuracy(model,X,Y):
    pred_probabilies = softmax(model(X),dim=0)
    probable_class   = pred_probabilies.argmax(dim=1)
    return torch.mean((probable_class == Y).float()).item()


class View(torch.nn.Module):
    def __init__(self, *args):
        super().__init__()
        self.shape = args

    def forward(self, x):
        return x.view(self.shape)

class Flatten(torch.nn.Module):
    def forward(self, input):
        return input.view(input.size(0), -1)



def pytorch_fit(model, X,Y, X_test, Y_test, criterion, optimizer, n_epochs=200):
    # on switche le modèle en mode entrainement (important pour le dropout uniquement)
    model.train()
    
    # on parcourt "n_epochs" fois l'ensemble des donnees
    for i in range(n_epochs):

        # le "dataloader" va fournir des mini-batches de 32 examples a la fois.
        dataloader = torch.utils.data.DataLoader(list(zip(X,Y)), batch_size=32,shuffle=True)

        for inputs,labels in dataloader:

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels) # calcul du cout
            loss.backward()                   # calcul du gradient
            optimizer.step()                  # un pas de descente de gradient

        if i%(n_epochs//5)==0:
            cout_test = criterion(model(X_test),Y_test).item()
            cout_train= criterion(model(X),Y).item()
            print("epoch ",i," , cout (en test) de ",cout_test," , cout (en train) de ",cout_train)
    
    # on switche le modèle en mode prediction
    model.eval()


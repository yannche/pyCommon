import torch as t
import numpy as np
import matplotlib.pyplot as plt

def visualize_pytorch_classifier(X, y, predict=None,**kwargs):
    X_ = X.detach().numpy()
    y_ = y.detach().numpy()
    
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
        Z      = np.array([predict((t.from_numpy(d)).float(),**kwargs).data.numpy()
                           for d in xxyy]).reshape(xx.shape)

        # Create a color plot with the results
        n_classes = len(np.unique(y.data.numpy()))
        contours = ax.contourf(xx, yy, Z, alpha=0.3,
                               levels=np.arange(n_classes + 1) - 0.5,
                               cmap='rainbow', #clim=(y_.min(), y_.max()),
                               zorder=1)

        ax.set(xlim=xlim, ylim=ylim)

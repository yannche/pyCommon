import numpy as np
import matplotlib.pyplot as plt

def Relu(a):
    return (a>0)*a

def visualize(X,Y,W,V=None):
    fig,ax = plt.subplots()
    y = np.argmax(Y,axis=1)
    ax.scatter(*X[:,:2].T,c=y)
    
    #ax.axis('tight')
    #ax.axis('off')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    xx, yy = np.meshgrid(np.linspace(*xlim, num=100),
                        np.linspace(*ylim, num=100))

    _x = np.c_[xx.ravel(), yy.ravel(),np.ones_like(xx).ravel()].T
    _a = W @ _x
    if V is None:
        _z = a
    else:
        _z = V @ Relu(_a)

    _pred = _z.argmax(axis=0)
    _pred = _pred.reshape(xx.shape)

    # Create a color plot with the results
    n_classes = len(np.unique(y))
    contours = ax.contourf(xx, yy, _pred, alpha=0.3,
                           #levels=np.arange(n_classes + 1) - 0.5,
                           #clim=(y.min(), y.max()),
                           zorder=1)

    #ax.set(xlim=xlim, ylim=ylim)

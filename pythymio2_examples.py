# -*- coding: utf-8 -*-
from pythymio2 import *
import time


### Test ###
def monCodeTest():
    x = yield "prox"
    print "capteurs de distance:",x

    print "je dors 2 secondes"
    yield "sleep 2"
    
    print "j'avance 1 seconde"
    av()
    yield "sleep 1"
    arrete()
    
    x = yield "prox"
    print "capteurs de distance :",x
    
    x = yield "buttons"
    print "boutons:",x



runThymioControl(monCodeTest)



### evitement d'obstacle ###
def eviteObstacles():
    yield "sleep 1"
    av()
    for i in range(100):

        x = yield "prox"
        print x
        if x[0] > 1000 or x[4] > 1000:
            if x[0] > x[1]:
                td()
                yield "sleep 0.2"
            else:
                tg()
                yield "sleep 0.2"
        else:
                av()
                yield "sleep 0.2"          
    arrete()



#runThymioControl(eviteObstacles)

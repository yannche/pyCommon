# -*- coding: utf-8 -*-
from pythymio2 import *
import time


### evitement d'obstacle ###
def eviteObstacles():
    
    av()
    for i in range(20):

        x = yield "prox"
        print "iter",i," => ",x[:5]
        
        if x[0] > 1000 or x[4] > 1000:
            if x[0] > x[1]:
                print "td"
                td()
                yield "sleep 0.2"
            else:
                print "tg"
                tg()
                yield "sleep 0.2"
        else:
                av()
                yield "sleep 0.2"          
    arrete()



runThymioControl(eviteObstacles)

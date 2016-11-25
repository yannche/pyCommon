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

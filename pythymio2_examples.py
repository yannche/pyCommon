# -*- coding: utf-8 -*-
import pythymio2
import time


def affiche_dix_evennements(evennement):
    for i in range(10):
        while True:
            ev = evennement("fwd.prox",(yield))
            if ev is not None:
                break

        print "=>",ev
    
#pythymio2.call(affiche_dix_evennements)
    

#######################################################



def Attend_appuie_touche_et_stop(evennement):
    while True:
        if evennement("fwd.button.center",(yield)):
            break

#pythymio2.call(Attend_appuie_touche_et_stop)


#######################################################


def Affiche_prox_horizontals(evennement):
    while True:
        p = evennement("fwd.prox",(yield))
        if p is not None:
            print p[:7]
        if evennement("fwd.button.center"):
            print "fini!"
            break

#pythymio2.call(Affiche_prox_horizontals)

#######################################################


def JeFonceEtJarrettePresDuMur(evennement):
    pythymio2.av()
    while True:
        p = evennement("fwd.prox",(yield))
        
        if p is not None and p[2] > 1000:
            pythymio2.arrete()
            print 'fin'
            break

#pythymio2.call(JeFonceEtJarrettePresDuMur)

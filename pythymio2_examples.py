# -*- coding: utf-8 -*-
import pythymio2
import time


def affiche_dix_evennements():
    
    def monmain(evennement):
        for i in range(10):
            ev = evennement("fwd.prox.horizontal",(yield))
            print "=>",ev
    
    pythymio2.call(monmain)
    

#######################################################



def Attend_appuie_touche_et_stop():
    def monmain(evennement):
        while True:
            if evennement("fwd.button.center",(yield)):
                break

    pythymio2.call(monmain)


#######################################################


def Affiche_prox_horizontals():
    def monmain(evennement):
        while True:
            p = evennement("fwd.prox",(yield))
            if p is not None:
                print p[:7]
            if evennement("fwd.button.center"):
                print "fini!"
                break

    pythymio2.call(monmain)

#Affiche_prox_horizontals()
#######################################################


def JeFonceEtJarrettePresDuMur():
    def monmain(evennement):
        pythymio2.av()
        while True:
            p = evennement("fwd.prox",(yield))
            
            if p is not None and p[2] > 1000:
                pythymio2.arrete()
                print 'fin'
                break

    pythymio2.call(monmain)

JeFonceEtJarrettePresDuMur()

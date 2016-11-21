from pythymio import *
import time

def av(Thym,l=500,r=500):
    Thym.set('motor.left.target', [l])
    Thym.set('motor.right.target', [r])

def td(Thym):
    av(Thym,500,-500)
    
def tg(Thym):
    av(Thym,-500,500)

def arrete(Thym):
    av(Thym,0,0)
    

"""
class Temps:
    def __init__(self):
        self.reset()

    def reset(self):
        self.t = time.time()

    def reveille(self,secondes):
        " devient TRUE au bout de "secondes" secondes "
        assert self.t is not None,"appeler reset() sur l'objet Temps apres utilisation"
        if time.time() - self.t > secondes:
            self.t = None
            return True
        else:
            return False
"""

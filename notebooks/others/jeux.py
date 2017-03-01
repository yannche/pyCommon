from __future__ import print_function
import random
import numpy as np
from functools import partial

class Jeu:
    def __init__(self,mat1,mat2=None):
        mat1 = np.matrix(mat1,dtype=np.float)
        if mat2 is None: # zero sum game
            mat2 = -mat1
        mat2 = np.matrix(mat2,dtype=np.float)
        self.nactions,_ = mat1.shape
        assert mat1.shape == (self.nactions,self.nactions) and mat2.shape == (self.nactions,self.nactions)
        self.mat1     = mat1
        self.mat2     = mat2

    def gain1(self,a1,a2):
        return self.mat1[a1,a2]

    def gain2(self,a1,a2):
        return self.mat2[a1,a2]

    def gains(self,a1,a2):
        return self.gain1(a1,a2),self.gain2(a1,a2)

    def play(self,player1,player2,niterations=100,verb=False):
        self.sumJ1,self.sumJ2 = 0.0,0.0
        p1 = player1(self.mat1,self.mat2)
        p2 = player2(self.mat2.T,self.mat1.T)
        a1 = next(p1)
        a2 = next(p2)
        try:
            for t in range(niterations):
                g1,g2 = self.gains(a1,a2)
                if verb:
                    print('\n--- Iteration ',t,' ---')
                    print('   J1(',player1.__name__,') et J2(',player2.__name__,') jouent ',(a1,a2),' et gagnent ',(round(g1,2),round(g2,2)))
                a1,a2 = p1.send( (a2,g1,g2) ),p2.send( (a1,g2,g1) )
                self.sumJ1 += g1
                self.sumJ2 += g2
        except StopIteration:
            pass
        if verb:
            g1,g2 = self.sumJ1,self.sumJ2
            print ('\n--- Score Final ---\n J1 et J2 ont gagne ',(round(g1,2),round(g2,2)))
            print (' Vainqueur : ','J1' if g1 >= g2 else 'J2','\n')

    def multiple_plays(self,player1,player2,niterations=100,nplays=10,verb=False):
        self.totalsumJ1,self.totalsumJ2 = 0.0,0.0
        for t in range(nplays):
            self.play(player1,player2,niterations,verb)
            self.totalsumJ1 += self.sumJ1
            self.totalsumJ2 += self.sumJ2
        if verb:
            g1,g2 = self.totalsumJ1,self.totalsumJ2
            print ('\n-----------------------------------')
            print ('--- Score sur plusieurs parties ---\n J1 et J2 ont ',(round(g1,2),round(g2,2)))
            print (' Vainqueur : ','J1' if g1 >= g2 else 'J2','\n')

        return self.totalsumJ1,self.totalsumJ2

matching_pennies = Jeu([[1,-1],[-1,1]])

random_zerosum_game = Jeu(np.random.rand(3,3)-0.5)

def my_inorder_player(mat1,mat2,_reverse=False):
    nactions = len(mat1)
    r = range(nactions)
    if _reverse: r.reverse()
    for a1 in r:
        a2,g1,g2 = yield a1

def my_biased_player(mat1,mat2):
    nactions = len(mat1)
    while True:
        a1 = random.choice(list(range(nactions))+[0])
        a2,g1,g2 = yield a1


def my_rand_player(mat1,mat2):
    nactions = len(mat1)
    while True:
        a1  = random.randint(0,nactions-1)
        a2,g1,g2  = yield a1
        print ("je joue l'action ",a1," et l'autre joueur joue ",a2)

def my_fictitious(mat1,mat2):
    nactions = len(mat1)
    freqs = np.ones(nactions)
    while True:
        print (freqs/np.sum(freqs))
        a1 = np.argmax( mat1 * np.matrix(freqs).T )
        a2,g1,g2 = yield a1
        freqs[a2] += 1


def my_dummycopy(mat1,mat2):
    nactions = len(mat1)
    i = 1
    a = random.randint(0,nactions-1)
    while True:
        a,g1,g2 = yield a

def jeux__test():
    for i in range(20): print ('\n')
    matching_pennies.play(my_biased_player,my_fictitious,100,verb=True)
    print ("\n\n")
    random_zerosum_game.multiple_plays(my_rand_player,my_rand_player,niterations=100,nplays=2,verb=True)

if __name__ == '__main__':
    jeux__test()
    pass

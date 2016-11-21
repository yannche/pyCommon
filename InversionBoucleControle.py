from collections import deque,defaultdict
from functools   import partial


class EventQueue:
    def __init__(self):
        self.d = defaultdict( partial(deque,maxlen=1000) )

    def push(self,name,arg):
        # traitement sur le format des arguments
        arg = list(map(float,arg))
        if name == "fwd.button.center" and arg == []:
            arg = True
        self.d[name].append( arg )

    def isEmpty(self,name):
        return len(self.d[name])==0

    def pop(self,name):
        return self.d[name].popleft()

    def queueLoop(self,user_fun):
        userAgent        = user_fun()
        answerSentToUser = None  # initially, nothing sent to user
        try:
            while True:
                # send answer to previous request and get new request
                userRequest = userAgent.send( answerSentToUser )

                print "l'utilisateur demande ",userRequest
                # while no event in queue matches the user's request
                while self.isEmpty(userRequest):
                    # ask thymio for event, and push in queue
                    n,a = yield
                    self.push(n,a)

                # send the requested event to user and get next request
                answerSentToUser = self.pop(userRequest)

        except StopIteration:
            pass

def affiche_evennements():
    ev = yield "n3"
    print "n3 =>",ev
    ev = yield "n1"
    print "n1 =>",ev
    ev = yield "n8"
    print "n8 =>",ev
    ev = yield "n12"
    print "n12 =>",ev
    print 'fin de ma fonction affiche_evennements'


def thymio_eventloop_simulator():
    eq = EventQueue()
    queueLoopGenerator = eq.queueLoop(affiche_evennements)
    queueLoopGenerator.next()

    for i in range(20):
        try:
            print "creation de l'evennement name=n"+str(i),", arg="+str([str(i)])
            queueLoopGenerator.send(('n'+str(i),[str(i)]))
        except StopIteration:
            break

    print "end of event loop successfully reached"


thymio_eventloop_simulator()

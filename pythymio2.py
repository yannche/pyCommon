import pythymio
from collections import deque



#### Evennements ####



class EventQueue:
    def __init__(self):
        self.d = dict()

    def __call__(self,fname,ev_name_arg=None):
        """
        s'utilise comme ca:
        data = evQueue("prox",yield)
        """
        if ev_name_arg is not None:

            ev_name,ev_arg = ev_name_arg
    
            # traitement sur le format des arguments
            ev_arg = list(map(float,ev_arg))
            if ev_name == "fwd.button.center":
                if ev_arg == []:
                    ev_arg = True
    
            # empilage
            if ev_name not in self.d:
                self.d[ev_name] = deque(maxlen=1000)
            self.d[ev_name].append( ev_arg )

        if fname not in self.d:
            self.d[fname] = deque(maxlen=1000)
        if len(self.d[fname]) == 0:
            return None
        else:
            return self.d[fname].popleft()



def call(func,eventlist=None):

    if eventlist is None:
        eventlist = ["prox","button.center"]

    with pythymio.thymio(eventlist,[]) as Thym:
        call.Thym=Thym
        monmain_generator = func( EventQueue() )
        monmain_generator.send(None)
        def dispatch(evtid, evt_name, evt_args):
            try:
                monmain_generator.send((evt_name,evt_args))
            except StopIteration:
                Thym.stop()

        Thym.loop(dispatch)

#### Moteurs ####

def av(l=500,r=500):
    call.Thym.set('motor.left.target', [l])
    call.Thym.set('motor.right.target', [r])

def td():
    av(500,-500)
    
def tg():
    av(-500,500)

def arrete():
    av(0,0)
    


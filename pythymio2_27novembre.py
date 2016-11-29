from collections import deque,defaultdict
from functools   import partial
import time
import pythymio
import types

MOTOR_COEF_LEFT  = 1.0
MOTOR_COEF_RIGHT = 1.0

class EventQueue:
	
    def __init__(self,listEvents):
		self._d = {name:deque(maxlen=1) for name in listEvents}
		self.listEvents = listEvents


	def d(self,name):
		""" safe access to dictionary self._d """
        try:
			return self._d[name]
		except KeyError:
			raise Exception('les seuls evennements autorises sont'+str(self.listEvents))


    def _parse_sleep_request(self,s):
        """ parses string of the form "sleep x" where x is a float, and returns x
            if parsing fails, returns False
        """
        try:
            s1,s2 = s.split(' ')
            assert s1 == 'sleep'
            return float(s2)
        except:
            return False
    

    def push(self,name,arg):
        """ push event on eventqueue
        """
		name=name.replace('fwd.','')
		try:
			# tries to convert into list of floats
			# If conversion fails, keep original type
			arg = list(map(float,arg))
        except ValueError,TypeError:
			pass
        self.d(name).append( arg )


    def isEmpty(self,name):
        """ returns True if eventqueue named "name" is empty """
		return len(self.d(name))==0


    def pop(self,name):
        return self.d(name).popleft()		


    def queueLoop(self,userAgent):
		
		# initially, nothing is sent to user
		answerSentToUser = None  

        try:
            while True:
                # send answer to previous request and get new request
                userRequest = userAgent.send( answerSentToUser )

                # is it a sleep request of the form "sleep x" ?
                sleepReq = self._parse_sleep_request(userRequest)    
				t0 = time.time()

                if sleepReq:
					# while the sleep request has not ended           
                    def continue_condition(): return time.time() < t0+sleepReq
                else:
                    # while no event in queue matches the user's request,
					def continue_condition(): return self.isEmpty(userRequest)


				while continue_condition():
                        # ask thymio for event, and push in queue
                        n,a = yield
                        self.push(n,a)

				# send the requested event to user (or None if sleepReq) and get next request
				answerSentToUser = None if sleepReq else self.pop(userRequest)


        except StopIteration:
            pass




def runThymioControl(userFun,eventlist=None):

    if eventlist is None:
        eventlist = ["prox","buttons"]

    eq = EventQueue(eventList)

    with pythymio.thymio(eventlist,[]) as Thym:

		# initialize runThymioControl.Thym for use by functions av(), td()...
        runThymioControl.Thym=Thym

		# check user_fun() takes no parameters and returns a generator
		try:
			userAgent = user_fun()
			if not isinstance(userAgent,types.GeneratorType): return None
		except TypeError: 
			raise TypeError('Votre fonction ne doit pas prendre de parametre')

		# connect event queue with userAgent
        queueLoopGenerator = eq.queueLoop(userAgent)
        queueLoopGenerator.next()


        def dispatch(evtid, evt_name, evt_args):
            try:
                queueLoopGenerator.send((evt_name,evt_args))
            except StopIteration:
                Thym.stop()

        Thym.loop(dispatch)


#### Moteurs ####

def av(l=500,r=500):
    runThymioControl.Thym.set('motor.left.target', [int(l*MOTOR_COEF_LEFT)])
    runThymioControl.Thym.set('motor.right.target', [int(r*MOTOR_COEF_RIGHT)])

def td():
    av(500,-500)
    
def tg():
    av(-500,500)

def arrete():
    av(0,0)
    


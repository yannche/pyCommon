import dbus
import dbus.mainloop.glib
import gobject
from optparse import OptionParser
 


ThymioVariables = ["event.args", "button.backward", "button.left", "button.center", "button.forward", "button.right", "prox.horizontal", "prox.comm.rx", "prox.comm.tx", "prox.ground.ambiant", "prox.ground.reflected", "prox.ground.delta", "motor.left.target", "motor.right.target", "motor.left.speed", "motor.right.speed", "motor.left.pwm", "motor.right.pwm", "acc", "temperature", "rc5.address", "rc5.command", "mic.intensity", "mic.threshold", "timer.period"]

ThymioEvents = ["button.backward", "button.left", "button.center", "button.forward", "button.right", "buttons", "prox", "prox.comm", "tap", "acc", "mic", "sound.finished", "temperature", "rc5", "motor", "timer0", "timer1"]

def get_var(s):
    def get_variables_reply(r):
        print ('asked: "%s" got: %s'%(s, str(r)))
    return get_variables_reply

def get_var_err(s):
    def get_variables_error(e):
        print 'asked %s error: %s'%(s, str(e))
#        loop.quit()
    return get_var_err

def Demo():
    for var in ThymioVariables:
        network.GetVariable("thymio-II",
                            var, 
                            reply_handler = get_var(var),
                            error_handler = get_var_err(var))
    return True


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
 
    (options, args) = parser.parse_args()
 
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
 
    if options.system:
        bus = dbus.SystemBus()
    else:
        print "using session bus"
        bus = dbus.SessionBus()
 
    #Create Aseba network 
    network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
 
    #print in the terminal the name of each Aseba NOde
    print network.GetNodesList()
 
    #GObject loop
    print 'starting loop'
    loop = gobject.MainLoop()
 #call the callback of Braitenberg algorithm
    handle = gobject.timeout_add (20000, Demo) #20s
    loop.run()


# -*- coding: utf-8 -*-
import pythymio2
import time

with pythymio2.thymio(["buttons","motor","prox"],[]) as Thym:
    temps = time.time()
    cnt   = 0
    def dispatch(evtid, evt_name, evt_args):
        global temps,cnt

        cnt +=1
        if cnt == 1:
            pythymio2.tg(Thym)

        if cnt > 200:
            pythymio2.arrete(Thym)
            Thym.stop()

        if evt_name == 'fwd.prox' and time.time() > temps + 0.1:
            temps = time.time()
            print(evt_name,evt_args)

    # Now lets start the loopy thing
    Thym.loop(dispatch)
    print "Sayonara"

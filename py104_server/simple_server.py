#!/usr/bin/env python
# coding: utf-8
# info
__version__ = "0.1"

'''
Free and open implementation of the IEC 60870-5 104 protocol
'''

import signal, time
import iec104

running = True
scaledValue = 0

def sigint_handler(signalNumber, frame):
    global running
    running = False

def main():
    global scaledValue

    signal.signal(signal.SIGINT, sigint_handler)

    slave = iec104.CS104_Slave_create(10, 10)

    iec104.CS104_Slave_setLocalAddress(slave, "0.0.0.0")

    iec104.CS104_Slave_setServerMode(slave, iec104.CS104_MODE_SINGLE_REDUNDANCY_GROUP)

    alParams = iec104.CS104_Slave_getAppLayerParameters(slave)

    apciParams = iec104.CS104_Slave_getConnectionParameters(slave)

    print("APCI parameters:\n")
    print("  t0:%s\n" %  apciParams.t0)
    print("  t1:%s\n" %  apciParams.t1)
    print("  t2:%s\n" %  apciParams.t2)
    print("  t3:%s\n" %  apciParams.t3)
    print("  k:%s\n" %  apciParams.k)
    print("  w:%s\n" %  apciParams.w)

    # create and set the callback handler for the clock synchronization command
    clockSyncHandler = iec104.clockSyncHandler_create()
    iec104.CS104_Slave_setClockSyncHandler(slave, clockSyncHandler, None)

    # set the callback handler for the interrogation command
    interrogationHandler = iec104.interrogationHandler_create()
    iec104.CS104_Slave_setInterrogationHandler(slave, interrogationHandler, None)

    # set handler for other message types
    asduHandler = iec104.asduHandler_create()
    iec104.CS104_Slave_setASDUHandler(slave, asduHandler, None)

    # set handler to handle connection requests (optional)
    connectionRequestHandler = iec104.connectionRequestHandler_create()
    iec104.CS104_Slave_setConnectionRequestHandler(slave, connectionRequestHandler, None)

    # set handler to track connection events (optional)
    connectionEventHandler = iec104.connectionEventHandler_create()
    iec104.CS104_Slave_setConnectionEventHandler(slave, connectionEventHandler, None)   

    iec104.CS104_Slave_start(slave)

    if (iec104.CS104_Slave_isRunning(slave) == False):
        print("Starting server failed!\n")
    else:
        print("Server started successfully!\n")
    
    while(running):
        time.sleep(10)

        newAsdu = iec104.CS101_ASDU_create(alParams, False, iec104.CS101_COT_PERIODIC, 0, 1, False, False)

        io = iec104.InformationObject_create(110, scaledValue)

        scaledValue += 1

        iec104.CS101_ASDU_addInformationObject(newAsdu, io)

        iec104.InformationObject_destroy(io)

        iec104.CS104_Slave_enqueueASDU(slave, newAsdu)

        iec104.CS101_ASDU_destroy(newAsdu)
    
    iec104.CS104_Slave_stop(slave)
    iec104.CS104_Slave_destroy(slave)
    quit()

if __name__ == '__main__':
    main()
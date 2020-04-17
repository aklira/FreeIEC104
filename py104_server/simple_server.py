#!/usr/bin/env python
# coding: utf-8
# info
__version__ = "0.1"

'''
Free and open implementation of the IEC 60870-5 104 protocol
'''

import signal
import iec104

running = True 

def sigint_handler():
    global running
    running = False

def main():

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

if __name__ == '__main__':
    main()
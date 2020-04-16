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
    running = False

# Callback handler to log sent or received messages (optional)
def rawMessageHandler(parameter, connection, msg, sent):
    if (sent):
        print("SEND: ")
    else:
        print("RCVD: ")

    for item in msg:
        print(item)

    print("\n")

# Callback handler for the clock synchronization command
def clockSyncHandler(parameter, connection, asdu, newTime):
    #printf("Process time sync command with time "); printCP56Time2a(newTime); printf("\n");

    newSystemTimeInMs = iec104.CP56Time2a_toMsTimestamp(newTime)

    #Set time for ACT_CON message
    iec104.CP56Time2a_setFromMsTimestamp(newTime, iec104.Hal_getTimeInMs())

    # update system time here

    return True


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

if __name__ == '__main__':
    main()
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

def sigint_handler(signalNumber, frame):
    global running
    running = False

def main():
    ip = "localhost"
    port = iec104.IEC_60870_5_104_DEFAULT_PORT

    signal.signal(signal.SIGINT, sigint_handler)

    print("Connecting to: %s on port: %s" %  (ip, port))

    con = iec104.CS104_Connection_create(ip, port)

    connectionHandler = iec104.connectionHandler_create()
    iec104.CS104_Connection_setConnectionHandler(con, connectionHandler, None)

    asduReceivedHandler = iec104.asduReceivedHandler_create()
    iec104.CS104_Connection_setASDUReceivedHandler(con, asduReceivedHandler, None)

    while(running):
        if (iec104.CS104_Connection_connect(con)):
            print("Connection established!\n")

            iec104.CS104_Connection_sendStartDT(con)

            #time.sleep(2)

            #iec104.CS104_Connection_sendInterrogationCommand(con, iec104.CS101_COT_ACTIVATION, 1, iec104.IEC60870_QOI_STATION)

            #time.sleep(5)

            #testTimestamp = iec104.CP56Time2a_Timestamp_create()

            #iec104.CS104_Connection_sendTestCommandWithTimestamp(con, 1, 0x4938, testTimestamp)

            print("Wait ...\n")
            time.sleep(1)
        else:
            print("Connection failed!\n")
            time.sleep(1)

            iec104.CS104_Connection_destroy(con)

            print("exit\n")
            quit()
        
    iec104.CS104_Connection_sendStopDT(con)
    iec104.CS104_Connection_destroy(con)

    print("exit\n")
    quit()

if __name__ == '__main__':
    main()
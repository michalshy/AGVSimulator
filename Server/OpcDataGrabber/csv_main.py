
import time

from Threads.FlagThread import FlagThread
from OpcDataGrabber import OPCDataGrabber
from datetime import datetime
from threading import Timer



def main():
    finishFlag = False
    url = "opc.tcp://localhost:4841/freeopcua/server/"
    opcclient = OPCDataGrabber()
    opcclient.SetTimeInterval()
    opcData = ""

    thread = FlagThread()
    thread.start()
    print(opcclient.timeInterval)

    while not finishFlag:
        t = Timer(opcclient.timeInterval, opcclient.ReceiveDataFromServer)

        t.start()
        print(opcclient.dataReceived)


        finishFlag = thread.value
        print(finishFlag)
        t.join()


    opcData += opcclient.dataReceived

    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    filename = "../Data/" + current_time + ".csv"


    f = open(filename, "w")
    f.write(opcData)
    opcclient.CloseConnection()









if __name__ == "__main__":
    main()
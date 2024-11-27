import time

from OpcDataGrabber import OPCDataGrabber
from datetime import datetime


def main():
    finishFlag = False
    opcclient = OPCDataGrabber()
    opcclient.SetTimeInterval()

    print(opcclient.timeInterval)

    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")

    filename = "../Data/" + current_time + ".csv"

    while not finishFlag:
        opcclient.ReceiveDataFromServer()

        print(opcclient.dataReceived)

        f = open(filename, "w")
        f.write(opcclient.dataReceived)

        time.sleep(opcclient.timeInterval)

        if opcclient.client == None:

            opcclient.CloseConnection
            finishFlag = True

    # opcclient.CloseConnection()


if __name__ == "__main__":
    main()
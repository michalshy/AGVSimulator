import time

from OpcDataGrabber import OPCDataGrabber
from datetime import datetime


def main():
    finishFlag = False
    opcclient = OPCDataGrabber()
    print("1")
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
        print("2")

        time.sleep(opcclient.timeInterval)

        if opcclient.client == None:
            print("3")

            opcclient.CloseConnection
            finishFlag = True

    # opcclient.CloseConnection()


if __name__ == "__main__":
    main()
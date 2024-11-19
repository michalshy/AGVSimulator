from threading import Thread

class FlagThread(Thread):
    def __init__(self):
        super().__init__()
        self.value = False

    def run(self):
        userInput = input("")
        if userInput.lower() == "q":
            self.value = True
from DataManager import DataManager
from AIManager import AI_Manager

import sys

if __name__ == "__main__":

    path = str(sys.argv[1])  # Save path to file with data to train model
    steps = int(sys.argv[2])  # Save amount of previous steps to train LSTM

    dataManager = DataManager(path)  # Initialize DataManager class object with path to file with data
    aiManager = AI_Manager(steps)    # Initialize AiManager class object with amount of last steps for LSTM

    data = dataManager._divided_data[-1]

    size = int(len(data) * 0.8)
    train_data = data[:size] 
    validation_data = data[size:]

    aiManager.preprocess_data(train_data, validation_data)
    aiManager.train_model()

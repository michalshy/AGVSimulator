from DataManager import DataManager
from AIManager import AI_Manager

import sys

if __name__ == "__main__":
    # Check if the correct number of arguments is passed
    if len(sys.argv) != 3:
        print("Error: Exactly two arguments required - <path_to_file> <number_of_steps>")
        sys.exit(1)

    # Validate that the first argument is a string and the second argument is a number
    try:
        path = str(sys.argv[1])  # Save path to file with data to train model
        
        # Ensure the second argument is an integer
        steps = int(sys.argv[2])
        if steps <= 0:
            raise ValueError("Number of steps must be a positive integer.")
        
    except ValueError as e:
        print(f"Error: Invalid argument - {e}")
        sys.exit(1)

    # Initialize DataManager and AI_Manager after validation
    dataManager = DataManager(path)  # Initialize DataManager class object with path to file with data
    aiManager = AI_Manager(steps)    # Initialize AI_Manager class object with amount of last steps for LSTM

    # Access data to train the model
    data = dataManager._fullData

    # Train battery predicting model
    aiManager.train_battery_model(data)

    # Split data into train and validation set for position predict model
    size = int(len(data) * 0.8)
    train_data = data[:size] 
    validation_data = data[size:]

    # Train model for postition prediction
    aiManager.preprocess_data(train_data, validation_data)
    aiManager.train_model()

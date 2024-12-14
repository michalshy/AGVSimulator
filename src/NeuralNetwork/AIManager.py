import os

# Disable oneDNN optimizations for TensorFlow for compatibility
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pandas as pd
import numpy as np
import joblib
import json 

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import load_model, Model, Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout

class AI_Manager:

    _scaler_X : MinMaxScaler # Scaler for input features
    _scaler_y : MinMaxScaler # Scaler for output features
    _segment_boundaries : {} # Dictionary with start and end points for each segment

    # Initialize AI_Manager and set up number of time steps for LSTM input sequences
    def __init__(self, steps: int,):
        self._n_steps = steps
        self.load_segment_boundaries() # Load segment boundaries from a file

    # Validate that all segments in the input DataFrame were present during training, warn if there are any unknown segments    
    def validate_segments(self, df):
        # Retrieve known segments from the encoder
        known_segments = set(self.segment_encoder.categories_[0])
        # Find unique segments in the input data
        prediction_segments = set(df['Current segment'].unique())

        # Identify unknown segments
        unknown_segments = prediction_segments - known_segments
        if unknown_segments:
            print(f"Warning: The following segments were not seen during training and will be ignored: {unknown_segments}")

    #Preprocess training and validation data for model training
    def preprocess_data(self, train_df, val_df):
        # Columns to use as input and output
        input_columns = ['X-coordinate', 'Y-coordinate', 'Heading', 'Current segment']
        output_columns = ['X-coordinate', 'Y-coordinate', 'Heading']

        # Separate inputs and targets for training and validation
        X_train = train_df[input_columns].values
        y_train = train_df[output_columns].values
        X_val = val_df[input_columns].values
        y_val = val_df[output_columns].values

        # Initialize and fit scalers for numerical features
        self._scaler_X = MinMaxScaler()  # Scaler for input features
        self._scaler_y = MinMaxScaler()  # Scaler for output targets

        # One-hot encode 'Current segment' with handling for unknown categories
        self.segment_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')  # Enable handling unknown categories
        segment_train = train_df[['Current segment']]
        segment_val = val_df[['Current segment']]

        # Fit and transform the encoder
        segment_train_encoded = self.segment_encoder.fit_transform(segment_train)
        segment_val_encoded = self.segment_encoder.transform(segment_val)

        # Scale the other features
        other_train_features = train_df[['X-coordinate', 'Y-coordinate', 'Heading']]
        other_val_features = val_df[['X-coordinate', 'Y-coordinate', 'Heading']]

        self._scaler_X = MinMaxScaler()
        X_train_scaled = self._scaler_X.fit_transform(other_train_features)
        X_val_scaled = self._scaler_X.transform(other_val_features)

        # Combine scaled features with one-hot encoded segment data
        X_train = np.hstack([X_train_scaled, segment_train_encoded])
        X_val = np.hstack([X_val_scaled, segment_val_encoded])

        # Scale output targets
        self._scaler_y = MinMaxScaler()
        y_train = self._scaler_y.fit_transform(train_df[output_columns])
        y_val = self._scaler_y.transform(val_df[output_columns])

        # Create sequences of data for LSTM input
        def create_sequences(data, target, seq_length):
            X_seq, y_seq = [], []
            for i in range(len(data) - seq_length):
                X_seq.append(data[i:i + seq_length])
                y_seq.append(target[i + seq_length])
            return np.array(X_seq), np.array(y_seq)

        self.X_train_seq, self.y_train_seq = create_sequences(X_train, y_train, self._n_steps)
        self.X_val_seq, self.y_val_seq = create_sequences(X_val, y_val, self._n_steps)

        # Save the OneHotEncoder and scalers
        joblib.dump(self.segment_encoder, 'Config/AI/segment_encoder.pkl') 
        joblib.dump(self._scaler_X, 'Config/AI/scaler_X.pkl')
        joblib.dump(self._scaler_y, 'Config/AI/scaler_y.pkl')

    def train_model(self):
        # Input layer
        input_main = Input(shape=(self._n_steps, self.X_train_seq.shape[2]))

        # LSTM layers
        lstm_out = LSTM(64, return_sequences=True)(input_main)
        lstm_out = Dropout(0.2)(lstm_out)
        lstm_out = LSTM(32, return_sequences=False)(lstm_out)

        # Dense layers
        dense_out = Dense(32, activation='relu')(lstm_out)
        dense_out = Dense(64, activation='sigmoid')(dense_out)

        # Output layer
        output_main = Dense(3)(dense_out)

        # Define the model using Model class
        model = Model(inputs=input_main, outputs=output_main)

        # Compile the model
        model.compile(optimizer='adam', loss='mae', metrics=['mae'])

        # Early stopping
        early_stopping = EarlyStopping(monitor='val_loss', patience=7, restore_best_weights=True)

        # Train the model
        model.fit(
            self.X_train_seq, self.y_train_seq,
            validation_data=(self.X_val_seq, self.y_val_seq),
            epochs=250, batch_size=32, callbacks=[early_stopping], verbose=1
        )

        # Save the trained model
        model.save('Config/AI/model.keras')

    def train_battery_model(self, data):

        data = data[['Battery cell voltage']]

        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)

        # Create sequences of 20 timesteps
        X, y = [], []
        for i in range(len(scaled_data) - self._n_steps):
            X.append(scaled_data[i:i + self._n_steps, 0])
            y.append(scaled_data[i + self._n_steps, 0])

        X = np.array(X)
        y = np.array(y)

        # Reshape X for LSTM (samples, timesteps, features)
        X = X.reshape((X.shape[0], X.shape[1], 1))

        # Create the LSTM model
        model = Sequential([
            LSTM(16, input_shape=(X.shape[1], 1)),
            Dense(16, activation='relu'),
            Dense(1)  # Single output for the next voltage value
        ])

        # Compile the model
        model.compile(optimizer='adam', loss='mse')

        # Train the model
        model.fit(X, y, epochs=12, batch_size=32, validation_split=0.2)

        # Save the model
        model.save('Config/AI/battery_model.keras')

        # Save the scaler
        joblib.dump(scaler, 'Config/AI/scaler_battery.pkl')

    # Predict a route based on initial input data and a trained LSTM model
    def predict_route(self, df, tms_data):
        # Change ordinary array to pandas dataframe
        df = pd.DataFrame(df)

        # Load previously saved scalers, encoder and trained model
        self._scaler_X = joblib.load('Config/AI/scaler_X.pkl')
        self._scaler_y = joblib.load('Config/AI/scaler_y.pkl')
        self.segment_encoder = joblib.load('Config/AI/segment_encoder.pkl')
        model = load_model('Config/AI/model.keras')

        battery_scaler = joblib.load('Config/AI/scaler_battery.pkl')
        battery_model = load_model('Config/AI/battery_model.keras')
        
        # Initialize the input DataFrame with the last `n_steps`
        df = df[-self._n_steps:].copy()
        predictions = [] # Store all predictions

        for idx, curr_segment in enumerate(tms_data):
            # Extract boundaries for the current segment
            boundaries = self._segment_boundaries[str(curr_segment)]
            end_coords = boundaries['end_coordinates']
            
            # Variables to track consecutive predictions moving away from endpoint
            previous_distance_to_end = None
            consecutive_moving_away = 0

            while True:
                # Prepare the latest input data
                data = df[-self._n_steps:].copy()
                segment_data = self.segment_encoder.transform(data[['Current segment']])  # One-hot encode segment
                scaled_features = self._scaler_X.transform(data[['X-coordinate', 'Y-coordinate', 'Heading']])
                scaled_battery = battery_scaler.transform(data[['Battery cell voltage']])
                
                # Concatenate scaled features with one-hot-encoded segment
                full_features = np.hstack([scaled_features, segment_data])
                input_data = np.expand_dims(full_features, axis=0)  # Add batch dimension
                battery_input_data = np.expand_dims('Battery cell voltage', axis=0)

                # Predict the next step
                predicted_scaled = model.predict(input_data)
                predicted_original = self._scaler_y.inverse_transform(predicted_scaled)

                predicted_battery = battery_model.predict(battery_input_data)
                predicted_original_battery = battery_scaler.inverse_transform(predicted_battery)

                # Create a prediction DataFrame
                result_df = pd.DataFrame(predicted_original, columns=['X-coordinate', 'Y-coordinate', 'Heading'])
                result_df['Current segment'] = curr_segment
                result_df['Battery cell voltage'] = predicted_original_battery

                # Append the prediction to the sequence and update input data
                predictions.append(result_df)
                df = pd.concat([df, result_df], ignore_index=True)

                # Analyze the predicted point
                predicted_point = result_df.iloc[-1][['X-coordinate', 'Y-coordinate']].values
                distance_to_end = np.linalg.norm(predicted_point - end_coords)
                print(f"Predicted point: {predicted_point}, Distance to endpoint: {distance_to_end:.4f}")

                # Check if the predicted point is close enough to the segment's endpoint
                if distance_to_end <= 0.3:
                    print(f"Reached the endpoint of Segment {curr_segment}. Moving to next segment.")
                    break

                # Check if the predicted point is moving away from the endpoint
                if previous_distance_to_end is not None:
                    if distance_to_end > previous_distance_to_end or round(distance_to_end, 4) == round(previous_distance_to_end, 4):
                        consecutive_moving_away += 1
                        print(f"Point is moving away from endpoint. Count: {consecutive_moving_away}")
                      
                    else:
                        consecutive_moving_away = 0  # Reset if moving closer

                # Update previous distance
                previous_distance_to_end = distance_to_end

                # Switch segment if moving away for 2 consecutive points
                if consecutive_moving_away >= 2:
                    print(f"Switching to the next segment due to consecutive moving-away points.")
                    break

        # Combine all predictions into a single DataFrame
        predicted_df = pd.concat(predictions, ignore_index=True)
        return predicted_df.values.tolist()

    # Load segment boundaries from file
    def load_segment_boundaries(self):
        try:
            with open('Config/AI/segment_boundaries.txt', 'r') as file:
                segment_boundaries = json.load(file)
            print(f"Segment boundaries successfully read from {'Config/AI/segment_boundaries.txt'}")
            self._segment_boundaries = segment_boundaries # Store segment boundaries
        except Exception as e:
            print(f"Error reading segment boundaries from file: {e}")
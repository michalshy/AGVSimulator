import os

# Disable oneDNN optimizations for TensorFlow for compatibility
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pandas as pd
import numpy as np
import joblib
import json 

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout

import pandas as pd
import time
import threading



# -*- coding: utf-8 -*-
"""Dec module

Deep learning class module, contains method which makes prediction of path possible.
Navigator module within AGV uses it to checks next points on route based on order.
"""

PATH = []
PATH_MUTEX = threading.Lock()

class Dec:
    def __init__(self) -> None:
        self._ai = AI_Manager(20)
        self._path = []
        self._segments = []
        self._finished = True
        self._started = False

    def Start(self):
        self._finished = False
        self._started = True

    def SetSegments(self, segments, initial_data):
        self._initial_data = initial_data
        self._segments = segments
        self._ai.SetParams(self._segments, self._initial_data)

    def PredictPath(self):
        self._ai.predict_route(self._segments)
        # ------------------------------ CRITICAL SECTION ------------------------------
        global PATH_MUTEX
        PATH_MUTEX.acquire()
        length = 0
        try:
            length = len(PATH)
        finally:
            PATH_MUTEX.release()
        # --------------------------- END OF CRITICAL SECTION ---------------------------
        self._finished = True
        self._started = False

    def GetInPrediction(self):
        return (not self._finished) and self._started 

    def ReturnPredictedPath(self):
        # ------------------------------ CRITICAL SECTION ------------------------------
        global PATH_MUTEX
        PATH_MUTEX.acquire()
        try:
            self._path = PATH
        finally:
            PATH_MUTEX.release()
        # --------------------------- END OF CRITICAL SECTION ---------------------------
        return self._path
    
class AI_Manager:

    _scaler_X : MinMaxScaler # Scaler for input features
    _scaler_y : MinMaxScaler # Scaler for output features
    _segment_boundaries : {} # Dictionary with start and end points for each segment

    def __init__(self, steps: int):
        self._scaler_X = joblib.load('Config/AI/scaler_X.pkl')
        self._scaler_y = joblib.load('Config/AI/scaler_y.pkl')
        self._segment_encoder = joblib.load('Config/AI/segment_encoder.pkl')
        self._model = load_model('Config/AI/model.keras')
        self._n_steps = steps
        self.load_segment_boundaries() # Load segment boundaries from a file
        self._initial_data = []
        self._segments = []

    def SetParams(self, segments, initial):
        self._initial_data = initial
        self._segments = segments

    # Predict a route based on initial input data and a trained LSTM model
    def predict_route(self, tms_data):
        # Change ordinary array to pandas dataframe
        df = pd.DataFrame(self._initial_data)
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
                segment_data = self._segment_encoder.transform(data[['Current segment']])  # One-hot encode segment
                scaled_features = self._scaler_X.transform(data[['X-coordinate', 'Y-coordinate', 'Heading']])
                
                # Concatenate scaled features with one-hot-encoded segment
                full_features = np.hstack([scaled_features, segment_data])
                input_data = np.expand_dims(full_features, axis=0)  # Add batch dimension

                # Predict the next step
                predicted_scaled = self._model.predict(input_data)
                predicted_original = self._scaler_y.inverse_transform(predicted_scaled)

                # Create a prediction DataFrame
                result_df = pd.DataFrame(predicted_original, columns=['X-coordinate', 'Y-coordinate', 'Heading'])

                # ------------------------------ CRITICAL SECTION ------------------------------
                global PATH_MUTEX
                PATH_MUTEX.acquire()
                try:
                    PATH.append(result_df.values.tolist()[0])
                finally:
                    PATH_MUTEX.release()
                # --------------------------- END OF CRITICAL SECTION ---------------------------

                result_df['Current segment'] = curr_segment

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

    # Load segment boundaries from file
    def load_segment_boundaries(self):
        try:
            with open('Config/AI/segment_boundaries.txt', 'r') as file:
                segment_boundaries = json.load(file)
            print(f"Segment boundaries successfully read from {'Config/AI/segment_boundaries.txt'}")
            self._segment_boundaries = segment_boundaries # Store segment boundaries
        except Exception as e:
            print(f"Error reading segment boundaries from file: {e}")
    
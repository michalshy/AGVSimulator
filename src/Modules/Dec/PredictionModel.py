import pandas as pd
import numpy as np
import joblib
import json 
from tensorflow.keras.models import load_model
from Modules.Dec.PathSingleton import PathSingleton
import time

class PredicitonModel:
    def __init__(self):
        pass

    # Predict a route based on initial input data and a trained LSTM model
    def predict_route(self, conn):


        while True:
            if conn.poll():
                msg = conn.recv()
                if msg[0] == 'predict':
                    try:
                        with open('Config/AI/segment_boundaries.txt', 'r') as file:
                            _segment_boundaries = json.load(file)
                    except Exception as e:
                        pass
                    
                    _initial_data = pd.DataFrame(msg[1])
                    _n_steps = msg[2]
                    tms_data = msg[3]
                    _scaler_X = joblib.load('Config/AI/scaler_X.pkl')
                    _scaler_y = joblib.load('Config/AI/scaler_y.pkl')
                    _segment_encoder = joblib.load('Config/AI/segment_encoder.pkl')
                    _model = load_model('Config/AI/model.keras')
                    battery_scaler = joblib.load('Config/AI/scaler_battery.pkl')
                    battery_model = load_model('Config/AI/battery_model.keras')

                    

                    
                    # Change ordinary array to pandas dataframe
                    df = _initial_data
                    # Initialize the input DataFrame with the last `n_steps`
                    df = df[-_n_steps:].copy()
                    
                    exitThread = False

                    # Find the last segment in `df`'s 'Current segment' column
                    last_segment_in_df = df['Current segment'].iloc[-1] 
                    if last_segment_in_df in tms_data: 
                        try:
                            start_idx = tms_data.index(last_segment_in_df) # Find its index in tms_data
                        except ValueError:
                            print(f"Error: Segment '{last_segment_in_df}' not found in tms_data.")
                            return
                        for curr_segment in tms_data[start_idx:]:
                            if exitThread:
                                continue
                            # Extract boundaries for the current segment
                            boundaries = _segment_boundaries[str(curr_segment)]
                            end_coords = boundaries['end_coordinates']
                            # Variables to track consecutive predictions moving away from endpoint
                            previous_distance_to_end = None
                            consecutive_moving_away = 0


                            while not exitThread:
                                # Prepare the latest input data
                                data = df[-_n_steps:].copy()
                                self._initial_data = data
                                segment_data = _segment_encoder.transform(data[['Current segment']])  # One-hot encode segment
                                scaled_features = _scaler_X.transform(data[['X-coordinate', 'Y-coordinate', 'Heading']])
                                battery_scaled = battery_scaler.transform(data[['Battery cell voltage']])
                                # Concatenate scaled features with one-hot-encoded segment
                                full_features = np.hstack([scaled_features, segment_data])
                                input_data = np.expand_dims(full_features, axis=0)  # Add batch dimension
                                battery_input_data = np.expand_dims(battery_scaled, axis=0)
                                # Predict the next step
                                try:
                                    predicted_scaled = _model.predict(input_data, verbose = 0)
                                    predicted_scaled_battery = battery_model.predict(battery_input_data, verbose=0)
                                    predicted_original = _scaler_y.inverse_transform(predicted_scaled)
                                    predicted_original_battery = battery_scaler.inverse_transform(predicted_scaled_battery)
                                    # Create a prediction DataFrame
                                    result_df = pd.DataFrame(predicted_original, columns=['X-coordinate', 'Y-coordinate', 'Heading'])
                                    result_df['Battery cell voltage'] = predicted_original_battery[0]
                                    # ------------------------------ CRITICAL SECTION ------------------------------
                                    conn.send([result_df.values.tolist()[0], df.to_dict()])
                                    # --------------------------- END OF CRITICAL SECTION ---------------------------
                                    result_df['Current segment'] = curr_segment
                                    df = pd.concat([df, result_df], ignore_index=True)
                                    # Analyze the predicted point
                                    predicted_point = result_df.iloc[-1][['X-coordinate', 'Y-coordinate']].values
                                    distance_to_end = np.linalg.norm(predicted_point - end_coords)
                                    # Check if the predicted point is close enough to the segment's endpoint
                                    if distance_to_end <= 0.3:
                                        break
                                    # Check if the predicted point is moving away from the endpoint
                                    if previous_distance_to_end is not None:
                                        if distance_to_end > previous_distance_to_end or round(distance_to_end, 4) == round(previous_distance_to_end, 4):
                                            consecutive_moving_away += 1
                                        else:
                                            consecutive_moving_away = 0  # Reset if moving closer
                                    # Update previous distance
                                    previous_distance_to_end = distance_to_end
                                    # Switch segment if moving away for 2 consecutive points
                                    if consecutive_moving_away >= 2:
                                        break
                                except RuntimeError as Err:
                                    self._initial_data = data
                                    exitThread = True
                                except ValueError as Err:
                                    self._initial_data = data
                                    exitThread = True
                    conn.send("END")
                elif msg[0] == 'stop':
                    break
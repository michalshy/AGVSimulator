import pandas as pd
import numpy as np
import json 

# Custom DataFrame class to add segment-specific filtering functionality
class SegmentDataFrame(pd.DataFrame):
    # Override the __getitem__ method to allow custom access logic
    def __getitem__(self, key):
        if isinstance(key, str) and key.isdigit():
            # If the key is a string that represents a number, filter rows based on 'Current segment'
            segment_id = float(key)  # Convert key to a float (matches 'Current segment' type)
            return self[self['Current segment'] == segment_id]
        else:
           # Use the default pandas behavior for other keys
            return super().__getitem__(key)
        
# Main class for handling and processing the data
class DataManager:
    _dataFileName: str # Filename of the input CSV file
    _fullData = [] # The full dataset after loading and cleaning
    _allSegments = [] # Unique segment identifiers in the dataset
    _divided_data = [] # List of segments divided by "jumps" (discontinuous segments)
    _segment_boundaries = {}  # Dictionary of segment start and end boundaries

    # Constructor: Initializes the object and sets up the data
    def __init__(self, dataFile: str):
        self._dataFileName = dataFile  # Store the file name
        self.setUp() # Set up the data by performing initial processing

    def setUp(self):
        self.read_data_from_csv() # Load and clean the data from the CSV file
        self.get_segment_boundaries() # Identify start and end points for each segment
        self.find_jumps(3) # Divide data into segments based on a distance threshold
        self._fullData.drop(columns=['Timestamp'],inplace=True)  # Drop the 'Timestamp' column
        self._divided_data = sorted(self._divided_data, key=len) # Sort chunks by their lengths

    # Load data from a CSV file and perform initial cleaning 
    def read_data_from_csv(self):
        # Read the CSV file into a DataFrame
        data = pd.read_csv(self._dataFileName, low_memory=False)

        # Select only relevant columns and coerce invalid data to NaN
        data = data[['Timestamp', 'X-coordinate', 'Y-coordinate', 'Heading', 'Current segment','Going to ID']]
        data['X-coordinate'] = pd.to_numeric(data['X-coordinate'], errors='coerce')
        data['Y-coordinate'] = pd.to_numeric(data['Y-coordinate'], errors='coerce')
        data['Heading'] = pd.to_numeric(data['Heading'], errors='coerce')
        data['Going to ID'] = pd.to_numeric(data['Going to ID'], errors='coerce')
        data['Current segment'] = pd.to_numeric(data['Current segment'], errors='coerce')

        # Remove rows with any NaN values
        data = data.dropna()

        # Store the cleaned data in a SegmentDataFrame for custom filtering
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        
        # Return data as a SegmentDataFrame instead of a regular DataFrame
        self._fullData = SegmentDataFrame(data)

    # Divide the dataset into segments based on large "jumps" in coordinates
    def find_jumps(self, threshold):
        segments = [] # List to hold identified segments
        last_index = 0  # Initialize the start index for the first segment
        
        # Iterate through the dataset to calculate distances between consecutive points
        for i in range(1, len(self._fullData)):
            # Extract coordinates of consecutive points
            x1, y1 = self._fullData.iloc[i-1][['X-coordinate', 'Y-coordinate']]
            x2, y2 = self._fullData.iloc[i][['X-coordinate', 'Y-coordinate']]
            
            # Calculate the Euclidean distance between the points
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            if distance > threshold: # Check if the distance exceeds the threshold
                # Create a segment from the last_index to the current point
                segments.append(self._fullData.iloc[last_index:i])
                last_index = i  # Update the starting index for the next segment
        
       # Append the final segment after the last jump
        if last_index < len(self._fullData):
            segments.append(self._fullData.iloc[last_index:])
        
        # Store the divided segments
        self._divided_data = segments

    # Determine the boundaries (start and end points) for each segment
    def get_segment_boundaries(self):
        # Get a list of unique segment IDs
        segments = self._fullData['Current segment'].unique()
        self._allSegments = segments # Store the unique segments
        segment_boundaries = {} # Dictionary to hold the boundaries

        # Iterate through each segment ID
        for segment in segments:
            # Filter data rows corresponding to the current segment
            segment_data = self._fullData[self._fullData['Current segment'] == segment]

            # Extract the start and end coordinates for the segment
            start_index = segment_data.index[0]
            end_index = segment_data.index[-1]
            start_point = segment_data.loc[start_index, ['X-coordinate', 'Y-coordinate']].tolist()
            end_point = segment_data.loc[end_index, ['X-coordinate', 'Y-coordinate']].tolist()

            # Store the start and end coordinates in the dictionary
            segment_boundaries[segment] = {
                'start_coordinates': start_point,
                'end_coordinates': end_point
            }

        # Save the segment boundaries
        self._segment_boundaries =  segment_boundaries
        self.save_segment_boundaries()

    # Save segment boundaries into a .txt file
    def save_segment_boundaries(self):
        try:
            with open('Config/segment_boundaries.txt', 'w') as file: 
                json.dump(self._segment_boundaries, file, indent=4)
            print(f"Segment boundaries successfully written to {'Config/segment_boundaries.txt'}")
        except Exception as e:
            print(f"Error writing segment boundaries to file: {e}")
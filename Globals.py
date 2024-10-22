#SCREEN
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

#AGV
AGV_SIZE = 10
AGV_TURN_TOLERANCE = 15

#NAVIGATION
GRID_DENSITY = 5
GRID_OFFSET_AMOUNT = int(AGV_SIZE/GRID_DENSITY) + 5
# 0 - Machine Learning navigation provided by LSTM Neural Network
# 1 - A* navigation, harcoded algorithm
NAV_TYPE = 0

#ROOM
ROOM_WIDTH = 1000
ROOM_HEIGHT = 600
ROOM_W_OFFSET = (SCREEN_WIDTH - ROOM_WIDTH)/2
ROOM_H_OFFSET = (SCREEN_HEIGHT- ROOM_HEIGHT)/2
STARTING_POS_X = 39.78110885620117
STARTING_POS_Y = 14.963831901550293

#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

#PHYSICS
ROTATE_VAL = 100
import sys
import pygame
from pygame import Surface
from Globals import *
import math
import heapq

BLACK = (0,0,0)
WHITE = (255,255,255)

# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination

class Navigator:
    def __init__(self) -> None:
        self._image: Surface = None
        self._grid: list = []
        self._rows = 0
        self._cols = 0

    def Init(self, img: Surface):
        self._image = img
        self._grid = self.DetermineGrid()

    def DetermineGrid(self) -> list:
        column = AGV_SIZE
        row = AGV_SIZE
        columnsCalculated = False
        while row < self._image.get_height():
            column = AGV_SIZE
            while column < self._image.get_width():
                if self._image.get_at((column, row)) == WHITE:
                    self._grid.append(1)
                else:
                    self._grid.append(0)
                column += AGV_SIZE
                if not columnsCalculated:
                    self._cols += 1
            columnsCalculated = True
            row += AGV_SIZE
            self._rows += 1
        return self._grid
    def TransformPos(self, pos: tuple) -> tuple:
        return (round((pos[1] - (SCREEN_HEIGHT - self._image.get_height())/2)/AGV_SIZE, 0), 
                round((pos[0] - (SCREEN_WIDTH - self._image.get_width())/2)/AGV_SIZE, 0))

    def FindPath(self, agvPos: tuple, destPos: tuple):
        startPos = self.TransformPos(agvPos)
        resultStart = tuple(tuple(map(int, startPos)))
        goalPos = self.TransformPos(destPos)
        resultGoal = tuple(tuple(map(int, goalPos)))
        self.AStarSearch(resultStart, resultGoal)
        
    # Check if a cell is valid (within the grid)
    def IsValid(self, row, col):
        return (row >= 0) and (row < self._rows) and (col >= 0) and (col < self._cols)

    # Check if a cell is unblocked
    def IsUnblocked(self, row, col):
        return self._grid[(row * self._cols) + col] == 1

    # Check if a cell is the destination
    def IsDestination(self, row, col, dest):
        return row == dest[0] and col == dest[1]

    # Calculate the heuristic value of a cell (Euclidean distance to destination)
    def CalculateHValues(self, row, col, dest):
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

    # Trace the path from source to destination
    def TracePath(self, cell_details, dest):
        print("The Path is ")
        path = []
        row = dest[0]
        col = dest[1]

        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()

        # Print the path
        for i in path:
            print("->", i, end=" ")
            pygame.draw.rect(self._image, (255,0,0), pygame.Rect(i[1] * AGV_SIZE, i[0] * AGV_SIZE, AGV_SIZE,AGV_SIZE))
        print()

    # Implement the A* search algorithm
    def AStarSearch(self, src, dest):
        # Check if the source and destination are valid
        if not self.IsValid(src[0], src[1]) or not self.IsValid(dest[0], dest[1]):
            print("Source or destination is invalid")
            return

        # Check if the source and destination are unblocked
        if not self.IsUnblocked(src[0], src[1]) or not self.IsUnblocked(dest[0], dest[1]):
            print("Source or the destination is blocked")
            return

        # Check if we are already at the destination
        if self.IsDestination(src[0], src[1], dest):
            print("We are already at the destination")
            return

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self._cols)] for _ in range(self._rows)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(self._cols)] for _ in range(self._rows)]

        # Initialize the start cell details
        i = src[0]
        j = src[1]
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            i = p[1]
            j = p[2]
            closed_list[i][j] = True

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]

                # If the successor is valid, unblocked, and not visited
                if self.IsValid(new_i, new_j) and self.IsUnblocked(new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if self.IsDestination(new_i, new_j, dest):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        print("The destination cell is found")
                        # Trace and print the path from source to destination
                        self.TracePath(cell_details, dest)
                        found_dest = True
                        return
                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = self.CalculateHValues(new_i, new_j, dest)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j

        # If the destination is not found after visiting all cells
        if not found_dest:
            print("Failed to find the destination cell")

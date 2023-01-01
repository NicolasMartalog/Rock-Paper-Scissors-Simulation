"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List 
from itertools import combinations
from random import randint, random
from copy import deepcopy
import constants
from math import sin, cos, pi, sqrt, pow

class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    id: int = 0
    character: str = "def" 

    def __init__(self, location: Point, direction: Point, character: str, id: int):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction
        self.character = character
        self.id = id

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.
        
    def color(self) -> str:
        """Return the color representation of a cell."""
        if (self.character == "R"): 
            return "gray"
        elif (self.character == "P"): 
            return "white"
        else: 
            return "silver"

    def tick(self) -> None: 
        self.location = self.location.add(self.direction) 
    
    def collide(self, other: Cell) -> None: 

        cell_distance = sqrt(((other.location.x - self.location.x)*(other.location.x - self.location.x)) + ((other.location.y - self.location.y)*(other.location.y - self.location.y)))

        # Normal
        nx = (other.location.x - self.location.x) / cell_distance
        ny = (other.location.y - self.location.y) / cell_distance 

        # Tangent
        tx = -1*ny
        ty = nx

        # Dot Product Tangent
        dpTan1 = self.direction.x * tx + self.direction.y * ty
        dpTan2 = other.direction.x * tx + other.direction.y * ty 

        # Dot Product Normal
        dpNormal1 = self.direction.x * nx + self.direction.y * ny
        dpNormal2 = other.direction.x * nx + other.direction.y * ny 

        #Conservation of momentum in 1D
        m1 = (dpNormal1 * ((constants.CELL_RADIUS * 0.8) - (constants.CELL_RADIUS * 0.8)) + 2 * (constants.CELL_RADIUS * 0.8) * dpNormal2) / ((constants.CELL_RADIUS * 0.8) + (constants.CELL_RADIUS * 0.8))
        m2 = (dpNormal2  + 2.0 * (constants.CELL_RADIUS * 0.8) * dpNormal1) / ((constants.CELL_RADIUS * 0.8) + (constants.CELL_RADIUS * 0.8))

        self.direction.x = tx * dpTan1 + nx * m1
        self.direction.y = ty * dpTan1 + ny * m1
        other.direction.x = tx * dpTan2 + nx * m2
        other.direction.y = ty * dpTan2 + ny * m2 
 
        # Update this
        if (self.character == "R" and other.character == "P"): 
            self.character = "P"
        if (self.character == "P" and other.character == "R"): 
            other.character = "P"
        if (self.character == "P" and other.character == "S"): 
            self.character = "S"
        if (self.character == "S" and other.character == "P"): 
            other.character = "S"
        if (self.character == "S" and other.character == "R"): 
            self.character = "R"
        if (self.character == "R" and other.character == "S"): 
            other.character = "R"



class Model:
    """The state of the simulation."""

    population: List[Cell]
    collisions: List[List[Cell, Cell]]
    time: int = 0

    def __init__(self, cells: int, speed: float):
        """Initialize the cells with random locations and directions."""
        self.population = []
        self.collisions = [[]]
        count = 0
        for _ in range(0, cells): 
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            start_char = self.random_character()
            self.population.append(Cell(start_loc, start_dir, start_char, count)) 
            count+=1

    
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population: 
            cell.tick()
            self.enforce_bounds(cell)
            self.check_collision(cell)

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def random_character(self) -> str:
        """Generate a 'point' used as a directional vector."""
        random_int = randint(1, 3)
        if (random_int == 1): 
            return "R"
        elif (random_int == 2): 
            return "P"
        else: 
            return "S"

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X: 
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1 


    def check_collision(self, cell: Cell) -> None:
        for cell1 in self.population: 
            if (cell.id != cell1.id): 
                calc = sqrt(((cell.location.x) - (cell1.location.x)) ** 2 + (cell.location.y - cell1.location.y) ** 2)
                if (calc <= constants.CELL_RADIUS):  

                    cell.collide(cell1)

                    fdistance = sqrt((cell.location.x - cell1.location.x)*(cell.location.x - cell1.location.x) + (cell.location.y - cell1.location.y)*(cell.location.y - cell1.location.y))
                    fOverlap = 0.5 * (fdistance - constants.CELL_RADIUS * 2) 

                    cell.location.x -= fOverlap * (cell.location.x - cell1.location.x) / fdistance
                    cell1.location.x += fOverlap * (cell.location.x - cell1.location.x) / fdistance 
                    cell.location.y -= fOverlap * (cell.location.y - cell1.location.y) / fdistance
                    cell1.location.y += fOverlap * (cell.location.x - cell1.location.x) / fdistance  


    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        return False
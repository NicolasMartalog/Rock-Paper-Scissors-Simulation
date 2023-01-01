from turtle import Turtle, Screen, done, Shape
from tkinter import PhotoImage
from model import Model
import constants
from typing import Any
from time import time_ns

NS_TO_MS: int = 1000000

class ViewController:
    """This class is responsible for controlling the simulation and visualizing it."""
    screen: Screen()
    pen: Turtle
    model: Model

    def __init__(self, model: Model):
        """Initialize the VC."""
        self.model = model
        self.screen = Screen()
        self.screen.setup(constants.VIEW_WIDTH, constants.VIEW_HEIGHT)
        self.screen.tracer(0, 0)
        self.screen.delay(0)
        self.screen.title("Rock vs Paper vs Scissor Battle Royale")
        self.pen = Turtle()
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.speed(0) 

        bigger_backround = PhotoImage(file="real.gif").zoom(2, 2)
        smaller_rock = PhotoImage(file="rock.gif").subsample(13, 13)
        smaller_scissor = PhotoImage(file="sciss.gif").subsample(50, 50)
        smaller_paper = PhotoImage(file="realpaper.gif").subsample(18, 18)
        self.screen.register_shape("smaller", Shape("image", smaller_rock)) 
        self.screen.register_shape("bigger", Shape("image", bigger_backround))
        self.screen.register_shape("smaller_scissor", Shape("image", smaller_scissor))
        self.screen.register_shape("smaller_paper", Shape("image", smaller_paper))
        self.screen.bgpic("output.gif") 

    def start_simulation(self) -> None:
        """Call the first tick of the simulation and begin turtle gfx."""
        self.tick()
        done() 

    def update_colour(self) -> None: 
        for cell in self.model.population:
            self.pen.color(cell.color())

    def tick(self) -> None:
        """Update the model state and redraw visualization."""
        start_time = time_ns() // NS_TO_MS
        self.model.tick()
        self.pen.clear()
        for cell in self.model.population:
            self.pen.penup()
            self.pen.goto(cell.location.x, cell.location.y)
            self.pen.pendown()
            self.pen.color(cell.color())  
            if (cell.color() == "gray"): 
                self.pen.shape("smaller")
            if (cell.color() == "white"): 
                self.pen.shape("smaller_paper")
            if (cell.color() == "silver"): 
                self.pen.shape("smaller_scissor")
            self.pen.stamp()
            #self.pen.dot(constants.CELL_RADIUS)
            

        self.screen.update()
        self.update_colour() 


        if self.model.is_complete():
            return
        else:
            end_time = time_ns() // NS_TO_MS
            next_tick = 30 - (end_time - start_time)
            if next_tick < 0:
                next_tick = 0
            self.screen.ontimer(self.tick, next_tick)
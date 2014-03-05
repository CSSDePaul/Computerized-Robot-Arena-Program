'''
Created on Feb 4, 2014

@author: excaliburhissheath
'''

from tkinter import *
from math import cos, sin, radians

class Graphics:
    '''
    A wrapper class to perform all graphical functions and run the main loop of the simulation.
    
    An object representing the board is provided, and a delay is given to 
    '''
    
    TILE_SIZE = 10;
    '''
    Size of tiles in the grid. Specifically, the length in pixels of the sides of the square tiles.
    '''
    
    TRIANGLE_POINTS = ((.577, 0), (-.289, -.5), (-.289, .5))
    '''
    Object coordinates for a scalene triangle with a circumcenter at the origin, pointing at the positive x direction.
    '''
    
    scaledTrianglePoints = [[0,0],[0,0],[0,0]]
    '''
    Scaled object coordinates for a scalene triangle with a circumcenter at the origin, pointing at the positive x direction.
    '''
    
    trianglePointsOffset = (.423, .5)
    '''
    Offset of the circumcenter of the triangle from the top left (least x and least y) corner of the tile it is in.
    The tip of the triangle is touching the positive x side of the tile on the right side.
    '''
    
    rotatedTrianglePoints = [[0,0],[0,0],[0,0]]
    ''' Points of the triangle rotated around the circumcenter. '''
    
    translatedTrianglePoints = [[0,0],[0,0],[0,0]]
    ''' Points of the triangle translated into world coordinates. '''
    
    tk_root = None
    ''' The root tkinter object. '''
    
    board = None
    ''' Object representing the current state of the game board. '''
    
    delay = 0
    ''' The interval between updates of the board (in miliseconds). '''

    robotGraphics = {}
    '''
    A dict of the id's of the robot graphics,
    indexed by the key for the corresponding robot object in board.robots .
    '''

    def __init__(self, board, delay=0):
        '''
        Constructor. It constructs stuff.
        '''
        
        
        # assign parameter values
        self.board = board;
        self.delay = delay;
        
        # initialize tk_root
        self.tk_root = Tk()
        
        self.canvas = Canvas(self.tk_root)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        
        # draw robots on canvas
        for key in self.board.robots:
            robot = self.board.robots[key]
            
            #scale the points of the triangle shape to the size of the tile
            for i in range(3):
                for j in range(2):
                    self.scaledTrianglePoints[i][j] = Graphics.TRIANGLE_POINTS[i][j] * Graphics.TILE_SIZE
            
            #rotate the points of the triangle shape to the correct orientation
            #currently by default the triangle is in the correct orientation
            #so this loop does nothing
            for i in range(3):
                self.rotatedTrianglePoints[i][0] = self.scaledTrianglePoints[i][0] * cos(radians(robot.rotation)) - self.scaledTrianglePoints[i][1] * sin(radians(robot.rotation))
                self.rotatedTrianglePoints[i][1] = self.scaledTrianglePoints[i][0] * sin(radians(robot.rotation)) + self.scaledTrianglePoints[i][1] * cos(radians(robot.rotation))
                
            #translate the points of the triangle    
            for i in range(3):
                self.translatedTrianglePoints[i][0] = self.rotatedTrianglePoints[i][0] + Graphics.TILE_SIZE * (self.trianglePointsOffset[0] + robot.xPosition)
                self.translatedTrianglePoints[i][1] = self.rotatedTrianglePoints[i][1] + Graphics.TILE_SIZE * (self.trianglePointsOffset[1] + robot.yPosition)
            
            self.robotGraphics[key] = self.canvas.create_polygon(self.translatedTrianglePoints[0][0],
                                                                 self.translatedTrianglePoints[0][1],
                                                                 self.translatedTrianglePoints[1][0],
                                                                 self.translatedTrianglePoints[1][1],
                                                                 self.translatedTrianglePoints[2][0],
                                                                 self.translatedTrianglePoints[2][1],
                                                                 fill="red",
                                                                 tags=('robot', key))
        
    def update(self):
        '''
        Updates the board, then redraws the board.

        Performs the logic for determining when the game ends.
        '''
        
        if (len(self.board.robots) <= 1):
            # if 1 or 0 robots left, end game

            # end tkinter loop
            self.tk_root.quit()

            # print winner
            print("A winner is " + list(self.board.robots.keys())[0])

            # exit
            return


        self.board.update();
        
        for key in self.board.robots:
            # redraw all robots
            robot = self.board.robots[key]
            robotid = self.robotGraphics[key]
            
            #scale the points of the triangle shape to the size of the tile
            for i in range(3):
                for j in range(2):
                    self.scaledTrianglePoints[i][j] = Graphics.TRIANGLE_POINTS[i][j] * Graphics.TILE_SIZE
            
            #rotate the points of the triangle shape to the correct orientation
            #currently by default the triangle is in the correct orientation
            #so this loop does nothing
            for i in range(3):
                self.rotatedTrianglePoints[i][0] = self.scaledTrianglePoints[i][0] * cos(radians(robot.rotation)) - self.scaledTrianglePoints[i][1] * sin(radians(robot.rotation))
                self.rotatedTrianglePoints[i][1] = self.scaledTrianglePoints[i][0] * sin(radians(robot.rotation)) + self.scaledTrianglePoints[i][1] * cos(radians(robot.rotation))
            
                
            #translate the points of the triangle    
            for i in range(3):
                self.translatedTrianglePoints[i][0] = self.rotatedTrianglePoints[i][0] + Graphics.TILE_SIZE * (self.trianglePointsOffset[0] + robot.xPosition)
                self.translatedTrianglePoints[i][1] = self.rotatedTrianglePoints[i][1] + Graphics.TILE_SIZE * (self.trianglePointsOffset[1] + robot.yPosition)
            
            self.canvas.coords(robotid, self.translatedTrianglePoints[0][0],
                                        self.translatedTrianglePoints[0][1],
                                        self.translatedTrianglePoints[1][0],
                                        self.translatedTrianglePoints[1][1],
                                        self.translatedTrianglePoints[2][0],
                                        self.translatedTrianglePoints[2][1])
                                         
        
        # reschedule update
        self.tk_root.after(self.delay, self.update)
        
    def start(self):
        '''
        Starts the tkinter's main loop and schedules the first update event.
        '''
        self.tk_root.after(self.delay, self.update)
        self.tk_root.mainloop()

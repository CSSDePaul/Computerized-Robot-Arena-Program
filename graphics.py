'''
Created on Feb 4, 2014

@author: excaliburhissheath
'''

from tkinter import *
from math import cos, sin, radians
from robot import Robot
from projectile import Projectile

class Graphics:
    '''
    A wrapper class to perform all graphical functions and run the __main__ loop of the simulation.
    
    An object representing the board is provided, and a delay is given to 
    '''
    
    TILE_SIZE = 10;
    '''
    Size of tiles in the grid. Specifically, the length in pixels of the sides of the square tiles.
    '''
    
    #TRIANGLE_POINTS = ((.577, 0), (-.289, -.5), (-.289, .5))
    '''
    Object coordinates for an equilateral triangle with a circumcenter at the origin, pointing at the positive x direction.
    '''
    
    ROBOT_TRIANGLE_POINTS = ((.5, 0), (-.5, -.4), (-.5, .4))
    '''
    Object coordinates for a large scalene triangle around the origin, pointing at the positive x direction and taking up a
    large amount of space in the 1x1 square around the origin
    '''
    
    PROJECTILE_TRIANGLE_POINTS = ((.3, 0), (-.3, -.2), (-.3, .2))
    '''
    Object coordinates for a scalene triangle around the origin, pointing at the positive x direction.
    '''
    
    scaledTrianglePoints = [[0,0],[0,0],[0,0]]
    '''
    Scaled object coordinates for the triangle with a circumcenter at the origin, pointing at the positive x direction.
    '''
    
    #trianglePointsOffset = (.423, .5)
    '''
    Offset of the circumcenter of the equilateral triangle from the top left (least x and least y) corner of the tile it is in.
    The tip of the triangle is touching the positive x side of the tile on the right side.
    '''
    
    trianglePointsOffset = (.5, .5)
    '''
    Offset of the center of the tile from the top left (least x and least y) corner of the tile.
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

    actorGraphics = {}
    '''
    A dict of the id's of the actor graphics,
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
        
        for key in self.board.actors:
            actor = self.board.actors[key]
            
            # The points are first gotten from the object coordinates for the object. then they are scaled, rotated and translated
            
            if type(actor) is Robot:
                #scale the points of the triangle shape to the size of the tile
                for i in range(3):
                    for j in range(2):
                        self.scaledTrianglePoints[i][j] = Graphics.ROBOT_TRIANGLE_POINTS[i][j] * Graphics.TILE_SIZE
            elif type(actor) is Projectile:
                #scale the points of the triangle shape to the size of the tile
                for i in range(3):
                    for j in range(2):
                        self.scaledTrianglePoints[i][j] = Graphics.PROJECTILE_TRIANGLE_POINTS[i][j] * Graphics.TILE_SIZE
            else:
                continue
            
            #rotate the points of the triangle shape to the correct orientation
            #so this loop does nothing
            for i in range(3):
                self.rotatedTrianglePoints[i][0] = self.scaledTrianglePoints[i][0] * cos(radians(actor.rotation)) - self.scaledTrianglePoints[i][1] * sin(radians(actor.rotation))
                self.rotatedTrianglePoints[i][1] = self.scaledTrianglePoints[i][0] * sin(radians(actor.rotation)) + self.scaledTrianglePoints[i][1] * cos(radians(actor.rotation))
                
            #translate the points of the triangle    
            for i in range(3):
                self.translatedTrianglePoints[i][0] = self.rotatedTrianglePoints[i][0] + Graphics.TILE_SIZE * (self.trianglePointsOffset[0] + actor.xPosition)
                self.translatedTrianglePoints[i][1] = self.rotatedTrianglePoints[i][1] + Graphics.TILE_SIZE * (self.trianglePointsOffset[1] + actor.yPosition)
            
            
            if type(actor) is Robot:
                 self.actorGraphics[key] = self.canvas.create_polygon(self.translatedTrianglePoints[0][0],
                                                                      self.translatedTrianglePoints[0][1],
                                                                      self.translatedTrianglePoints[1][0],
                                                                      self.translatedTrianglePoints[1][1],
                                                                      self.translatedTrianglePoints[2][0],
                                                                      self.translatedTrianglePoints[2][1],
                                                                      fill="red",
                                                                      tags=('robot', key))
            elif type(actor) is Projectile:
                 self.actorGraphics[key] = self.canvas.create_polygon(self.translatedTrianglePoints[0][0],
                                                                      self.translatedTrianglePoints[0][1],
                                                                      self.translatedTrianglePoints[1][0],
                                                                      self.translatedTrianglePoints[1][1],
                                                                      self.translatedTrianglePoints[2][0],
                                                                      self.translatedTrianglePoints[2][1],
                                                                      fill="blue",
                                                                      tags=('projectile', key))
        
    def drawActors(self):
        '''
        Does the transformations and logic needed to draw all the actors to the screen
        '''
        pass
            

    def update(self):
        '''
        Updates the board, then redraws the board.

        Performs the logic for determining when the game ends.
        '''
        
        if (len(self.board.actors) <= 1):
            # if 1 or 0 robots left, end game

            # end tkinter loop
            self.tk_root.quit()

            # print winner
            print("A winner is " + list(self.board.actors.keys())[0])

            # exit
            return

        self.board.update();
        
        for key in self.board.destroyed:
            if self.actorGraphics.get(key) != None:
                del self.actorGraphics[key];
                self.canvas.delete(key)
        
        for key in self.board.actors:
            # redraw all robots
            actor = self.board.actors[key]
            actorid = self.actorGraphics[key]
            
            if type(actor) is Robot:
                #scale the points of the triangle shape to the size of the tile
                for i in range(3):
                    for j in range(2):
                        self.scaledTrianglePoints[i][j] = Graphics.ROBOT_TRIANGLE_POINTS[i][j] * Graphics.TILE_SIZE
            elif type(actor) is Projectile:
                #scale the points of the triangle shape to the size of the tile
                for i in range(3):
                    for j in range(2):
                        self.scaledTrianglePoints[i][j] = Graphics.PROJECTILE_TRIANGLE_POINTS[i][j] * Graphics.TILE_SIZE
            else:
                continue
            
            #rotate the points of the triangle shape to the correct orientation
            #so this loop does nothing
            for i in range(3):
                self.rotatedTrianglePoints[i][0] = self.scaledTrianglePoints[i][0] * cos(radians(actor.rotation)) - self.scaledTrianglePoints[i][1] * sin(radians(actor.rotation))
                self.rotatedTrianglePoints[i][1] = self.scaledTrianglePoints[i][0] * sin(radians(actor.rotation)) + self.scaledTrianglePoints[i][1] * cos(radians(actor.rotation))
                
            #translate the points of the triangle    
            for i in range(3):
                self.translatedTrianglePoints[i][0] = self.rotatedTrianglePoints[i][0] + Graphics.TILE_SIZE * (self.trianglePointsOffset[0] + actor.xPosition)
                self.translatedTrianglePoints[i][1] = self.rotatedTrianglePoints[i][1] + Graphics.TILE_SIZE * (self.trianglePointsOffset[1] + actor.yPosition)
            
            self.canvas.coords(actorid, self.translatedTrianglePoints[0][0],
                                        self.translatedTrianglePoints[0][1],
                                        self.translatedTrianglePoints[1][0],
                                        self.translatedTrianglePoints[1][1],
                                        self.translatedTrianglePoints[2][0],
                                        self.translatedTrianglePoints[2][1])   
        
        # reschedule update
        self.tk_root.after(self.delay, self.update)
        
    def start(self):
        '''
        Starts the tkinter's __main__ loop and schedules the first update event.
        '''
        self.tk_root.after(self.delay, self.update)
        self.tk_root.mainloop()

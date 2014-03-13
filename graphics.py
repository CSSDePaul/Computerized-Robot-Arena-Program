'''
Created on Feb 4, 2014

@author: excaliburhissheath
'''

from tkinter import Tk, Canvas, N, W, E, S
from math import cos, sin, radians
from robot import Robot
from projectile import Projectile

class Graphics:
    '''
    A wrapper class to perform all graphical functions and run the main loop of the simulation.
    
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
        
        # DEBUGTASTIC CODE - binds the update method to escape for stepwise debugging
#         self.tk_root.bind("<space>", self.update)
        
        # binds the exit method to the escape key
        self.tk_root.bind("<Escape>", self.exit) 
        
        # initialize tk canvas object
        self.canvas = Canvas(self.tk_root)

        #set canvas width and height to the number of tiles times the number of pixels per tile
        self.canvas = Canvas(self.tk_root, width=board.BOARD_SIZE * self.TILE_SIZE, height=board.BOARD_SIZE * self.TILE_SIZE)#Canvas(self.tk_root)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        
        for key in self.board.actors:
            self.drawActor(key)
        
    def drawActor(self, key):
        '''
        Does the transformations and logic needed to draw the actors to the screen
        '''
        actor = self.board.actors[key]
        
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
            return
        
        #rotate the points of the triangle shape to the correct orientation
        #so this loop does nothing
        for i in range(3):
            self.rotatedTrianglePoints[i][0] = self.scaledTrianglePoints[i][0] * cos(radians(actor.rotation)) - self.scaledTrianglePoints[i][1] * sin(radians(actor.rotation))
            self.rotatedTrianglePoints[i][1] = self.scaledTrianglePoints[i][0] * sin(radians(actor.rotation)) + self.scaledTrianglePoints[i][1] * cos(radians(actor.rotation))
            
        #translate the points of the triangle    
        for i in range(3):
            self.translatedTrianglePoints[i][0] = self.rotatedTrianglePoints[i][0] + Graphics.TILE_SIZE * (self.trianglePointsOffset[0] + actor.xPosition)
            self.translatedTrianglePoints[i][1] = self.rotatedTrianglePoints[i][1] + Graphics.TILE_SIZE * (self.trianglePointsOffset[1] + actor.yPosition)
        
        #if already not in actorGraphics dict
        if self.actorGraphics.get(key) == None:
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
        # now you can assume that key is in actorGraphics dict
        actorid = self.actorGraphics[key]
        self.canvas.coords(actorid, self.translatedTrianglePoints[0][0],
                            self.translatedTrianglePoints[0][1],
                            self.translatedTrianglePoints[1][0],
                            self.translatedTrianglePoints[1][1],
                            self.translatedTrianglePoints[2][0],
                            self.translatedTrianglePoints[2][1]) 
            
    def update(self, event = None):
        '''
        Updates the board, then redraws the board.

        Performs the logic for determining when the game ends.
        '''
        
        print('\nUPDATE BOARD WITH FULL LOGIC')
        
        # =================
        # END OF GAME LOGIC
        # =================
        
        # if 1 or 0 robots left, end game
        if len(self.board.getRobots()) == 1:
            
            # Only one robot left, that robot is the winner
            # print out winner and exit

            # print winner
            print("A winner is " + list(self.board.getRobots().keys())[0])

            # exit without closing tk window
            return
        elif len(self.board.getRobots()) < 1:
            
            # no robots left,
            # declare game a tie
            
            #print tie
            print("The game is a tie, everyone is dead.")
            
            # exit without closing tk window
            return
        
        # ============
        # UPDATE BOARD
        # ============

        self.board.update();
        
        # ======================
        # CLEAR DESTROYED ACTORS
        # ======================
        
        for key in self.board.destroyed:
            if self.actorGraphics.get(key) != None:
                
                # delete graphics object using the stashed key
                self.canvas.delete(self.actorGraphics[key])
                
                # delete stashed key
                del self.actorGraphics[key];
        
        # ===============
        # UPDATE GRAPHICS
        # ===============
        
        for key in self.board.actors:
            self.drawActor(key)
        
        # reschedule update
        self.tk_root.after(self.delay, self.update)
        
    def exit(self, event = None):
        '''
        Ends the Tkinter main loop and exits the game.
        '''
        
        self.tk_root.quit()
        
    def start(self):
        '''
        Starts the tkinter's main loop and schedules the first update event.
        '''
        self.tk_root.after(self.delay, self.update)
        self.tk_root.mainloop()

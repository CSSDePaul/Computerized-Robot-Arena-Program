'''
Created on Feb 4, 2014

@author: excaliburhissheath
'''

from tkinter import Tk, Canvas, N, W, E, S
from math import cos, sin, radians
from robot import Robot
from projectile import Projectile

from threading import Thread
'''
Import Thread class to use as parent of Graphics object.
'''

from queue import Queue
'''
Import synchronized queue class for use in queueing updates.
'''

import board
''' Import board module to get access to board.DEFAULT_BOARD_SIZE '''

class Graphics(Thread):
    '''
    A wrapper class to perform all graphical functions and run the main loop of the simulation.
    
    An object representing the board is provided, and a delay is given to 
    '''
    
    TILE_SIZE = 10;
    '''
    Size of tiles in the grid. Specifically, the length in pixels of the sides of the square tiles.
    '''
    
#     TRIANGLE_POINTS = ((.577, 0), (-.289, -.5), (-.289, .5))
#     '''
#     Object coordinates for an equilateral triangle with a circumcenter at the origin, pointing at the positive x direction.
#     '''
    
    ROBOT_TRIANGLE_POINTS = ((.5, 0), (-.5, -.4), (-.5, .4))
    '''
    Object coordinates for a large scalene triangle around the origin, pointing at the positive x direction and taking up a
    large amount of space in the 1x1 square around the origin
    '''
    
    PROJECTILE_TRIANGLE_POINTS = ((.3, 0), (-.3, -.2), (-.3, .2))
    '''
    Object coordinates for a scalene triangle around the origin, pointing at the positive x direction.
    '''
    
    scaledTrianglePoints = [[0, 0], [0, 0], [0, 0]]
    '''
    Scaled object coordinates for the triangle with a circumcenter at the origin, pointing at the positive x direction.
    '''
    
#     trianglePointsOffset = (.423, .5)
#     '''
#     Offset of the circumcenter of the equilateral triangle from the top left (least x and least y) corner of the tile it is in.
#     The tip of the triangle is touching the positive x side of the tile on the right side.
#     '''
    
    trianglePointsOffset = (.5, .5)
    '''
    Offset of the center of the tile from the top left (least x and least y) corner of the tile.
    '''
    
    rotatedTrianglePoints = [[0, 0], [0, 0], [0, 0]]
    ''' Points of the triangle rotated around the circumcenter. '''
    
    translatedTrianglePoints = [[0, 0], [0, 0], [0, 0]]
    ''' Points of the triangle translated into world coordinates. '''
    
    tk_root = None
    ''' The root tkinter object. '''
    
    delay = 0
    ''' The interval between updates of the board (in miliseconds). '''

    boardSize = 0
    ''' The length of the sizes of the square board. '''

    canvas = None
    ''' The tkinter canvas being used to render the graphics '''

    actorGraphics = {}
    '''
    A dict of the id's of the actor graphics,
    indexed by the key for the corresponding robot object in board.robots .
    '''
    
    updateQueue = None
    '''
    Queue of board copy frames to be rendered.
    '''
    
    exitFlag = False
    '''
    Flag used to indicate that the graphics window has been closed.
    '''

    def __init__(self, delay=500, boardSize = board.DEFAULT_BOARD_SIZE):
        '''
        Constructor for Graphics class.
        
        @note: Initialization of all tkinter stuff happens in run() for threading reasons.
        '''        
        # assign parameter values
        self.delay = delay;
        self.boardSize = boardSize
            
        # =================================
        # DO IMPORTANT THINGS FOR THREADING
        # =================================
        
        # initialize update queue
        self.updateQueue = Queue()
        
        # call thread constructor
        Thread.__init__(self)
        
    def drawActor(self, actor):
        '''
        Does the transformations and logic needed to draw the actors to the screen
        '''
        
        # retrieve actor's name to use as key in actorGraphics dict
        key = actor.name
        
        if type(actor) is Robot:
            # scale the points of the triangle shape to the size of the tile
            for i in range(3):
                for j in range(2):
                    self.scaledTrianglePoints[i][j] = Graphics.ROBOT_TRIANGLE_POINTS[i][j] * Graphics.TILE_SIZE
        elif type(actor) is Projectile:
            # scale the points of the triangle shape to the size of the tile
            for i in range(3):
                for j in range(2):
                    self.scaledTrianglePoints[i][j] = Graphics.PROJECTILE_TRIANGLE_POINTS[i][j] * Graphics.TILE_SIZE
        else:
            return
        
        # rotate the points of the triangle shape to the correct orientation
        # so this loop does nothing
        for i in range(3):
            self.rotatedTrianglePoints[i][0] = self.scaledTrianglePoints[i][0] * cos(radians(actor.rotation)) - self.scaledTrianglePoints[i][1] * sin(radians(actor.rotation))
            self.rotatedTrianglePoints[i][1] = self.scaledTrianglePoints[i][0] * sin(radians(actor.rotation)) + self.scaledTrianglePoints[i][1] * cos(radians(actor.rotation))
            
        # translate the points of the triangle    
        for i in range(3):
            self.translatedTrianglePoints[i][0] = self.rotatedTrianglePoints[i][0] + Graphics.TILE_SIZE * (self.trianglePointsOffset[0] + actor.xPosition)
            self.translatedTrianglePoints[i][1] = self.rotatedTrianglePoints[i][1] + Graphics.TILE_SIZE * (self.trianglePointsOffset[1] + actor.yPosition)
        
        # if already not in actorGraphics dict
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
    
    def update(self, state):
        '''
        Public function used to queue a graphical update.
        
        @param state: The state of the board to be displayed for this update. state is pushed onto updateQueue.
        '''
        
        print('Graphics.update() called')
        
        # put state in updateQueue
        self.updateQueue.put(state)
       
    def _update(self, event=None):
        '''
        Internal update function which is injected into the tkinter main loop.
        
        @note: _update() should never be called directly, it should only ever be registered in the tkinter main loop.
        To notify the Graphics object that it needs to update, call Graphics.update() instead.
        '''
        
        # =================
        # CHECK UPDATE FLAG
        # =================
        
        # only update if there are queued updates
        # otherwise reschedule the update method without re-rendering the graphics
        if not self.updateQueue.empty():
            
            # remove next queued update
            board = self.updateQueue.get()
        
            # ======================
            # CLEAR DESTROYED ACTORS
            # ======================
            
            for key in board.destroyed:
                if self.actorGraphics.get(key) != None:
                    
                    # delete graphics object using the stashed key
                    self.canvas.delete(self.actorGraphics[key])
                    
                    # delete stashed key
                    del self.actorGraphics[key];
            
            # ===============
            # UPDATE GRAPHICS
            # ===============
            
            for key in board.actors:
                self.drawActor(board.actors[key])
        
        # reschedule update
        self.tk_root.after(self.delay, self._update)
        
    def exit(self, event=None):
        '''
        Ends the Tkinter main loop and exits the game.
        '''
        
        # set exit flag
        self.exitFlag = True
        
        # kill tk mainloop
        self.tk_root.quit()
        
    def run(self):
        '''
        Initializes the tkinter graphics and starts the mainloop.
        '''
        
        print('Graphics thread started')
        
        # =========================
        # INITIALIZE TKINTER STUFFS
        # =========================
        
        # reset flags
        self.updateFlag = False
        self.exitFlag = False
        
        # initialize tk_root
        self.tk_root = Tk()
        
        # DEBUGTASTIC CODE - binds the update method to escape for stepwise debugging
#         self.tk_root.bind("<space>", self.update)
        
        # binds the exit method to the escape key
        self.tk_root.bind("<Escape>", self.exit)
        
        # forces tkinter to call exit() when the window is closed (hitting the x button)
        self.tk_root.protocol("WM_DELETE_WINDOW", self.exit)
        
        # initialize tk canvas object
        self.canvas = Canvas(self.tk_root)
        
        print('canvas initialize to {}'.format(self.canvas))

        # set canvas width and height to the number of tiles times the number of pixels per tile
        self.canvas = Canvas(self.tk_root, width = self.boardSize * self.TILE_SIZE, height = self.boardSize * self.TILE_SIZE)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S)) # I don't even know what this is doing
              
        # ===============
        # START MAIN LOOP
        # ===============
        
        self.tk_root.after(10, self._update)
        self.tk_root.mainloop()

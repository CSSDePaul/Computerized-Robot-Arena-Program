'''
Created on Mar 1, 2014

@author: excaliburhissheath
'''

from actor import Actor

class Projectile(Actor):
    '''
    A class representing a basic projectile on the board.
    '''
    
    STARTING_HEALTH = 1
    '''
    The starting health value for robots on the field.
    '''
        
    def __init__(self, x, y, theta, name = None):
        '''
        Constructor method.
        
        @param x: The starting x coordinate of the projectile.
        
        @param y: The starting y coordinate of the projectile.
        
        @param theta: The starting theta of the projectile.
    
        The projectile is assumed to be in front of a robot.
        '''
        
        # set parameter values
        self.xPosition = x
        self.yPosition = y
        self.rotation = theta
        self.health = STARTING_HEALTH
        
        # name is the default string of the object,
        # which includes the memory address,
        # guaranteeing that the string is unique.
        self.name = id(self);
        
    def takeAction(self, board):
        '''
        Moves the projectile forward one space in the current direction.
        If it runs into a wall, it will destroy itself
        
        @param board: A reference to the board object. This is used for checking bounds and collisions.
        '''
        newX = self.xPosition + cos(radians(self.rotation))
        newY = self.yPosition + sin(radians(self.rotation))
        
        # if board is infinite, no need to check against board.Board bounds
        if board.BOARD_SIZE > 0:
            # if the projectile exits the board, flag it for destruction
            if newX < 0 or newX >= board.BOARD_SIZE:
                health = 0;
                return;   
            if newY < 0 or newY >= board.BOARD_SIZE:
                health = 0;
                return;
            
        # update position
        self.xPosition = newX
        self.yPosition = newY
        
        print("action taken by %s is moveForward" % (self.name))
        
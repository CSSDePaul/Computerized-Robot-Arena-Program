'''
Created on Mar 1, 2014

@author: excaliburhissheath
'''

from actor import Actor

from utility import forwardCoords

import logging
''' Import logging module. '''

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
        self.health = Projectile.STARTING_HEALTH
        
        # name is the default string of the object,
        # which includes the memory address,
        # guaranteeing that the string is unique.
        if not name:
            self.name = 'Projectile_' + str(id(self));

        else:
            self.name = name
        
    def takeAction(self, board):
        '''
        Moves the projectile forward one space in the current direction.
        If it runs into a wall, it will destroy itself.
        
        @param board: A reference to the board object. This is used for checking bounds and collidingActors.
        '''
        
        logging.debug("%s is moving forward" % (self.name))
        
        # get the coordinates in front of the robot
        coords = forwardCoords(self.xPosition, self.yPosition, self.rotation, board)
        
        # if out of bounds, destroy self
        if coords is None:
            
            # debugging output
            logging.debug('{} is off the board'.format(self.name))
            
            self.health = 0
            return
        
        # ===================
        # TEST FOR COLLISIONS
        # ===================
        
        # retrieve list of actors in new space
        collidingActors = board.occupied(coords[0], coords[1])
        
        if len(collidingActors) > 0:
            
            logging.debug('actors in front of {}: {}'.format(self.name, str(collidingActors)))
            
            # iterate over actors in space
            for actor in collidingActors:
                
                logging.debug(self.name + " to collide with actor " + actor)
            
                # if actor is robot, damage robot and destroy self
                if actor in board.getRobots():
                    
                    logging.debug(self.name + " colliding with robot " + actor)
                    
                    # run collision logic
                    board.collision(self.name, actor)
                    
                    # reset health to 0 to ensure correct destruction
                    self.health = 0
                elif actor in board.getProjectiles():
                    # actor is a projectile
                    # if both are not facing the same direction, both are destroyed
                    
                    logging.debug(self.name + " colliding with projectile " + actor)
                    
                    # test if both are facing same direction
                    if not (board.actors[actor].rotation == self.rotation):
                        
                        # collide both
                        board.collision(self.name, actor)
        
        # projectile still on the board
        if (self.health > 0):
            self.xPosition = coords[0]
            self.yPosition = coords[1]
        
    def __copy__(self):
        '''
        Create a safe copy of the projectile, containing only positional and type info.
        '''
        
        return Projectile(self.xPosition, self.yPosition, self.rotation, self.name)
'''
Created on Mar 12, 2014

@author: excaliburhissheath
'''

from math import cos, sin, radians
'''
math module for use in forwardCoords()
'''

from actor import Actor
'''
Actor class from actor module for use in manhattanDistance()
'''

import random
'''
random module used in decay()
'''

def forwardCoords(x, y, rotation, board = None):
    '''
    Returns the coordinates of one forward move as a tuple in the form of (x,y,rotation).
    
    @param x: The current x coordinate.
    @param y: The current y coordinate.
    @param rotation: The current rotation.
    @param board: The board being considered.
    This is optional, if it is not provided the new position will not be checked to see if they are out of bounds (even if they are negative!).
    
    @return: Returns a tuple with the new coordinates as integers. If a value is provided for board, the new position will be checked against the bounds of the board,
    and if it is out of bound the function will return None.
    '''
    
    # calculate the new x and y coordinates using mathemagic
    newX = int(x + cos(radians(rotation)))
    newY = int(y + sin(radians(rotation)))
    
    returnval = (newX, newY, rotation)
    
    # if board exists, check against bounds
    # if out of bounds, set returnval to None
    if not (board is None) and (newX < 0 or newY < 0 or newX >= board.BOARD_SIZE or newY >= board.BOARD_SIZE):
        returnval = None
    
    return returnval

def manhattanDistance(loc1, loc2):
    '''
    Returns the manhattan distance between the two locations.
    
    Either location may be either an Actor object or a tuple in the format (x,y...).
    
    @param loc1: The first location. It may be either an Actor object or a tuple in the format (x,y...).
    @param loc2: The second location. It may be either an Actor object or a tuple in the format (x,y...).
    
    @return: The manhattan distance between the two locations as an integer value.
    '''
    
    # convert loc1 to position tuple
    if isinstance(loc1, Actor):
        loc1 = (loc1.xPosition, loc1.yPosition)
        
    # convert loc2 to position tuple
    if isinstance(loc2, Actor):
        loc2 = (loc2.xPosition, loc2.yPosition)
        
    # calculate and return result
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

def decay(probability):
    '''
    Performs the decay function used in Games and Sets.
    
    Generates a random number on [0.0, 1.0), and if that number
    is less than probability, returns True, otherwise returns False.
    
    @param probability: The probability for the decay function,
    i.e., the probability that this function will return false.
    
    @return: False if the random value is less than probability, True otherwise.
    '''
    
    return random.random() < probability
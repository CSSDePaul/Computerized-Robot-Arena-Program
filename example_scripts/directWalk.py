'''
Created on Mar 12, 2014

@author: excaliburhissheath
'''

from utility import forwardCoords, manhattanDistance

from robot import Robot

import logging

class robotBehavior:
    '''
    A behavior that make the robot walk in a straight line towards the closest robot.
    '''

    def decideAction(self, robot, board, actions):
        '''
        Walks towards the other robot and tries to run into it.
        '''
        
        # get the list of robots from the board
        robots = board.getRobots()
        
        # if no other robot, do nothing
        if len(robots) <= 1:
            return
        
        robotKeys = list(robots.keys())
        
        # temporary hacky workaround
        # get the other robot (future versions should find the closest robot)
        closest = robots[robotKeys[0]]
        
        # if first robot is this robot, get second robot
        if robotKeys[0] == robot.name:
            closest = robots[robotKeys[1]]
        
        # get current distance to target robot
        currentDistance = manhattanDistance(robot, closest)
        
        # get coordinates of space in front of robot
        forwardPos = forwardCoords(robot.xPosition, robot.yPosition, robot.rotation)
        
        # if other robot is right in front, shoot that robot
        actors_ahead = board.occupied(forwardPos[0], forwardPos[1])
        
        logging.debug(actors_ahead)
        
        fire = False
        for actor_name in actors_ahead:
            fire = True if isinstance(board.actors[actor_name], Robot) else fire
            
        if fire:
            logging.debug('FIRE AWAY')
            return 'SHOOT_PROJECTILE'
        
        # get distance of forwardPos from target
        forwardDistance = manhattanDistance(forwardPos, closest)
        
        # if forward gets robot closer to target, move forward
        if forwardDistance < currentDistance:
            return 'MOVE_FORWARD'
        # otherwise turn right
        else:
            return 'TURN_RIGHT'

    def __init__(self):

        pass
        
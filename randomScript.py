import robot
import random

MOVEFUNCTIONS = [robot.Robot.turnLeft, robot.Robot.turnRight, robot.Robot.moveForward]

class randomScript:

	# Returns a string from Board.MOVEFUNCTIONS.keys()
	# this is the action the agent decided to take
	# the human player uploads a script that is called by this action 
	def decideAction(self, robot, Board):
		'''
		Returns the alias to a random movement function in the robot class
		'''
		return random.choice(MOVEFUNCTIONS)
		
	def __init__(self):
		pass

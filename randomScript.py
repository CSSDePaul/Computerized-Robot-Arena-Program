import random

class robotBehavior:

	# Returns a string from Board.MOVEFUNCTIONS.keys()
	# this is the action the agent decided to take
	# the human player uploads a script that is called by this action 
	def decideAction(self, robot, board, actions):
		'''
		Returns the alias to a random movement function in the robot class
		'''
		return random.choice(actions)
		
	def __init__(self):
		pass

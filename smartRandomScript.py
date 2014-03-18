import random
import utility

class robotBehavior:

	# Returns a string from Board.MOVEFUNCTIONS.keys()
	# this is the action the agent decided to take
	# the human player uploads a script that is called by this action 
	def decideAction(self, robot, board, actions):
		'''
		Returns the alias to a random movement function in the robot class
		'''
		
		choice = random.choice(actions)
		if (choice == 'MOVE_FORWARD'):
			
			forwardLoc = utility.forwardCoords(robot.xPosition, robot.yPosition, robot.rotation, board)
			
			# if going to move off the board, turn
			if forwardLoc is None:
				return 'TURN_RIGHT'
			
			# do other stuff
			isOccupied = board.occupied(forwardLoc[0],forwardLoc[1])
			if isOccupied is None:
				#space in front is outside the board
				return 'TURN_RIGHT'
			if isOccupied:
				#if something is in front, shoot at it
				return 'SHOOT_PROJECTILE'
			else:
				#if something isn't in front, move forward
				return 'MOVE_FORWARD'
		
		return choice
		
	def __init__(self):
		pass

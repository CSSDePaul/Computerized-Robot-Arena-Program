from robot import robot

class boardState:
	BOARD_SIZE = 10
	'''
	The size of the board, specifically the number of tiles on the side of a square board.
	
	If BOARD_SIZE is 0, the board is unbounded.
	'''
	
	MOVEFUNCTIONS = {
					'turnLeft':	 	robot.turnLeft,
					'turnRight': 	robot.turnRight,
					'moveForward':	robot.moveForward,
					}
	'''
	A dict containing the available functions for robots to perform
	and their corresponding function calls.
	'''
	
	robots = []
	'''
	A list containing the robots on the board.
	'''
	
	def __init__(self):
		'''
		Initializes robots to add to boardState
		'''
		
		self.robots.append(robot(0, 0, 0, "Robot0"))

	def update(self):
		'''
		Updates the positions of all robots and performs all other simulation logic.
		'''
		
		for player in self.robots:
			player.takeAction(self)
			print(player)

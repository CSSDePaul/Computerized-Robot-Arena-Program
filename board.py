import robot
from randomScript import decideAction

class Board:
	'''
	A representation of the game board.
	
	Keeps a collection of the robots in play
	and performs the logic for updating the board each tick.
	'''
	
	BOARD_SIZE = 10
	'''
	The size of the board, specifically the number of tiles on the side of a square board.
	
	If BOARD_SIZE is 0, the board is unbounded.
	'''
	
	robots = {}
	'''
	A list containing the robot.Robots on the board.
	'''
	
	def __init__(self):
		'''
		Initializes robot.Robots to add to Board
		'''
		
		print("initializing board")
		
		self.robots["Robot0"] = robot.Robot(0, 0, 0, decideAction, "Robot0")

	def update(self):
		'''
		Updates the positions of all robot.Robots and performs all other simulation logic.
		'''
		
		for key in self.robots:
			print(key + " moving")
			self.robots[key].takeAction(self)

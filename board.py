import robot

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
	
	def __init__(self, scripts):
		'''
		Initializes robot.Robots to add to Board
		
		@param scripts: function pointers to the scripts which define the robot behaviors.
		One robot will be created for each script provided.
		'''
		
		print("initializing board")
		
		for i in range(len(scripts)):
			robotName = "Robot_" + str(i)
			self.robots[robotName] = robot.Robot(0, 0, 0, scripts[i], robotName)

	def update(self):
		'''
		Updates the positions of all robot.Robots and performs all other simulation logic.
		'''
		
		for key in self.robots:
			self.robots[key].takeAction(self)

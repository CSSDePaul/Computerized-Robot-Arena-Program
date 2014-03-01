import robot
'''
provides access to robot constructor.
'''

from random import shuffle
'''
Import shuffle function to randomize turn order.
'''

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
	A dict containing the active robot.Robots on the board.
	'''

	destroyed = {}
	'''
	A dict for stashing destroyed robots.
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
			self.robots[robotName] = robot.Robot(5, 5, 0, scripts[i], robotName)

	def update(self):
		'''
		Updates the positions of all robots and performs all other simulation logic.
		'''
		
		# make a copy of the list of keys so python doesn't freak out if a robot gets deleted
		keys = list(self.robots.keys())

		# shuffle list for random turn order
		shuffle(keys)

		for key in keys:

			# double check that robots[key] has not been destroyed
			if key not in self.robots:
				continue

			# Have robot act
			self.robots[key].takeAction(self)

			# check to see if any robot has been destroyed
			keys2 = list(self.robots.keys())
			for key2 in keys2:

				if self.robots[key2].health == 0:

					print(self.robots[key2], " destroyed")

					# stash destroyed robot
					self.destroyed[key2] = self.robots[key2]

					# remove destroyed robot from robot list
					del self.robots[key2]

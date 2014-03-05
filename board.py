import robot
'''
provides access to robot constructor.
'''
import projectile
'''
provides access to projectile constructor.
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
	
	BOARD_SIZE = 20
	'''
	The size of the board, specifically the number of tiles on the side of a square board.
	
	If BOARD_SIZE is 0, the board is unbounded.
	'''
	
	actors = {}
	'''
	A dict containing the active actors on the board.
	'''

	destroyed = {}
	'''
	A dict for stashing destroyed actors.
	'''
	
	def __init__(self, scripts):
		'''
		Initializes robot.actors to add to Board
		
		@param scripts: function pointers to the scripts which define the robot behaviors.
		One robot will be created for each script provided.
		'''
		
		print("initializing board")
		
		for i in range(len(scripts)):
			robotName = "Robot_" + str(i)
			
			print("initializing " + robotName)
			
			self.actors[robotName] = robot.Robot(5+i, 5+i, 0, scripts[i], robotName)
		
		self.actors["Projectile_0"] = projectile.Projectile(0, 0, 0,"Projectile_0")
		self.actors["Projectile_1"] = projectile.Projectile(0, 1, 90,"Projectile_1")
		self.actors["Projectile_1"] = projectile.Projectile(0, 15, 90,"Projectile_1")
			

	def update(self):
		'''
		Updates the positions of all actors and performs all other simulation logic.
		'''
		
		# make a copy of the list of keys so python doesn't freak out if a robot gets deleted
		keys = list(self.actors.keys())
		
		# shuffle list for random turn order
		# chosen so that turn order is not predictably in order to simulate all 
		# action happening concurrently on average
		shuffle(keys)

		for key in keys:

			# double check that actors[key] has not been destroyed
			if key in self.destroyed:
				continue

			# Have robot act
			self.actors[key].takeAction(self)

			# check to see if any robot has been destroyed
			keys2 = list(self.actors.keys())
			for key2 in keys2:

				# health == 0 is used a general flag for destroying an actor
				if self.actors[key2].health <= 0:

					print(self.actors[key2], " destroyed")

					# stash destroyed robot
					self.destroyed[key2] = self.actors[key2]

					# remove destroyed robot from robot list
					del self.actors[key2]

	def occupied(self, x, y):
		'''
		Returns true is board[x, y] is occupied.

		@returns true if there is an actor at coordinates (x,y).
		'''
		for key in self.actors:
			actor = self.actors[key]
			if x == actor.x and y == actor.y:
				return True

		return False
	
	def spawnProjectile(self, x, y, rotation):
		'''
		Instantiates a new projectile object and add it to the list of actors.
		
		@param x: the x coordinate of the projectile to be spawned
		@param y: the y coordinate of the projectile to be spawned
		@param rotation: the direction the projectile should move in.
		'''
		
		# if board is infinite, no need to check against board bounds
		if self.BOARD_SIZE > 0:
			
			# if out of bounds, return without spawning projectiles
			if x < 0 or x >= self.BOARD_SIZE:
				return
			if y < 0 or y >= self.BOARD_SIZE:
				return
			
		# spawn projectile
		newProjectile = projectile.Projectile(x, y, rotation)
		self.actors[newProjectile.name] = newProjectile;
		
	def getRobots(self):
		'''
		Returns a dict containing only the robots on the board.
		'''
		
		result = {}
		
		for key in self.actors:
			if (isinstance(self.actors[key], robot.Robot)):
				result[key] = self.actors[key]
				
		return result
	
	def getProjectiles(self):
		'''
		Returns a dict containing only the robots on the board.
		'''
		
		result = {}
		
		for key in self.actors:
			if (isinstance(self.actors[key], projectile.Projectile)):
				result[key] = self.actors[key]

		return result
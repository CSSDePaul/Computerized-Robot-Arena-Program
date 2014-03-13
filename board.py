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

from copy import deepcopy
"""
Import deepcopy function to allow safe board-state passing.
"""

class Board:
	'''
	A representation of the game board.
	
	Keeps a collection of the robots in play
	and performs the logic for updating the board each tick.
	
	@note: For the sake of consistency and type safety, all references to actors passed into and out of the Board class
	should be strings representing the name of the actor, and therefore the key of the actor in the Board.actors dict.
	Methods of Board should always return the name, and should always take the name in as parameters when referencing actors.
	'''
	
	BOARD_SIZE = 10
	'''
	The size of the board, specifically the number of tiles on the side of a square board.
	Actors on the board may have coordinates in the range of [0,BOARD_SIZE),
	that is, 0 <= coord < BOARD_SIZE
	
	If BOARD_SIZE is 0, the board is unbounded.
	'''

	actors = None
	'''
	An instance-variable dict containing the active actors on the board.
	'''

	destroyed = None
	'''
	An instance-variable dict for stashing destroyed actors.
	'''

	def __init__(self, scripts):
		'''
		Initializes robot.actors to add to Board
		
		@param scripts: function pointers to the scripts which define the robot behaviors.
		One robot will be created for each script provided.
		'''
		
		#initialization of instance variables (necessary for copying purposes)
		self.actors = {}
		self.destroyed = {} 

		print("initializing board")
		
		for i in range(len(scripts)):
			robotName = "Robot_" + str(i)
			
			print("initializing " + robotName)
			
			self.actors[robotName] = robot.Robot(4*i, 4*i, 0, scripts[i], robotName)			

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
		Returns the names of the actors occupying (x, y), returns None otherwise

		@returns a list containing the names of the actors (keys in Board.actors) occupying (x, y). The list is empty if the space is empty.
		'''
		
		# =======================================================
		# iterate over the list of actors
		# if the actor's coordinates match the given coordinates,
		# append actor to the list of actors
		# =======================================================
		
		actorsInSpace = []
		
		for key in self.actors:
			actor = self.actors[key]
			if x == actor.xPosition and y == actor.yPosition:
				actorsInSpace.append(key)


		return actorsInSpace
	
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

	def collision(self, actor1, actor2, damage1 = 1, damage2 = 1):
		'''
		Simulates a collision between actor1 and actor2 by applying some amount of damage to them.
		
		Subtracts damage1 from actor1's health, and subtracts damage2 from actor2's health.
		
		@param actor1: The first actor in the collision, should be a key to the object in self.actors.
		@param actor2: The second actor in the collision, should be a key to the object in self.actors.
		@param damage1: The damage to be applied to actor1. Defaults to 1.
		@param damage2: The damage to be applied to actor2. Defaults to 1.
		'''
		
		print ('collision between {} and {}'.format(actor1, actor2))
		
		# apply damage to robots
		self.actors[actor1].health -= damage1
		self.actors[actor2].health -= damage2
		
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
		Returns a dict containing only the projectiles on the board.
		'''
		
		result = {}
		
		for key in self.actors:
			if (isinstance(self.actors[key], projectile.Projectile)):
				result[key] = self.actors[key]

		return result
		
	def getcopy(self):
		"""
		Returns a deep copy of the board to be passed to a script.
		Everything is the same except that robot scripts have been removed.
		"""
		boardCopy = deepcopy(self)
		robots = boardCopy.getRobots() #references to the robot copies
		for robotkey in robots:
			boardCopy.actors[robotkey].script = None 
		return boardCopy

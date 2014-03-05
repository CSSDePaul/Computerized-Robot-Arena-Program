from actor import Actor
import projectile

from math import cos, sin, radians

class Robot(Actor):
	'''
	The parent class for all robot scripts.

	Each robot is given an x and y coordinate,
	a value for theta representing rotation,
	and a string with a unique identifying name for the robot.
	'''

	DEFAULT_HEALTH = 1
	'''
	The starting health value for robots on the field.
	'''
	
	script = None
	'''
	A function pointer to the script defining the behavior of the robot.
	'''

	def __init__(self, x, y, theta, script, name = None, health = DEFAULT_HEALTH):
		'''
		Constructor method.
		
		@param x: The starting x coordinate of the robot.
		
		@param y: The starting y coordinate of the robot.
		
		@param theta: The starting theta of the robot.
		
		@param script: A function pointer to the script defining the behavior of the robot.
		
		@param name: The name of the robot. If no name is provided a unique, random name will be provided.

		@param health: The starting health of the robot. Defaults to Robot::DEFAULT_HEALTH
		'''
		
		# set parameter values
		self.xPosition = x
		self.yPosition = y
		self.rotation = theta
		self.script = script
		self.health = health
		
		# if no name provided, create unique name
		if name is None:
			
			# name is the default string of the object,
			# which includes the memory address,
			# guaranteeing that the string is unique.
			name = id(self);
			
		self.name = name

	def takeAction(self, board):
		'''
		Call the behavior script and then take the chosen action.
		'''
		
		# call behavior script
		# behavior script returns function pointer for action to be performed
		action = self.script.decideAction(self, board, list(Robot.ACTIONS.keys()))
		
		if (action in Robot.ACTIONS.keys()):
			print("action taken by %s is %s" % (self.name, str(action)))
			
			action = Robot.ACTIONS[action]
			
			action(self, board)
		else:
			pass

	def turnLeft(self, board):
		'''
		Rotate the robot 90 degrees to the left.
		'''
		self.rotation = (self.rotation + 90) % 360
	
	def turnRight(self, board):
		'''
		Rotate the robot 90 degrees to the right
		'''
		self.rotation = (self.rotation - 90) % 360
		
	def shootProjectile(self, board):
		'''
		Creates a projectile in front and adds it to the board
		
		@param board: A reference to the board object. This is used for checking bounds and collisions.
		'''
		targetX = self.xPosition + cos(radians(self.rotation))
		targetY = self.yPosition + sin(radians(self.rotation))
		
		# if board is infinite, no need to check against board.Board bounds
		if board.BOARD_SIZE > 0:
			if targetX < 0 or targetX >= board.BOARD_SIZE:
				return
			if targetY < 0 or targetY >= board.BOARD_SIZE:
				return
			
		# create projectile
		newProjectile = projectile.Projectile(targetX, targetY, self.rotation)
		board.actors[newProjectile.name] = newProjectile;
		
	def moveForward(self, board):
		'''
		Moves the robot forward one space in the current direction.
		If it runs into a wall, it will simply not move.
		
		@param board: A reference to the board object. This is used for checking bounds and collisions.
		'''
		newX = self.xPosition + cos(radians(self.rotation))
		newY = self.yPosition + sin(radians(self.rotation))
		
		# if board is infinite, no need to check against board.Board bounds
		if board.BOARD_SIZE > 0:
			if newX < 0 or newX >= board.BOARD_SIZE:
				return
			if newY < 0 or newY >= board.BOARD_SIZE:
				return
			
		# update position
		self.xPosition = newX
		self.yPosition = newY
	
	ACTIONS = {	'MOVE_FORWARD': moveForward,
				'TURN_RIGHT': turnRight,
				'TURN_LEFT': turnLeft,
				'SHOOT_PROJECTILE': shootProjectile }

from math import cos, sin, radians

class Robot:
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
	
	xPosition = 0
	'''
	The x coordinate of the robot on the game board.Board.
	'''
	
	yPosition = 0
	'''
	The y coordinate of the robot on the game board.Board.
	'''

	health = 0
	'''
	The amount of health the robot has. Defaults to 
	'''
	
	thetaPosition = 0
	'''
	The orientation (rotation) of the robot.
	
	Measured in degrees (to allow for integral values),
	0 degrees faces positive x direction,
	rotation is anti-clockwise (maybe).
	'''
	
	name = None
	'''
	A string representing the name of the robot.
	
	The string must be unique within the game simulation to avoid collisions.
	If no string is provided to the constructor,
	one that is guaranteed to be unique will be generated. 
	'''
	
	image = None
	'''
	The image to use for graphical representations of the robot.
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

		@param health: The starting heald of the robot. Defaults to Robot::DEFAULT_HEALTH
		'''
		
		# set parameter values
		self.xPosition = x
		self.yPosition = y
		self.thetaPosition = theta
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
		action = self.script.decideAction(self, board)
		
		print("action taken by %s is %s" % (self.name, str(action)))
		
		action(self, board)

	def turnLeft(self, board):
		'''
		Rotate the robot 90 degrees to the left.
		'''
		self.thetaPosition = (self.thetaPosition + 90) % 360
	
	def turnRight(self, board):
		'''
		Rotate the robot 90 degrees to the right
		'''
		self.thetaPosition = (self.thetaPosition - 90) % 360

	def moveForward(self, board):
		'''
		Moves the robot forward one space in the current direction.
		If it runs into a wall, it will simply not move.
		
		@param board: A reference to the board object. This is used for checking bounds and collisions.
		'''
		newX = self.xPosition + cos(radians(self.thetaPosition))
		newY = self.yPosition + sin(radians(self.thetaPosition))
		
		# if board is infinite, no need to check against board.Board bounds
		if board.BOARD_SIZE > 0:
			if newX < 0 or newX >= board.BOARD_SIZE:
				return
			if newY < 0 or newY >= board.BOARD_SIZE:
				return
			
		# update position
		self.xPosition = newX
		self.yPosition = newY
	
	def drawArgs(self):
		'''
		Returns a dictionary with information on the robot's current position.
		
		@return: 
		'''
		return {
				"x":self.xPosition,
				"y": self.yPosition,
				"theta": self.thetaPosition
				}

	# Returns the string representation of the Robot (called whenever object is converted to string)
	
	def __str__(self):
		'''
		Returns the string representation of the Robot
		'''
		return "Robot %s at (%i, %i) facing %i degrees" % (
				self.name, self.xPosition, self.yPosition, self.thetaPosition)

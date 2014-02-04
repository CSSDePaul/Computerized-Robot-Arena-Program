from math import cos, sin, radians
import randomScript as script

class robot:
	xPosition = 0
	yPosition = 0
	thetaPosition = 0  # 0 degrees is facing positive x direction
	name = "robot"
	image = ""  # the image file to display as the robot

	# the constructor for the robot
	# x = starting x coordinate
	# y = starting y coordinate
	# t = starting angle (0 degrees is facing positive x, 90 is facing positive y)
	def __init__(self, x, y, t, Str):
		self.xPosition = x
		self.yPosition = y
		self.thetaPosition = t
		self.name = Str
	
	# Returns a string from boardState.MOVEFUNCTIONS.keys()
	# this is the action the agent decided to take
	# the human player uploads a script that is called by this action 
	def decideAction(self, boardState):
		return script.decideAction(boardState)

	# The robot first decides on an action to take, then executes the action
	def takeAction(self, boardState):
		action = self.decideAction(boardState)
		print("action taken by %s is %s" % (self.name, action))
		theAction = boardState.MOVEFUNCTIONS[action]  # maps string to function
		theAction(self, boardState)  # calls the appropriate function
	
	# The function called from takeAction
	# this function becomes a function corresponding to an action
	def theAction(self, boardState):  # is replaced when takeAction is called
		raise NotImplementedError

	def turnLeft(self, boardState):
		self.thetaPosition = (self.thetaPosition + 90) % 360
	
	def turnRight(self, boardState):
		self.thetaPosition = (self.thetaPosition - 90) % 360

	# moves forward one space in the appropriate direction
	# if it runs into a wall, it will simply not move
	def moveForward(self, boardState):
		newX = self.xPosition + cos(radians(self.thetaPosition))
		newY = self.yPosition + sin(radians(self.thetaPosition))
		if newX < 0 or newX >= boardState.BOARD_SIZE:
			return
		if newY < 0 or newY >= boardState.BOARD_SIZE:
			return
		self.xPosition = newX
		self.yPosition = newY
	
	# Returns a dictionary with the following information:
	# 	'x': the x coordinate
	# 	'y': the y coordinate
	# 	'a': the angle
	def drawArgs(self):
		return {"x":self.xPosition, "y": self.yPosition, "a": self.thetaPosition}

	# Returns the string representation of the robot (called whenever object is converted to string)
	def __str__(self):
		return "Robot %s at (%i, %i) facing %i degrees" % (\
				self.name, self.xPosition, self.yPosition, self.thetaPosition)

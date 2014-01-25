import random
from math import *

class robot:
	xPosition = 0
	yPosition = 0
	thetaPosition = 0
	name = "robot"
	
	def __init__(self, x, y, t, Str):
		self.xPosition = x
		self.yPosition = y
		self.thetaPosition = t
		self.name = Str
		
	def decideAction(self, boardState): #this is what is scripted by user
		return random.choice(list(boardState.MOVEFUNCTIONS.keys()))
		
	def takeAction(self, boardState):
		global theFunction
		action = self.decideAction(boardState)
		print("action taken by %s is %s"%(self.name, action))
		theFunction = boardState.MOVEFUNCTIONS[action]
		theFunction(self, boardState)	
		
	def theFunction(self, boardState): #is replaced when takeAction is called
		raise NotImplementedError

	def turnLeft(self, boardState):
		self.thetaPosition -= 90
	
	def turnRight(self, boardState):
		self.thetaPosition += 90

	def moveForward(self, boardState):
		newX = self.xPosition + sin(radians(self.thetaPosition))
		newY = self.yPosition + cos(radians(self.thetaPosition))
		if newX < 0 or newX >= boardState.BOARD_SIZE:
			return
		if newY < 0 or newY >= boardState.BOARD_SIZE:
			return
		self.xPosition = newX
		self.yPosition = newY

	def __str__(self):
		return "Robot %s at (%i, %i) facing %i degrees" %(\
				self.name, self.xPosition, self.yPosition, self.thetaPosition)

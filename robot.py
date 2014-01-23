
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
		
	def takeAction(self, boardState):
		move = 'forward'
		xVector = boardState.MOVEVECTORS[move][0]
		yVector = boardState.MOVEVECTORS[move][1]
		tVector = boardState.MOVEVECTORS[move][2]
		newX = self.xPosition + xVector
		newY = self.yPosition + yVector
		newT = self.thetaPosition + tVector
		if self.isValidMove(newX, newY, newT, boardState):
			self.xPosition = newX
			self.yPosition = newY
			self.thetaPosition = newT
		
	
	def isValidMove(self, x, y, t, boardState):
		if 	x < 0 or x >= boardState.BOARD_SIZE:
			return False
		if y < 0 or y >= boardState.BOARD_SIZE:
			return False
		return True		

	def __str__(self):
		return "Robot %s at (%i, %i) facing %i degrees" %(\
				self.name, self.xPosition, self.yPosition, self.thetaPosition)

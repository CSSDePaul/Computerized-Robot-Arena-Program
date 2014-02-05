from robot import Robot

class boardState:
	BOARD_SIZE = 10
	MOVEFUNCTIONS = {	'turnLeft':	 	robot.turnLeft,
						'turnRight': 	robot.turnRight,
						'moveForward':	robot.moveForward,
					}
	Players = []  # the list of robot objects
	DisplayMatrix = [] # 2D started in init. indexed in row major order
	
	# the constructor. Initializes robots to add to boardState
	def __init__(self):
		self.Players.append(robot(0, 0, 0, "Robot0"))

		for i in range(self.BOARD_SIZE):
		    self.DisplayMatrix.append([])
		    for j in range(self.BOARD_SIZE):
		    	self.DisplayMatrix[i].append("X")

	# updates positions of all objects
	def update(self):
		for player in self.Players:
			player.takeAction(self)
			print(player)

	def display(self):
		outputString = ""
		
		for row in self.DisplayMatrix:
			for col in row:
				outputString += col
			print(outputString)
			outputString = ""
				
		
		
		
		
		
		
		
		
		
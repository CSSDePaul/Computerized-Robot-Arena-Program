from robot import robot

class boardState:
	BOARD_SIZE = 10
	MOVEFUNCTIONS = {'turnLeft':	 robot.turnLeft,
				'turnRight': robot.turnRight,
				'moveForward':   robot.moveForward,
				}
	Players = []
	
	def __init__(self):
		self.Players.append(robot(0,0,0, "Robot0"))
	
	def update(self):
		for player in self.Players:
			player.takeAction(self)
			print(player)

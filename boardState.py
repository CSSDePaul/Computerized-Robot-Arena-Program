from robot import robot

class boardState:
	BOARD_SIZE = 10
	MOVES = ['turnleft', 'turnright', 'forward']
	MOVEVECTORS = {'turnleft':	 (0, 0, -90), #(x, y, t)
				'turnright': (0, 0, 90),
				'forward':   (0, 1, 0),
				}
	Players = [None, None]
	
	def __init__(self):
		self.Players[0] = robot(0,0,0, "Robot0")
		self.Players[1] = robot(1,1,0, "Robot1")
	
	def update(self):
		for player in self.Players:
			player.takeAction(self)
			print(player)

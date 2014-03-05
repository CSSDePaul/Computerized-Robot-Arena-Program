
class robotBehavior:

	# Returns a string from Board.MOVEFUNCTIONS.keys()
	# this is the action the agent decided to take
	# the human player uploads a script that is called by this action 
	def decideAction(self, robot, board, actions):
		'''
		Returns the alias to a random movement function in the robot class
		'''
		print("Possible moves: ")
		for i in range(len(actions)):
			print("%s: %s"%(i, actions[i]))
		choice = None
		while choice == None: #until valid input
			choice = input("Input number corresponding to action:")
			try:
				choice = actions[int(choice)]
			except:
				print("Invalid input. Type a number between 0 and %s"%(len(actions)))
				choice = None #causes while loop to continue
		return choice
		
	def __init__(self):
		pass

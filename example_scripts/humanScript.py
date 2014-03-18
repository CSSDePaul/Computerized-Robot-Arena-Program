
class robotBehavior:

	def decideAction(self, robot, board, actions):
		'''
		Returns a human-chosen string from Board.MOVEFUNCTIONS.keys()
		this is the action the agent decided to take
		'''
		print("Possible moves: ")
		for i in range(len(actions)):
			print("{}: {}".format(i, actions[i]))
		choice = None
		while choice == None: #until valid input
			choice = input("Input number corresponding to action:") #should be a number from 0 to len(actions)
			try:
				choice = actions[int(choice)] #the string representing the action to be taken
			except:
				print("Invalid input. Type a number between 0 and {}".format(len(actions)))
				choice = None #causes while loop to continue
		return choice
		
	def __init__(self):
		pass

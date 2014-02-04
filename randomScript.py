import random

# Returns a string from boardState.MOVEFUNCTIONS.keys()
# this is the action the agent decided to take
# the human player uploads a script that is called by this action 
def decideAction(boardState):
	return random.choice(list(boardState.MOVEFUNCTIONS.keys()))

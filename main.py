from board import Board
from graphics import Graphics

from randomScript import randomScript # shitty hard-coded include for testing

def main():
	
	# create list of behaviors
	behaviors = [ randomScript(), randomScript() ]
	
	# instantiate Board object
	gameBoard = Board(behaviors)
	
	# instantiate Graphics object
	display = Graphics(gameBoard, 250)
	
	# start simulation
	display.start()
	
if __name__ == "__main__":
	main()

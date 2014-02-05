from board import Board
from graphics import Graphics

def main():
	theBoard = Board()
	display = Graphics(theBoard)
	display.start()
	
if __name__ == "__main__":
	main()

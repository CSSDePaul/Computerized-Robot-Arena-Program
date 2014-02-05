from board import Board
from graphics import Graphics

def main():
	gameBoard = Board()
	display = Graphics(gameBoard, 250)
	display.start()
	
if __name__ == "__main__":
	main()

from boardState import boardState

def main():
	theBoard = boardState()
	for i in range(20):
		theBoard.update()
	
if __name__ == "__main__":
	main()

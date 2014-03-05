class Actor:
	'''
	A class representing any items which can be placed on the board.
	'''

	xPosition = 0
	'''
	The x coordinate of the actor on the board.
	'''
	
	yPosition = 0
	'''
	The y coordinate of the actor on the board.
	'''

	rotation = 0
	'''
	The rotation of the actor.
	
	Measured in degrees (to allow for integral values),
	0 degrees faces positive x direction,
	rotation is anti-clockwise (maybe).
	'''
	
	name = None
	'''
	A string representing the name of the actor.
	
	The string must be unique within the game simulation to avoid collisions.
	If no string is provided to the constructor,
	one that is guaranteed to be unique will be generated. 
	'''
	
	image = None
	'''
	The image to use for graphical representations of the actor.
	'''

	def __init__(self, x, y, rotation, name = None, image = None):
		self.xPosition = x
		self.yPosition = y
		self.rotation = rotation
		self.name = name
		self.image = image
Computerized-Robot-Arena-Program
================================

CRAP is a competitive coding challenge which has two or more coders write the behavior code for robots on a field of battle.

Latest Release: [v0.1.3](https://github.com/CSSDePaul/Computerized-Robot-Arena-Program/releases/tag/v0.1.3)

With the release of v0.1.0 the game is now runable from the command line (no graphical interface yet, learn to use the CLI you NUB). To have two scripts duke it out, navigate to the directory containing the Computerized-Robot-Arena-Program directory and your two scripts, and run `python Computerized-Robot-Arena-Program script1.py script2.py`. 

**Note**: CRAPpy requires python 3.3+, so you might have to run `python3.3 Computerized-Robot-Arena-Program script1.py script2.py` depending on your local python install.

![](http://i.imgur.com/cK0tYOY.png)

## Writing Scripts

The basic structure of a robot behavior script is as follows:

```python
class robotBehavior:

	def decideAction(self, robot, board, actions):
		'''
		Returns one of the elements in actions.
		'''
		
		chosen_action = 0
		
		# some logic to choose the action you want
		
		return actions[chosen_action]
		
	def __init__(self):
		pass
```

Behavior scripts have to be wrapped in a class called `robotBehavior` and have a function `decideAction` which takes in the object representing the robot, an object representing the board, and a list with strings representing the acations the robot are allowed to take. `decideAction` should be the element of _actions_ representing the action you want the robot to take.

### Actions

The robots can take the following actions:

* **Move Forward** (MOVE_FORWARD) - The robot moves one space in the direction its currently facing.
* **Turn Left** (TURN_LEFT) - The robot turns 90 degrees to the left (anti-clockwise).
* **Turn Right** (TURN_RIGHT) - The robot turns 90 degrees to the right (clockwise).
* **Fire Projectile** (FIRE_PROJECTILE) - The robot fires a projectile directly in front of itself, moving in the direction the robot is facing.

### Example Scripts

CRAPpy comes with several example scripts used for testing and debugging which define very basic strategies and give examples of how to use the API to write behavioral scripts. Here are a few:

#### randomScript.py

This script randomly chooses one of the available options.

```python
import random

class robotBehavior:

	# Returns a string from Board.MOVEFUNCTIONS.keys()
	# this is the action the agent decided to take
	# the human player uploads a script that is called by this action 
	def decideAction(self, robot, board, actions):
		'''
		Returns the alias to a random movement function in the robot class
		'''
		return random.choice(actions)
		
	def __init__(self):
		pass
```

#### smartRandomScript.py

smartRandomScript is an improvement over randomScript, which won't suicidally walk into an occupied space.

```python
import random
import utility

class robotBehavior:

	# Returns a string from Board.MOVEFUNCTIONS.keys()
	# this is the action the agent decided to take
	# the human player uploads a script that is called by this action 
	def decideAction(self, robot, board, actions):
		'''
		Returns the alias to a random movement function in the robot class
		'''
		
		choice = random.choice(actions)
		if (choice == 'MOVE_FORWARD'):
			
			forwardLoc = utility.forwardCoords(robot.xPosition, robot.yPosition, robot.rotation, board)
			
			isOccupied = board.occupied(forwardLoc[0],forwardLoc[1])
			if (isOccupied is None):
				#space in front is outside the board
				return 'TURN_RIGHT'
			if (isOccupied):
				#if something is in front, shoot at it
				return 'SHOOT_PROJECTILE'
			else:
				#if something isn't in front, move forward
				return 'MOVE_FORWARD'
		
		return choice
		
	def __init__(self):
		pass
```

#### directWalk.py

This robot picks the first other robot on the field and walks into it so that both of them are destroyed.

```python
'''
Created on Mar 12, 2014

@author: excaliburhissheath
'''

from utility import forwardCoords, manhattanDistance

class robotBehavior:
    '''
    A behavior that make the robot walk in a straight line towards the closest robot.
    '''

    def decideAction(self, robot, board, actions):
        '''
        Walks towards the other robot and tries to run into it.
        '''
        
        # get the list of robots from the board
        robots = board.getRobots()
        robotKeys = list(robots.keys())
        
        # temporary hacky workaround
        # get the other robot (future versions should find the closest robot)
        closest = robots[robotKeys[0]]
        
        # if first robot is this robot, get second robot
        if robotKeys[0] == robot.name:
            closest = robots[robotKeys[1]]
        
        # get current distance to target robot
        currentDistance = manhattanDistance(robot, closest)
        
        # get coordinates of space in front of robot
        forwardPos = forwardCoords(robot.xPosition, robot.yPosition, robot.rotation)
        
        # get distance of forwardPos from target
        forwardDistance = manhattanDistance(forwardPos, closest)
        
        # if forward gets robot closer to target, move forward
        if forwardDistance < currentDistance:
            return 'MOVE_FORWARD'
        # otherwise turn right
        else:
            return 'TURN_RIGHT'

    def __init__(self):
        pass
```

## More Information

For more information see [the wiki](https://github.com/CSSDePaul/Computerized-Robot-Arena-Program/wiki).

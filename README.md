Computerized-Robot-Arena-Program
================================

CRAP is a competitive coding challenge which has two or more coders write the behavior code for robots on a field of battle.

## v0.0.1

v0.0.1 is out!

With the release of v0.0.1 the game is now runable from the command line (no graphical interface yet, learn to use the CLI nub). To have two scripts duke it out, navigate to the directory containing the Computerized-Robot-Arena-Program directory, and run `python3.3 Computerized-Robot-Arena-Program script1.py script2.py`

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
		
		...
		
		return actions[0]
		
	def __init__(self):
		pass

```

Behavior scripts have to be wrapped in a class called `robotBehavior` and have a function `decideAction` which takes in the object representing the robot, an object representing the board, and a list with strings representing the acations the robot are allowed to take. `decideAction` should be the element of _actions_ representing the action you want the robot to take.

## Actions

The robots can take the following actions:

* **Move Forward** - The robot moves one space in the direction its currently facing.
* **Turn Left** - The robot turns 90 degrees to the left (anti-clockwise).
* **Turn Right** - The robot turns 90 degrees to the right (clockwise).
* **Fire Projectile** - The robot fires a projectile directly in front of itself, moving in the direction the robot is facing.

## More Information

For more information see [the wiki](https://github.com/CSSDePaul/Computerized-Robot-Arena-Program/wiki).

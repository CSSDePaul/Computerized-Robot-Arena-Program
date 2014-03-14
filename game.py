'''
Created on Mar 13, 2014

@author: excaliburhissheath
'''

from board import Board
'''
Import the Board class.
'''

from graphics import Graphics
'''
Import Graphics class.
'''

import utility
'''
Import utility module for decay functionality.
'''

import time
'''
Used to cause delay for graphics.
'''

class Game:
    '''
    A runner class to run one full full game.
    
    The Game class is customizable in the following ways:
    * maximumRounds - The absolute maximum number of rounds to be played in the game before a tie is declared, defaults to 250. A value of 0 means that there is no maximum number of rounds.
    * minimumRounds - The minimum number of rounds to be run when doing decay ending, defaults to 0.
    * decay - The probability of any given round taking place, defaults to 1.
    
    @note: A decay of .01 give an expected length of ~100 rounds. Decay calculations do not begin until after minimumRounds rounds have passed.
    '''

    maximumRounds = 250
    '''
    The maximum number of rounds in the game. A value of 0 means there is no maximum number of rounds.
    '''
    
    decay = 1
    '''
    The decay rate of of the program of the program, i.e. the probability that the current round is the last round.
    
    @note: A decay of .01 give an expected length of ~100 rounds. Decay calculations do not begin until after minimumRounds rounds have passed.
    '''
    
    minimumRounds = 0
    '''
    The minimum number of rounds in the game.
    
    @note: This is the number of rounds that are run before the decay logic is applied to determine the end of the game.
    '''
    
    numRounds = 0
    '''
    The number of rounds so far.
    '''
    
    graphics = None
    '''
    The Graphics object used for displaying the game.
    
    If the value is None, then no graphics are displayed.
    '''
    
    board = None
    '''
    The Board object for the game.
    '''
    
    gameOver = False
    '''
    Flag indicating whether the game is done or not.
    '''

    def __init__(self, scripts, useGraphics = False, maximumRounds = 250, decay = 1, minimumRounds = 0):
        '''
        Constructor for Game class.
        
        @param scripts: A list of RobotBehavior objects defining the robots in the game.
        @param graphics: The Graphics object being used to render the graphics object. If graphics is None, no graphical display will be done.
        '''
        
        # ====================
        # INITIALIZE VARIABLES
        # ====================
        
        # initialize passed in variables
        self.maximumRounds = maximumRounds
        self.decay = decay
        self.minimumRounds = minimumRounds
        
        
        
        # initialize numRounds
        self.numRounds = 0
        
        # =========================
        # CREATE BOARD AND GRAPHICS
        # =========================
        
        self.board = Board(scripts)
        
        # if graphics are being used, initialize graphics
        if useGraphics: 
            self.graphics = Graphics(self.board, 500)
        
    def run(self):
        '''
        Runs the game simulation and returns the winner.
        '''
        
        # reset important variables
        self.numRounds = 0
        self.gameOver = False
        
        # ==============
        # START GRAPHICS
        # ==============
        
        # if graphics not None, start graphics runner
        if not (self.graphics is None):
            self.graphics.start()
            
        # ========
        # RUN GAME
        # ========
        
        # This loop runs the logic for each round,
        # rounds continue until one of the end game conditions are met.
        while not self.gameOver:
            
            print('\nGAME ROUND #{}'.format(self.numRounds))
            
            # ============================
            # TEST FOR END GAME CONDITIONS
            # ============================
            
            if self.maximumRounds > 0 and self.numRounds >= self.maximumRounds:         # round limit reached
                self.gameOver = True
                print('Round Limit Reached')
            elif self.numRounds >= self.minimumRounds and not utility.decay(self.decay):    # decay termination
                self.gameOver = True
                print('Decay Limit Reached')
            elif len(self.board.getRobots()) <= 1:                                       # one or fewer robots left
                self.gameOver = True
                print('Only {} robots left'.format(len(self.board.getRobots())))
            elif self.graphics is not None and self.graphics.exitFlag:
                self.gameOver = True
                print('Graphics Window Closed')
                
            # ===============
            # PERFORM UPDATES
            # ===============
            
            # update board    
            self.board.update()
            
            # update graphics and delay if necessary
            if not (self.graphics is None):
                self.graphics.update()
                
                if (self.graphics.delay > 0):
                    time.sleep(self.graphics.delay / 1000)  # Graphics.delay is in miliseconds, time.sleep() takes seconds
                
            # increment number of rounds
            self.numRounds += 1
        
        # =================
        # END OF GAME LOGIC
        # =================
        
        returnval = ''
        
        # if 1 or 0 robots left, end game
        if len(self.board.getRobots()) == 1:
            
            # Only one robot left, that robot is the winner
            # print out winner and exit

            # print winner
            print("A winner is " + list(self.board.getRobots().keys())[0])

            # return name of winning robot
            returnval = list(self.board.getRobots().keys())[0]
        elif len(self.board.getRobots()) < 1:
            
            # no robots left,
            # declare game a tie
            
            # print tie
            print("The game is a tie, everyone is dead.")
            
            # return tie
            returnval = 'TIE'
        elif len(self.board.getRobots()) > 1:
            
            # multiple robots left, declare a tie
            print("multiple robots left: {}".format(list(self.board.getRobots().keys())))
            
            returnval = 'TIE'
            
        # kill graphics
        self.graphics.exit()
            
        # return result
        return returnval


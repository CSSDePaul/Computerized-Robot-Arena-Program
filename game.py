'''
Created on Mar 13, 2014

@author: excaliburhissheath
'''

from board import Board
''' Import the Board class. '''

from graphics import Graphics
''' Import Graphics class. '''

import utility
''' Import utility module for decay functionality. '''

import time
''' Import time module, used to cause delay for graphics. '''

import copy
''' Import copy module, used to pass copies of the board to the graphics class. '''

import logging
''' Import logging module. '''

DEFAULT_MAXIMUM_ROUNDS = 250

class Game:
    '''
    A runner class to run one full full game.
    
    The Game class is customizable in the following ways:
    * maximumRounds - The absolute maximum number of rounds to be played in the game before a tie is declared, defaults to 250. A value of 0 means that there is no maximum number of rounds.
    * minimumRounds - The minimum number of rounds to be run when doing decay ending, defaults to 0.
    * decay - The probability of any given round taking place, defaults to 1.
    
    @note: A decay of .01 give an expected length of ~100 rounds. Decay calculations do not begin until after minimumRounds rounds have passed.
    '''

    maximumRounds = 0
    ''' The maximum number of rounds in the game. A value of 0 means there is no maximum number of rounds. '''
    
    decay = 1
    '''
    The decay rate of the game, i.e. the probability that the next round will take place.
    
    @note: A decay of .99 gives an expected length of ~100 rounds, which is a reasonable default value for a game.
    Decay calculations do not begin until after minimumRounds rounds have passed.
    '''
    
    minimumRounds = 0
    '''
    The minimum number of rounds in the game.
    
    @note: This is the number of rounds that are run before the decay logic is applied to determine the end of the game.
    '''
    
    numRounds = 0
    ''' The number of rounds so far. '''
    
    graphics = None
    '''
    The Graphics object used for displaying the game.
    
    If the value is None, then no graphics are displayed.
    '''
    
    synchronizeGraphics = False
    ''' Flag used to indicate whether the game update loop should synchronize with the graphics or not. '''
    
    board = None
    ''' The Board object for the game. '''
    
    gameOver = False
    ''' Flag indicating whether the game is done or not. '''
    
    scripts = None
    ''' Stash of scripts used for re-running the game. '''

    def __init__(self, scripts, useGraphics = False, synchronizeGraphics = False, maximumRounds = DEFAULT_MAXIMUM_ROUNDS, decay = 1, minimumRounds = 0):
        '''
        Constructor for Game class.
        
        @param scripts: A dict of robotBehavior objects keyed to the script's name.
        @param useGraphics: The Graphics object being used to render the graphics object. If graphics is None, no graphical display will be done.
        @param synchronizeGraphics: If graphics are being used, making this True will cause the game loop to update at the same rate as the graphics loop,
        rather than running as fast as it can. This is available for debugging purposes.
        @param maximumRounds: The maximum number of rounds in the game.
        @param decay: The decay rate of the game, i.e. the probability that the next round will take place.
        @param minimumRounds: The minimum number of rounds in the game.
        '''
        
        # ====================
        # INITIALIZE VARIABLES
        # ====================
        
        # initialize passed in variables
        self.maximumRounds = maximumRounds
        self.decay = decay
        self.minimumRounds = minimumRounds
        self.scripts = scripts
        
        # if graphics are being used, initialize graphics
        if useGraphics: 
            self.graphics = Graphics()
            self.synchronizeGraphics = synchronizeGraphics
        
    def run(self):
        '''
        Runs the game simulation and returns the winner.
        
        @return: A list containing the names of all the robots that survived the round.
        '''
        
        # reset important variables
        self.numRounds = 0
        self.gameOver = False
        self.board = Board(self.scripts)
        
        # ==============
        # START GRAPHICS
        # ==============
        
        # if graphics not None, start graphics runner
        if not (self.graphics is None):
            
            # give graphics object initial board state
            self.graphics.update(copy.deepcopy(self.board))
            
            # start graphics thread
            self.graphics.start()
            
        # ========
        # RUN GAME
        # ========
        
        # This loop runs the logic for each round,
        # rounds continue until one of the end game conditions are met.
        while not self.gameOver:
            
#             logging.debug('\nGAME ROUND #{}'.format(self.numRounds))
            
            # ============================
            # TEST FOR END GAME CONDITIONS
            # ============================
            
            if self.maximumRounds > 0 and self.numRounds >= self.maximumRounds:             # round limit reached
                self.gameOver = True
#                 logging.debug('Round Limit Reached')
            elif self.numRounds >= self.minimumRounds and not utility.decay(self.decay):    # decay termination
                self.gameOver = True
#                 logging.debug('Decay Limit Reached')
            elif len(self.board.getRobots()) <= 1:                                          # one or fewer robots left
                self.gameOver = True
                logging.debug('{} robot(s) left'.format(len(self.board.getRobots())))
            elif self.graphics is not None and self.graphics.exitFlag:                      # graphics window closed
                self.gameOver = True
#                 logging.debug('Graphics Window Closed')
                
            # ===============
            # PERFORM UPDATES
            # ===============
            
            # update board    
            self.board.update()
            
            # update graphics and delay if necessary
            if self.graphics is not None:
                self.graphics.update(copy.deepcopy(self.board))
                
                if self.synchronizeGraphics:
                    time.sleep(self.graphics.delay / 1000)  # Graphics.delay is in miliseconds, time.sleep() takes seconds
                
            # increment number of rounds
            self.numRounds += 1
        
        # =================
        # END OF GAME LOGIC
        # =================
        
        # if 1 or 0 robots left, end game
        if len(self.board.getRobots()) == 1:
            
            # Only one robot left, that robot is the winner
            # print out winner and exit

            # print winner
            logging.info("A winner is " + list(self.board.getRobots().keys())[0])
        elif len(self.board.getRobots()) < 1:
            
            # no robots left,
            # declare game a tie
            
            # print tie
            logging.info("The game is a tie, everyone is dead.")
        elif len(self.board.getRobots()) > 1:
            
            # multiple robots left, declare a tie
            logging.info("multiple robots left: {}".format(list(self.board.getRobots().keys())))
        
        # kill graphics
#         self.graphics.exit()
            
        # return result
        return self.board.getRobots()


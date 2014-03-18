'''
Created on Mar 16, 2014

@author: excaliburhissheath
'''

from game import Game
''' Import game runner class. '''

import logging
''' Import logging module. '''

import utility
''' Import utility module for decay logic. '''

DEFAULT_MAXIMUM_GAMES = 100
''' The default maximum number of games in a set. '''

DEFAULT_DECAY = 0.98
''' The default decay rate for a set. '''

DEFAULT_MINIMUM_GAMES = 25
''' The default minimum number of games in a set. '''

class Set:
    '''
    A runner class for running one full set.
    
    The Set class is customizable in the following ways:
    * maximumGames - The absolute maximum number of games to be played in the game before a tie is declared, defaults to 250. A value of 0 means that there is no maximum number of games.
    * minimumRounds - The minimum number of games to be run when doing decay ending, defaults to 0.
    * decay - The probability of any given game being run, defaults to 1.
    
    @note: A decay of .02 give an expected length of ~50 games. Decay calculations do not begin until after minimumRounds rounds have passed.
    '''

    maximumGames = 0
    ''' The maximum number of games in the set. '''
    
    minimumGames = 0
    '''
    The minimum number of games in the set.
    
    @note: minimumGames is the number of games run before decay logic is applied.
    '''
    
    decay = 0
    '''
    The decay rate of of the set, i.e. the probability that the next game will take place.
    
    @note: A decay of .98 gives an expected length of ~50 rounds, which is a reasonable default value for a set.
    Decay calculations do not begin until after minimumRounds game have passed.
    '''
    
    scoreBoard = None
    '''
    A dict holding the scores for each of the bots in the game.
    
    The values stored in the score board are the number of games each robot survived,
    keyed to the name of the robot as defined in the scripts dict passed in at construction.
    '''
    
    gameRunner = None
    ''' A game object used to run each game in the set. '''

    def __init__(self, scripts, maximumGames = DEFAULT_MAXIMUM_GAMES, decay = DEFAULT_DECAY, minimumGames = DEFAULT_MINIMUM_GAMES, noBlock = False, gameConfig = None):
        '''
        Constructor for Set class.
        
        @param scripts: A dict of robotBehavior objects keyed to the script's name.
        @param maximumGames: The maximum number of games in the set.
        @param decay: The decay rate of the set.
        @param minimumGames: The minimum number of games in the set.
        @param noBlock: If noBlock is set to false, the set will be run upon construction of the Set object,
        and the results will be available immediately. As this has the potential to cause blocking, setting noBlock to True will
        have the Set object wait until run() is called explicitly to run the simulation. Defaults to False.
        @param gameConfig: A dict holding the configuration values for the game runner. If not provided, default values will be used.
        '''
        
        # ====================
        # INITIALIZE VARIABLES
        # ====================
        
        # initialize passed in variables
        self.maximumGames = maximumGames
        self.minimumGames = minimumGames
        self.decay = decay
        
        # initialize score board
        self.scoreBoard = {}
        for script_name in scripts:
            self.scoreBoard[script_name] = 0
            
        # initialize game runner
        self.gameRunner = Game(scripts) # TODO add configuration options
        
        if not noBlock:
            self.run()
    
    def run(self):
        '''
        Runs the set and stores the results in Set.scoreBoard
        
        @note: Unlike in the game runner, run() in Set does NOT reset scoring values,
        so calling run() twice would mean that the results of two sets will be represented within
        Set.scoreBoard. This is potentially useful in the case that running a single set is inconclusive.
        '''
        
        # ====================
        # INITIALIZE VARIABLES
        # ====================
        
        numGames = 0
        setOver = False
        
        # =======
        # RUN SET
        # =======
        
        while not setOver:
            
            # ===========================
            # TEST FOR END SET CONDITIONS
            # ===========================
            
            if numGames >= self.maximumGames:
                setOver = True
                logging.info('Game Limit Set Termination')
                continue
            elif numGames >= self.minimumGames and not utility.decay(self.decay):
                setOver = True
                logging.info('Set Decay Termination')
                continue
            
            logging.info('\nGAME #{}'.format(numGames))
            
            # ========
            # RUN GAME
            # ========
            
            # run game and get results
            results = self.gameRunner.run()
            
            logging.debug(results)
            
            # update score board with results
            for script_name in results:
                logging.debug('{} survived game #{}'.format(script_name, numGames))
                self.scoreBoard[script_name] += 1
                
            numGames += 1
        
        logging.info(self.scoreBoard)
            
        
        
        
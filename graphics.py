'''
Created on Feb 4, 2014

@author: excaliburhissheath
'''

from tkinter import *

class Graphics:
    '''
    A wrapper class to perform all graphical functions and run the main loop of the simulation.
    
    An object representing the board is provided, and a delay is given to 
    '''
    
    tk_root = None
    graphics = None
    
    board = None
    ''' Object representing the current state of the game board. '''
    
    delay = 0
    ''' The interval between updates of the board (in miliseconds). '''

    def __init__(self, board, delay = 0):
        '''
        Constructor. It constructs stuff.
        '''
        
        # assign parameter values
        self.board = board;
        self.delay = delay;
        
        # initialize tk_root
        self.tk_root = Tk()
        
        self.canvas = Canvas(self.tk_root)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        
    def redraw_board(self):
        '''
        Update board, then redraw it.
        '''
        
        print(self.delay)
        
        # update board
        self.board.update();
        
        # redraw all robots
        
        
        # reschedule update
        self.tk_root.after(self.delay, self.redraw_board)
        
    def start(self):
        '''
        start the canvas's main loop
        '''
        self.tk_root.after(self.delay, self.redraw_board)
        self.tk_root.main_loop()

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 21:21:04 2021

@author: comim
"""
import numpy as np
from utils import *

class Player:
    def __init__(self, index):
        self.index = index
        assert self.index != 0, "The player index cannot be 0"
        
    def __str__(self):
        return f'Player {self.index}'     
    
            
class Human(Player):
    def __init__(self):
        """ Create Human player. Human's index is 2. """
        super().__init__(2)       

    def get_action_from_mouse(self, game, mouse_pos):
        """
        Convert the mouse position into the board position, the image position, and the action 
        as integer. 
        The mouse position represents the position on the screen, and has a range between (0, 0) 
        and (width, height).
        The board position represents the position of the cell on the board, and ranges between
        (0,0) and (2, 2).
        The image position represents the starting point on the screen where the image needs to be
        placed.
        """       
        board_pos = []
        img_pos = []
        dicts = [game.dict_row.items(), game.dict_col.items()]
        indexes = [0, 1]    # 0: rows, 1: cols
        for index in indexes:
            for key, values in dicts[index]:
                if (mouse_pos[index] >= values[0]) and (mouse_pos[index] <= values[1]):
                    board_pos.append(key)
                    img_pos.append(values[0])
                    break 
        action = cell_to_index(board_pos)
        return board_pos, img_pos, action
    
    def choice(self, mouse_pos, game):
        """
        Player chooses an action. The action is a position between [0, 0] and [2, 2].
        """       
        board_pos, img_pos, action = self.get_action_from_mouse(game, mouse_pos)
        if game.check_available_action(action=action, board=game.board):
            game.board[action] = self.index
            game.draw_action(img_pos, 'img/cross.png', board_pos, img_pos)             
            game.game_won(player=self, board=game.board)
            game.turn -= 1        
        else:
            print('You cannot choose this cell')
    
    def next_player(self):
        player = Computer()
        return player
                      
        
class Computer(Player):
    def __init__(self):
        """ Create Computer player. Computer's index is 1. """
        super().__init__(1)

    def choice(self, game):
        """
        Player chooses an action. The action is an integer between 0 and 8.
        """        
        action = np.random.choice(game.get_available_actions(board=game.board))
        game.board[action] = self.index
        game.draw_action(action, 'img/circle.png')
        game.game_won(player=self, board=game.board)
        game.turn += 1   
    
    def next_player(self):
        player = Human()
        return player
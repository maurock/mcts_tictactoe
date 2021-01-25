# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 21:20:17 2021

@author: comim
"""
import pygame
import numpy as np
from utils import *
from player import Computer, Human, Player

class Game:
    def __init__(self, display_option=True):
        self.height = 400
        self.width = 400
        self.gameDisplay = pygame.display.set_mode([self.height, self.width])
        self.bg = pygame.transform.scale(pygame.image.load('img/bg.png'), (self.height, self.width))
        self.board = np.zeros(9)
        self.running = True
        self.display_option = display_option
        if self.display_option:
            self.screen_update()
        self.dict_row = {0: [0, self.height / 3],
                         1: [self.height / 3, 2 / 3 * self.height],
                         2: [2 / 3 * self.height, self.height]}
        self.dict_col = {0: [0, self.width / 3],
                         1: [self.width / 3, 2 / 3 * self.width],
                         2: [2 / 3 * self.width, self.width]}
        self.turn = 0
        #self.dict_cell = self.dict_action_to_cell()
        
    def draw_action(self, action, image_path, board_pos=None, img_pos=None):
        if board_pos is None:
            board_pos = index_to_cell(action) 
            img_pos = [self.dict_row[board_pos[1]][0], self.dict_col[board_pos[0]][0]]
        mark = pygame.transform.scale(pygame.image.load(image_path),
                                      (int(self.height / 3), int(self.width / 3)))
        self.gameDisplay.blit(mark, (img_pos[0], img_pos[1]))    
        pygame.display.update()      
  
    def get_available_actions(self, board):            
        return np.where(board == 0)[0]   # return only the actions
    
    def check_available_action(self, board, action):
        return board[action] == 0
        
    def screen_update(self):        
        self.gameDisplay.blit(self.bg, (0, 0))
        pygame.display.update()
    
    def game_won(self, board, player):
        """
        Return the score of game, and set game.running = False if the game is done.
        The score is a dictionary, where the key '1' is the score of the Computer, and key '2' is 
        the score of the Human. The winning player receives a score equal to 1, otherwise 0.
        """
        # Diagonals        
        score = {'1': 0, '2': 0}    # index 1 is Computer, index 2 is Human
        if (board[0] == board[4] == board[8] and board[0] != 0) or \
           (board[2] == board[4] == board[6] and board[2] != 0):            
            self.running = False
        # Rows and cols
        for i in range(0, 3):
            if (board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] and board[i * 3] != 0) or \
               (board[i] == board[i + 3] == board[i + 6] and board[i] != 0):
                self.running = False
        if self.running is False:  # game won!
            if self.display_option:
                pygame.time.wait(1000)                     
                myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)
                text_won = myfont_bold.render(f'PLAYER {player.index} WON', True, (0, 0, 0))             
                self.gameDisplay.fill([255, 255, 255])
                self.gameDisplay.blit(text_won, (120, 180))
                pygame.display.update()
                pygame.time.wait(1000)                       
                print(f'{player} won!')
            if isinstance(player, Computer):
                score['1'] = 1
                score['2'] = -1
            else:
                score['1'] = -1
                score['2'] = 1
        elif self.running and len(self.get_available_actions(board=board)) == 0:     # draw
            if self.display_option:
                pygame.time.wait(1000)                     
                myfont_bold = pygame.font.SysFont('Segoe UI', 20, True)
                text_won = myfont_bold.render(f'DRAW', True, (0, 0, 0))             
                self.gameDisplay.fill([255, 255, 255])
                self.gameDisplay.blit(text_won, (160, 180))
                pygame.display.update()
                pygame.time.wait(1000)                       
                print(f'draw')
            self.running = False
        return score
    
    def select_first_player(self, player):
        select_player = pygame.transform.scale(pygame.image.load('img/first_player.png'), (self.height, self.width))
        self.gameDisplay.blit(select_player, (0, 0))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                # Did the user click the window close button?
                if event.type == pygame.QUIT:
                    print('Game closed')
                    game.running = False  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos() 
                    if mouse_pos[0] < self.width / 2:
                        self.screen_update()
                        return player[1].index
                    elif mouse_pos[0] > self.width / 2:
                        self.screen_update()
                        return player[0].index

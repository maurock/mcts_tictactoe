# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 16:42:43 2021

@author: Mauro Comi
"""
import numpy as np
import pygame
import random
from utils import *
from player import *
from game import *
from mcts import *
import logging
pygame.init()
           
def play(mcts_mode):    
    game = Game() 
    player = [Computer(), Human()]
    index = game.select_first_player(player)
    game.turn = index
    mcts = MCTS()
    print(f'You are Player {player[1].index}')
    while game.running:        
        # Computer turn
        if game.turn == player[0].index:   
            if mcts_mode == True:
                mcts.choice(player[0], game)
            else:
                player[0].choice(game)
        # Human turn    
        for event in pygame.event.get():
            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                print('Game closed')
                game.running = False
            if event.type == pygame.KEYDOWN:
                action = event.unicode
                player[1].choice(action, game)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.turn == player[1].index:
                    mouse_pos = pygame.mouse.get_pos()                    
                    player[1].choice(mouse_pos, game)
    logging.shutdown()
    pygame.quit()
 
    
if __name__ == '__main__':    
    mcts_mode = True
    play(mcts_mode)
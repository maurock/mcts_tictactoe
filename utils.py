# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 21:13:44 2021

@author: Mauro Comi

Utility functions
"""


def index_to_cell(index):
    row = int(index / 3)
    col = index % 3
    return [row, col]  
    

def cell_to_index(board_pos):
    return board_pos[0] + board_pos[1] * 3

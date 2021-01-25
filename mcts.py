# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 18:11:10 2021

@author: comim
"""
import numpy as np
import math 
from utils import *
import copy
from game import Game
from player import Computer, Human, Player
import random
import logging
logging.basicConfig(level=logging.DEBUG, filename="test.log")

class Node:
    def __init__(self, state, player_index):
        self.state_visits = 0
        self.wins = 0
        self.state = state
        self.ucb = math.inf
        self.children_states = []
        self.player_index = player_index      
    
    def add_visit(self):
        self.state_visits += 1
    
    def compute_ucb(self, parent_state_visits, tree):
        if self.state_visits == 0:
            self.ucb = math.inf
        else:
            self.ucb = self.wins / self.state_visits + math.sqrt(2 * math.log(parent_state_visits) / self.state_visits)
        
        
class MCTS:
    def __init__(self):
        self.tree = None
        self.game = None
        self.max_counter = 500
        
    def add_node(self, node):
        self.tree[tuple(node.state)] = node
        
    def get_node(self, node_state):
        return self.tree[tuple(node_state)]
        
    def selection(self, player, game, sequence):
        """
        parent_state: tuple
            state of the parent
        """
        selected_node = self.get_node(sequence[-1])
        score = {'1': 0, '2': 0}
        while len(selected_node.children_states) > 0 and game.running: 
            unvisited_nodes = []
            max_ucb = -math.inf
            for child_state in self.tree[tuple(sequence[-1])].children_states:
                child_node = self.get_node(child_state)
                if child_node.state_visits == 0:
                    unvisited_nodes.append(child_state)
                else:
                    child_node.compute_ucb(parent_state_visits=self.tree[tuple(sequence[-1])].state_visits, \
                                           tree=self.tree)
                    self.add_node(child_node)
                    if child_node.ucb >= max_ucb:
                        selected_node = copy.deepcopy(child_node)
                        max_ucb = copy.deepcopy(child_node.ucb)
            if len(unvisited_nodes) > 0:
                selected_node = self.get_node(random.choice(unvisited_nodes))
            self.mcts_board = copy.deepcopy(selected_node.state)
            selected_node.add_visit()
            self.add_node(selected_node)
            score = game.game_won(board=self.mcts_board, player=player)
            sequence.append(selected_node.state)
            if game.running:
                player = player.next_player()
        return sequence, player, game, score
    
    def get_available_actions(self):            
        return np.where(self.mcts_board == 0)[0]   # return only the actions
    
    def expansion(self, parent_state, player):
        actions = self.get_available_actions()
        for action in actions:
            state = copy.deepcopy(self.mcts_board)
            state[action] = player.index
            node = Node(state, player.index)
            self.add_node(node)   
            parent_node = self.get_node(parent_state)
            parent_node.children_states.append(state)
            self.add_node(parent_node)
        
    def rollout(self, player, game):
        while game.running:
            actions = self.get_available_actions()
            action = random.choice(actions)
            self.mcts_board[action] = player.index
            score = game.game_won(player=player, board=self.mcts_board) 
            player = player.next_player()
        return score
    
    def backpropagate(self, selected_node, score, sequence):
        sequence.reverse()
        for idx, node_state in enumerate(sequence):
            node = self.get_node(node_state)
            node.wins += score[str(node.player_index)]   # Score depends on the player for the node   
            if idx < (len(sequence) - 1):
                node.compute_ucb(self.get_node(sequence[idx + 1]).state_visits, self.tree)                       
            self.add_node(node)
        
    def choose_best_action(self, player, game):
        original_diplay_option = game.display_option
        game.display_option = False
        first_player = player
        self.tree = dict()
        self.mcts_board = copy.deepcopy(game.board)
        init_state = copy.deepcopy(self.mcts_board)
        root_node = Node(init_state, player.index)
        self.add_node(root_node)
        counter = 0        
        while counter < self.max_counter:
            player = first_player           
            game.running = True
            sequence = []
            self.mcts_board = copy.deepcopy(game.board)
            node = self.get_node(init_state)
            node.add_visit()
            if len(sequence) > 0:
                node.compute_ucb(self.get_node(sequence[-1]).state_visits, self.tree)
            self.add_node(node)
            sequence.append(node.state)
            sequence, player, game, score = self.selection(player, game, sequence)
            if game.running:
                self.expansion(sequence[-1], player)
                sequence, player, game, score = self.selection(player, game, sequence)
            if game.running:
                score = self.rollout(player, game)  # else, use the rollout score
            self.backpropagate(self.get_node(sequence[-1]), score, sequence)
            counter += 1        
        # TODO: simplify - Choose the child with the highest number of visits
        self.mcts_board = copy.deepcopy(game.board)
        actions = self.get_available_actions()
        max_state_visits = 0
        best_action = -1
        logging.debug(f'Choosing the best action...')
        for action in actions:
            state = copy.deepcopy(game.board)
            state[action] = first_player.index
            node = self.get_node(state)            
            state_visits = node.state_visits
            logging.debug(f'Action {action} leads to state {node.state} -- Visited: {node.state_visits}, Won: {node.wins}')
            if (state_visits) > max_state_visits:
                best_action = action
                max_state_visits = state_visits
        logging.debug(f'Chosen action: {best_action}')
        game.display_option = original_diplay_option
        game.running = True
        return best_action
    
    def choice(self, player, game):
        action = self.choose_best_action(player, game)
        game.board[action] = player.index
        game.draw_action(action, 'img/circle.png')
        game.game_won(player=player, board=game.board)
        game.turn += 1

        
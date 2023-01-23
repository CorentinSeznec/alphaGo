# -*- coding: utf-8 -*-
''' This is the famous random player which (almost) always looses.
'''

import Goban
from playerInterface import *

import numpy as np
import matplotlib.pyplot as plt
from GameAbstraction import GameAbstract
from node import node
import time
class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''
    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "MCTS Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            
            print("Referee told me to play but the game is over!")
            
            return "PASS"

        # Let's plot some board probabilities
        import go_plot
        
        
        # MCTS
    
        node_init = node(self._board, self._mycolor, 0, terminal_node=False)
    
        for i in range(30):
            
            start_time = time.time()
            
            with open('readme.txt', 'a') as file:  
                file.write("\n\nI'm player Black - X") if self._mycolor == 1 else file.write("\n\nI'm player White - O") 
                file.write("\niteration"+str(i))
           

            node_to_expand = node_init.select_child()
            node_to_expand.expand()

            # regarder ici puis faire la diff apres les rollout
            visit_before = node_to_expand.nbr_visit
            score_before = node_to_expand.score
            
            
            if node_to_expand.terminal_node:
                res = node_to_expand.rollout()
                node_to_expand.backpropag(res)
                return "PASS"
  
                
            else:
                for idx_child, child in enumerate(node_to_expand.children):
 
                    move = child.move_parent
                    child.board.push(move)
            
                    res = child.rollout()

                    child.backpropag(res)

                    child.board.pop()
                
                for _ in range(node_to_expand.gen):
                    child.board.pop()
                    

            visit = node_to_expand.nbr_visit
            score = node_to_expand.score
            with open('readme.txt', 'a') as file:   
                file.write("\nratio victoire:"+str((score - score_before)/(visit - visit_before)))
            
            end_time = time.time()
            with open('readme.txt', 'a') as file:   
                file.write("\ntime:"+str(end_time - start_time))
        best_child = 0
        best_score = 0
        for child in node_init.children:
            current_score = child.score/child.nbr_visit
            if  current_score > best_score:
                best_score = current_score
                best_child = child
        
        move = best_child.move_parent
        with open('readme.txt', 'a') as file:   
            file.write("\nmove selected"+str(self._board.move_to_str(move)))
            

        
        # Correct number for PASS
        if move == 81:
            move = -1
        is_valid = self._board.push(move)
        if is_valid:
            return Goban.Board.flat_to_name(move)
        else:
            with open('readme.txt', 'a') as file:   
                file.write("\nBECAREFUL")

        

    def playOpponentMove(self, move):
        #print("Opponent played ", move, "i.e. ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move))

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

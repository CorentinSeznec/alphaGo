import go_plot
import Goban
import copy
import random
import numpy as np
import matplotlib.pyplot as plt

class node():

    
    def __init__(self, board, mycolor , gen, terminal_node, final_reward= False, parent = False, move_parent= None):
        self.gen = gen
        self.board = board
        self.mycolor = mycolor
        self.parent  = parent
        self.move_parent = move_parent
        self.score = 0
        self.nbr_visit = 0
        self.possible_moves = [] # ACTION posssible for this node, call has_children
        self.children = []
        self.terminal_node = terminal_node
        self.final_reward = final_reward
        
    def print_state(self):
        print("\n----------------")
        print("self.score", self.score)
        print("self.nbr_visit", self.nbr_visit)
        print("self.children", self.children)
        print("----------------\n")
        
    def print_arbre(self, child_index=0):
        
        print("\n------")
        print("my gen:", self.gen)
        print("I'am the ", child_index, "child")
        print("nbr_victoire",self.score,"self.nbr_visit", self.nbr_visit)
        print("I have ", len(self.children), "children")

        if len(self.children) >0:
            for child_index,child in enumerate(self.children):
                   
                child.print_arbre(child_index)
        
    def mean_sucess_node(self):
        return self.score/self.nbr_visit
    
    def is_terminal_node(self):
        
        if len(self.possible_moves) <= 1:
            return 1
        else:
            return 0
        
    # Décrit les actions possible dans self.possible_actions
    def check_possible_children(self):
        
        possible_moves = self.board.weak_legal_moves() # Dont use weak_legal_moves() here!
        
        self.possible_moves = possible_moves

    
    
    def best_child(self, c_params):

  
        children_weights = [child.mean_sucess_node()+c_params* np.sqrt(np.log(self.nbr_visit)/child.nbr_visit)
                                for child in self.children]
        i = np.argmax(children_weights)
        best_child = self.children[np.argmax(children_weights)]
        if not self.board._gameOver:
            self.board.push(best_child.move_parent)
        else:
            with open('readme.txt', 'a') as file:   
                file.write("\n best child game over")
        
        return best_child
    
    
    def select_child(self, c_params= .1):

        # tant que j'ai des fils je select, si pas de fils j'expand? si pas noeud terminal
        if self.children == []:
            with open('readme.txt', 'a') as file:   
                file.write("\n select child je me retorune moi meme, le mvt de mes parent est"+ str(self.move_parent))
            return self
        
        else:
            return self.best_child(c_params).select_child()
            
       
    
    # Creer les fils possible a partir d'un noeud
    def expand(self):
        
        self.check_possible_children()
        self.terminal_node = self.board._gameOver
        
        with open('readme.txt', 'a') as file:   
            file.write("\n possible_moves: game over"+ str(self.terminal_node))
            for move in self.possible_moves:
                file.write(str(move)+ " ")
            
        if self.terminal_node:
            with open('readme.txt', 'a') as file:   
                    file.write("\n\n\n ICIIIIICICICIICIC:")
            pass
        
        else:

            for move in self.possible_moves: 
                
                is_valid = self.board.push(move)
                
                if is_valid:
                    if self.board.is_game_over():
                        with open('readme.txt', 'a') as file:   
                            file.write("\n Game over expand:")
                        result = self.board.result()
                        terminal_node = True
                        if self.mycolor == "black":
                            final_reward = 1 if result == "0-1" else 0
                        else:
                            final_reward = 1 if result == "1-0"  else 0
                        # Creation of child
                        child_node = node(self.board, self.mycolor, self.gen+1, terminal_node, final_reward,  self, move)
                        # add child to children list
                        self.children.append(child_node)
                    
                    else:
                        terminal_node = False
                        final_reward = False
                        # Creation of child
                        child_node = node(self.board, self.mycolor, self.gen+1, terminal_node, final_reward,  self, move)
                        # add child to children list
                        self.children.append(child_node)
                        
                self.board.pop()
                
            
    # Simulation du jeu
    def rollout(self):
        # faire revenir le board à son état
        
        if self.terminal_node:
             
            return self.final_reward
        
        
        idx_push = 0
        # Playing until end
        while not self.board.is_game_over():
            all_moves = self.board.weak_legal_moves()
            
            move = random.choice(all_moves)
            is_valid = self.board.push(move)
            
            while not is_valid:
                self.board.pop()
                move = random.choice(all_moves)
                is_valid = self.board.push(move)

            idx_push +=1
 
        
        result = self.board.result()

                
        if self.mycolor == "black":
            final_reward = 1 if result == "0-1" else 0
        else:
            final_reward = 1 if result == "1-0"  else 0
       
        
        [self.board.pop() for _ in range(idx_push)]
            # with open('readme.txt', 'a') as file:   
            #      file.write("\ndel rollout")
         
        return final_reward 
                
            
            
    
    def backpropag(self, result):
        #print("gen:",self.gen)
        #print("score:", self.score, self.nbr_visit)
        #print("result is added", result)
        self.score += result # 0 ou 1 
        self.nbr_visit += 1
        # print("here",self.nbr_visit)
        # with open('readme.txt', 'a') as file:  
        #     file.write("here"+str(self.nbr_visit))
        if self.parent:
            self.parent.backpropag(result)
         
   
    
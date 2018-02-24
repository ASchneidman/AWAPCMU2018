from base_player import BasePlayer
import networkx as nx

class Player(BasePlayer):

    """
    You will implement this class for the competition.
    You can add any additional variables / methods in this file.
    Do not modify the class name or the base class and do not modify the lines marked below.
    """

    def __init__(self, p_id):
        super().__init__(p_id)  #Initializes the super class. Do not modify!
        self.nuclei = {}
        self.max_size = 50
        self.target = None
        self.dead = false
        """
        Insert player-specific initialization code here
        """
        return


    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables
        if self.nuclei == None:
            for node in self.nodes:
                self.nuclei.add(node)
        if self.nuc
        if self.target in self.nodes:
            self.nucleus = self.target
        """
        Insert any player-specific turn initialization code here
        """
        return

    def split(self, nucleus):
        weakest=[]
        for neighbor in self.board[self.nucleus]:
            n = self.board.nodes[neighbor]
            weakest.append((n, n['old_units']))
        weakest = sorted(weakest, key=lambda tup: tup[1])
        weakest = [i[0] for i in weakest]
        if (len(weakest) >= 2):
            self.move_unit(nucleus, weakest[0], (nucleus['old_units']/2-1))
            self.move_unit(nucleus, weakest[1], (nucleus['old_units']/2-1))
        elif(len(weakest) == 1):
            self.move_unit(nucleus, weakest[0], (nucleus['old_units']/2-1))

    def bomb(self, nucleus):
        for neighbor in self.board[nucleus]:
            n = self.board.nodes[neighbor]
            troops = n['old_units'] + 10
            self.move_unit(nucleus, n, troops)
            self.nuclei.add(n)
        self.nuclei.remove(nucleus)

    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        if dead:
            return self.dict_moves

    def can_bomb(self, nucleus):
        num_enemies=0
        enemy_strength=0
        for neighbor in self.board[nucleus]:
            n=self.board.nodes[neighbor]
            if n['owner'] != self.player_num:
                num_enemies+=1
                enemy_strength+=n['old_units']
        if(num_enemies<4): return False
        elif enemy_strength + 10 * num_enemies > nucleus['old_units']:
            return False
        return True

    def get_weakest(self):
        weakest=None
        weakness=99999999999999
        for neighbor in self.board[self.nucleus]:
            n = self.board.nodes[neighbor]
            if(n['old_units'] <= weakness and n['owner'] != self.player_num):
                weakness = n['old_units']
                weakest = neighbor
        return weakest, weakness

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        for n in self.nuclei:
            if

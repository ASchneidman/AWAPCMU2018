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
        self.nucleus = None
        self.target = None
        """
        Insert player-specific initialization code here
        """
        return


    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables
        if self.nucleus == None:
            for node in self.nodes:
                self.nucleus = node

        if self.target in self.nodes:
            self.nucleus = self.target
        """
        Insert any player-specific turn initialization code here
        """
        return


    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        """
        Insert player logic here to determine where to place your units
        """
        self.place_unit(self.nucleus, self.max_units)
        return self.dict_moves #Returns moves built up over the phase. Do not modify!

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
        """
        Insert player logic here to determine where to move your units
        """
        target, strength= self.get_weakest()
        if(target==None):
            print("backtracking")
            for node in self.board[self.nucleus]:
                target = node
            self.move_unit(self.nucleus, target, self.board.nodes[self.nucleus]['old_units'] - 1)
            self.target = target
        elif (target != None and strength + 2 <= self.board.nodes[self.nucleus]['old_units']):
            print("we're going to win!")
            print("our power: %d, their power: %d" % (self.board.nodes[self.nucleus]['old_units'], strength))
            self.move_unit(self.nucleus, target, self.board.nodes[self.nucleus]['old_units']-1)
            self.target = target

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

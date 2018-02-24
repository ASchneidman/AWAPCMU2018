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
        self.nucleus = self.nodes[0]
        """
        Insert player-specific initialization code here
        """
        return


    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables
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

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """
        target, strength= get_weakest()
        if(strength-1<self.board.nodes[self.nucleus]['old_units']):
            self.move_unit(self.nucleus, target, self.board.nodes[self.nucleus]['old_units']-1)
            self.nucleus=target

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    def get_weakest(self):
        weakest=None
        weakness=99999999999999
        for neighbor in self.board[self.nucleus]:
            if(self.board.nodes[neighbor]['old_units']<=weakness and self.board.nodes[neighbor]['owner']!= self.player_num):
                weakness=self.board.nodes[neighbor]['old_units']
                weakest=self.board.nodes[neighbor]
        return weakest, weakness

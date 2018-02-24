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


    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        if dead:
            return self.dict_moves


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

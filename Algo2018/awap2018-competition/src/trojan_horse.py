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
        self.nuclei = set()
        self.max_size = 50
        self.target_set = None
        self.dead = False
        """
        Insert player-specific initialization code here
        """
        return


    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables
        if self.target_set == None:
            self.target_set = set()
            for node in self.nodes:
                self.target_set.add(node)
        self.nuclei = set()
        for t in self.target_set:
            if t in self.nodes:
                self.nuclei.add(t)
        """
        Insert any player-specific turn initialization code here
        """
        print(self.nuclei)
        return


    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        units = self.max_units
        while True:
            for n in self.nuclei:
                self.place_unit(n, 1)
                units = units - 1
                if units <= 0:
                    return self.dict_moves


    def get_weakest_neighbor(self, n):
        weakest=None
        weakness=99999999999999
        for neighbor in self.board[n]:
            nb = self.board.nodes[neighbor]
            if(nb['old_units'] <= weakness and nb['owner'] != self.player_num):
                weakness = nb['old_units']
                weakest = neighbor
        return weakest, weakness

    def step_and_poop(self, n):
        target, strength = self.get_weakest_neighbor(n)
        if(target==None):
            print("backtracking")
            for node in self.board[n]:
                target = node
            self.move_unit(n, target, self.board.nodes[self.nucleus]['old_units'] - 1)
            self.target_set.add(target)
        elif (target != None and strength + 2 <= self.board.nodes[n]['old_units']):
            print("we're going to win!")
            print("our power: %d, their power: %d" % (self.board.nodes[n]['old_units'], strength))
            self.move_unit(n, target, self.board.nodes[n]['old_units'] - 1)
            self.target_set.add(target)


    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        for n in self.nuclei:
            self.step_and_poop(n)
        return self.dict_moves

    """if self.board.nodes[n]['old_units'] >= self.max_size and self.canbomb(n):
        self.bomb(n)
    elif self.board.nodes[n]['old_units'] >= self.max_size:
        self.split(n)
    else:"""

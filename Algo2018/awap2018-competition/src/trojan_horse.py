from base_player import BasePlayer
import networkx as nx
import random

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
        self.tag = False
        self.counter = 0
        """
        Insert player-specific initialization code here
        """
        return


    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables
        if self.tag:
            self.tag = False
            return
        else:
            self.tag = True
        self.counter = self.counter + 1
        if self.target_set is None:
            self.target_set = set()
            for node in self.nodes:
                self.target_set.add(node)
        self.nuclei.clear()
        for t in self.target_set:
            if t in self.nodes:
                self.nuclei.add(t)
        """
        Insert any player-specific turn initialization code here
        """
        self.target_set.clear()
        if(len(self.nuclei) == 0):
            poop_nuke = random.choice(list(self.nodes))
            self.nuclei.add(poop_nuke)
        print("Nucleus set")
        print(self.nuclei)

    def split(self, nucleus):
        weakest=[]
        for neighbor in self.board[nucleus]:
            n = self.board.nodes[neighbor]
            weakest.append((n, n['old_units'], neighbor))
        weakest = sorted(weakest, key=lambda tup: tup[1])
        weakest = [i[2] for i in weakest]
        if (len(weakest) >= 2):
            self.move_unit(nucleus, weakest[0], (self.board.nodes[nucleus]['old_units']//2-1))
            self.move_unit(nucleus, weakest[1], (self.board.nodes[nucleus]['old_units']//2-1))
            self.target_set.add(weakest[0])
            self.target_set.add(weakest[1])
        elif(len(weakest) == 1):
            self.move_unit(nucleus, weakest[0], (self.board.nodes[nucleus]['old_units']//2-1))
            self.target_set.add(weakest[0])
            self.target_set.add(nucleus)

    def bomb(self, nucleus):
        for neighbor in self.board[nucleus]:
            n = self.board.nodes[neighbor]
            troops = n['old_units'] + 10
            self.move_unit(nucleus, n, troops)
            self.target_set.add(neighbor)
        self.target_set.remove(nucleus)

    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        units = self.max_units
        while units >= 0:
            for n in self.nuclei:
                self.place_unit(n, 1)
                units = units - 1
                if units <= 0:
                    return self.dict_moves

    def can_bomb(self, nucleus):
        num_enemies=0
        enemy_strength=0
        for neighbor in self.board[nucleus]:
            n=self.board.nodes[neighbor]
            if n['owner'] != self.player_num and n['owner'] != None:
                num_enemies+=1
                enemy_strength+=n['old_units']
        print("Stats: enemies: %d, strengh: %d" % (num_enemies, enemy_strength))
        if(num_enemies<3): return False
        elif enemy_strength + 10 * num_enemies > self.board.nodes[nucleus]['old_units']:
            return False
        return True
    def poop_bomb(self, n):
        x = len(self.board[n])
        if(len(self.board[n]) < 3):
            return
        for neighbor in self.board[n]:
            nb = self.board.nodes[neighbor]
            if(nb['owner'] != self.player_num and nb['owner'] in [1, 2, 3, 4]):
                self.target_set.add(neighbor)
                self.move_unit(n, neighbor, self.board.nodes[n]['old_units']//(x + 1))

    def get_weakest_neighbor(self, n):
        weakest=None
        weakness=99999999999999
        for neighbor in self.board[n]:
            nb = self.board.nodes[neighbor]
            if(nb['old_units'] <= weakness and nb['owner'] != self.player_num):
                weakness = nb['old_units']
                weakest = neighbor
        return weakest, weakness

    def poop_split(self, n):
        target, strength = self.get_weakest_neighbor(n)
        if(target == None):
            print("backtracking")
            for node in self.board[n]:
                target = node
            self.move_unit(n, target, self.board.nodes[n]['old_units']//2)
            self.target_set.add(target)
            self.target_set.add(n)
        elif (target != None and strength + 2 <= self.board.nodes[n]['old_units']):
            print("we're going to win!")
            print("our power: %d, their power: %d" % (self.board.nodes[n]['old_units'], strength))
            self.move_unit(n, target, self.board.nodes[n]['old_units']//2)
            self.target_set.add(target)
            self.target_set.add(n)
        else:
            self.target_set.add(n)

    def step_and_poop(self, n):
        target, strength = self.get_weakest_neighbor(n)
        if(target == None):
            print("backtracking")
            for node in self.board[n]:
                target = node
            self.move_unit(n, target, self.board.nodes[n]['old_units'] - min(self.board.nodes[n]['old_units'] - 1, 1))
            self.target_set.add(target)
        elif (target != None and strength + 2 <= self.board.nodes[n]['old_units']):
            print("we're going to win!")
            print("our power: %d, their power: %d" % (self.board.nodes[n]['old_units'], strength))
            self.move_unit(n, target, self.board.nodes[n]['old_units'] - min(self.board.nodes[n]['old_units'] - 1, 1))
            self.target_set.add(target)
        else:
            self.target_set.add(n)


    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        for n in self.nuclei:
            if self.board.nodes[n]['old_units'] >= self.max_size:
                print("we gone splat")
                self.poop_bomb(n)
                print("boom")
            else:
                print("stepping and pooping")
                self.step_and_poop(n)
                print("finished stepping and pooping")

        print("Target set")
        print(self.target_set)
        return self.dict_moves

    """if self.board.nodes[n]['old_units'] >= self.max_size and self.canbomb(n):
        self.bomb(n)
    elif self.board.nodes[n]['old_units'] >= self.max_size:
        self.split(n)
    else:"""

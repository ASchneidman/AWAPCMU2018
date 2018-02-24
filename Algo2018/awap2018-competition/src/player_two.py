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
        # If player is "losing" to someone next to them, funnel units towards that square
        places_needing_units = []
        left_to_place = self.max_units
        for node in self.nodes:
            old_units = self.board.nodes[node]['old_units']
            num_needed_here = 0
            for neighbor in self.board[node]:
                neighbor = self.board.nodes[neighbor]
                if(neighbor['owner'] != self.player_num):
                    num_needed_here += neighbor['old_units']
            places_needing_units.append((node, num_needed_here))
        places_needing_units = sorted(filter(lambda x: x[1] > 0,places_needing_units), key = lambda x: x[1])

        for (node,amount) in places_needing_units:
            amount_to_place_here = min(left_to_place,amount+1)
            self.place_unit(node, amount_to_place_here)
            left_to_place -= amount_to_place_here
            if(left_to_place <= 0):
                break

        nodes_added_to = [a[0] for a in places_needing_units]

        # add one to nodes with one unit
        if(left_to_place > 0):
            for node in self.nodes:
                if(self.nodes[node]['old_units'] == 1):
                    self.place_unit(node,1)
                    left_to_place -= 1
                if(left_to_place <= 0):
                    break


        # add more in reverse order, distribute evenly
        if(left_to_place > 0):
            if(len(nodes_added_to) > 0):
                nodes_to_add_to = nodes_added_to
            else:
                nodes_to_add_to = self.nodes
            num_in_each = left_to_place//len(nodes_to_add_to)
            leftover = left_to_place%len(nodes_to_add_to)
            for node in reversed(nodes_to_add_to):
                amount = num_in_each
                if(leftover > 0):
                    leftover -= 1
                    amount += 1
                if(amount > 0):
                    self.place_unit(node,amount)

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """        
        #if you see a neighbor you can attack, do it.
        attackable_neighbors = {}

        node_to_attackable_neighbor = {}

        node_units_available = {}


        for node in self.nodes:
            old_units = self.board.nodes[node]['old_units']
            node_units_available[node] = old_units
            for neighbor in self.board[node]:
                if(self.board.nodes[neighbor]['owner'] != self.player_num):
                    neighbor_amount = self.board.nodes[neighbor]['old_units']
                    if(neighbor_amount + 1 < old_units):
                        try:
                            attackable_neighbors[(neighbor, neighbor_amount)].append(node)
                        except KeyError:
                            attackable_neighbors[(neighbor, neighbor_amount)] = [node]
                        try:
                            node_to_attackable_neighbor[node].append((neighbor,neighbor_amount))
                        except KeyError:
                            node_to_attackable_neighbor[node] = [(neighbor,neighbor_amount)]


        neighbors_moved = set()

        for node in node_to_attackable_neighbor:
            for(neighbor,neighbor_amount) in node_to_attackable_neighbor[node]:
                if(neighbor not in neighbors_moved):
                    # only one node can attack this, go ahead
                    if(node_units_available[node] > neighbor_amount + 1):
                        node_units_available[node] -= neighbor_amount + 1
                        self.move_unit(node, neighbor, neighbor_amount + 1)
                        neighbors_moved.add(node)


        return self.dict_moves #Returns moves built up over the phase. Do not modify!

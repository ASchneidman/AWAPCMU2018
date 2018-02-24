from base_player import BasePlayer
import networkx as nx
import operator
import random
import copy
import inspect

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
        self.long_term_attack_targets = set() 
        self.long_term_protect_targets = set()
        self.long_term_unit_counts = dict() #Contains (prev_enemy_count, curr_enemy_count)
        self.long_term_movements = dict() # Contains list of nodes to move to

        return


    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables
        self.list_graph = sorted(list(self.board.nodes(data=True)))
        """
        Insert any player-specific turn initialization code here
        """
        return


    """
    Looks at the call stack to see who the caller is - can be useful debugging error messages
    """
    def find_caller(self):
        frame,filename,line_number,function_name,lines,index = inspect.stack()[2]
        # (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
        print(function_name, ':', line_number)
        return

    """
    Run some basic checks and then call the parent function to add the move
    """
    def verify_and_place_unit(self, node, amount):
        if (self.list_graph[node] is None):
            print("Error: Node does not exist in list_graph")
            return

        if (self.list_graph[node][1]['owner'] != self.player_num):
            print("Error: You do not own this node you are placing into")
            self.find_caller()
            return

        if (amount <= 0):
            return

        if (amount > self.max_units):
            print("Error: You are trying to place too many units")
            return

        super().place_unit(node, amount)
        return

    """
    Run some basic checks and then call the parent function to add the move
    """
    def verify_and_move_unit(self, start, end, amount):
        if (amount <= 0):
            return

        start_node = self.list_graph[start]
        end_node = self.list_graph[end]

        if ((start is None) or (end is None)):
            print("Error: Node does not exist in list_graph")
            return

        if (start_node[1]['owner'] != self.player_num):
            print("Error: You do not own this node you are starting from")
            return

        if (start == end):
            return

        if (start_node[1]['old_units'] <= amount):
            print("Error: You do not have enough units to execute this movement")
            print("You are requesting", amount, "units, but you only have ", start_node[1]['old_units'], 'units')
            self.find_caller()
            return

        super().move_unit(start, end, amount)
        return

    """
    Determine number of enemy units connected to this node
    min_val == True: Return minimum number of units needed to take over an adjacent node
    min_val == False: Return sum of all enemies adject to this node
    """
    def get_enemy_units(self, node, min_val=False):
        neighbors = self.board.neighbors(node)
        curr_enemy_count = 0
        min_count = 9999999
        for n in neighbors:
            n_node = self.board.nodes[n]
            if (n_node['owner'] != self.player_num):
                min_count = min(min_count, n_node['old_units'])
                curr_enemy_count += n_node['old_units']
        if (min_val):
            if (min_count == 9999999):
                return 0
            return min_count
        return curr_enemy_count



    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        """
        Insert player logic here to determine where to place your units
        """

        for target in self.long_term_unit_counts:
            curr_enemy_count = self.get_enemy_units(target)
            prev_enemy_count = self.long_term_unit_counts[target][0]
            self.long_term_unit_counts[target] = (prev_enemy_count, curr_enemy_count)

        for target in copy.copy(self.long_term_protect_targets):
            if (self.board.nodes[target]['owner'] != self.player_num):
                continue # Oh no, someone took the node before we could protect it 

            if (target in self.long_term_unit_counts):
                count = self.long_term_unit_counts[target]
                self.verify_and_place_unit(target, count[1] - count[0])
                self.long_term_unit_counts[target] = (self.long_term_unit_counts[target][1], self.get_enemy_units(target))
            else:
                self.long_term_unit_counts[target] = (0, self.get_enemy_units(target))
            if (self.long_term_unit_counts[target][1] == 0):
                self.long_term_unit_counts.pop(target, None)
                self.long_term_protect_targets.remove(target)

        for target in copy.copy(self.long_term_attack_targets):
            if (self.board.nodes[target]['owner'] != self.player_num):
                continue # Oh no, someone took the node before we could attack from it

            if (target in self.long_term_unit_counts):
                self.long_term_unit_counts[target] = (self.long_term_unit_counts[target][1], self.get_enemy_units(target, True))
            else:
                self.long_term_unit_counts[target] = (0, self.get_enemy_units(target, True))

            count = self.long_term_unit_counts[target]
            new_units = min(count[1] - self.list_graph[target][1]['old_units'] + 2, self.max_units)
            self.verify_and_place_unit(target, new_units)
            if (self.long_term_unit_counts[target][1] == 0):
                self.long_term_unit_counts.pop(target, None)
                self.long_term_attack_targets.remove(target)

        for i in range(self.max_units, 0, -1):
            node = random.choice(list(self.nodes))
            self.verify_and_place_unit(node, 1)


        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    

    def execute_single_turn_actions(self):
        for nodes in self.nodes:
            neighbors = self.board.neighbors(nodes)
            for n in neighbors:
                self_units =self.board.nodes[nodes]['old_units']
                n_node = self.board.nodes[n]
                n_units = n_node['old_units']
                n_owner = n_node['owner']

                if (n_owner != self.player_num):
                    # For now, prioritize attacking
                    if ((n_units + 1) < self_units):
                        self.verify_and_move_unit(nodes, n, n_units + 1)
                    else:
                        self.long_term_attack_targets.add(nodes)    #Maybe I'll get around to it

                    # Protect nodes at risk                
                    if ((n_owner != None) and (n_owner != self.player_num)):                    
                        if (n_units > self_units/2):
                            self.long_term_protect_targets.add(nodes)
        return
    # TODO: Fix the many logical problems with this function
    # Missing many edge cases
    # 1. Circular scheduling
    # 2. Pathing through unowned nodes
    # 3. Small viewing window
    def schedule_multi_turn_actions(self):

        
        #Calculate all path lengths, even if we don't use it
        length = nx.all_pairs_shortest_path_length(self.board)
        list_len = (dict(length)) #(nodeA, {nodeB:dist, nodeC:dist ...})

        for nodes in self.long_term_attack_targets:

            neighbors = self.board.neighbors(nodes)
            targets = []
            for n in neighbors:
                n_node = self.board.nodes[n]
                if (n_node['owner'] != self.player_num):
                    targets.append((n, n_node['old_units']))

            if (len(targets) == 0):
                continue

            targets.sort(key=lambda pair: pair[1])


            curr_dists = list_len[nodes] #Dictionary(nodeB:dist, nodeC:dist ...)

            curr_dists = sorted(curr_dists.items(), key=operator.itemgetter(1))
            curr_dists = filter(lambda d: (d[1] < 5) and (d[1] > 0), curr_dists) #Only focus on nodes between 1 and 4 units away
            curr_dists = list(curr_dists)

            for n in copy.copy(curr_dists):
                if (self.board.nodes[n[0]]['owner'] != self.player_num):
                    curr_dists.remove(n)

            if (len(curr_dists) == 0):
                continue

            curr_target_num = 0
            units_needed = targets[0][1]
            for d in curr_dists:
                curr_target = targets[curr_target_num]
                src = d[0]
                path = list(nx.shortest_path(self.board, src, nodes))
                path.pop(0)
                dst = path[-1]

                if (self.board.nodes[dst]['owner'] != self.player_num):
                    continue

                if ((src not in self.long_term_movements) and (dst not in self.long_term_movements)):
                    tmp_node = self.board.nodes[src]

                    if ((tmp_node['old_units']-1) == 0):
                        continue
                    # TODO: Consider spreading requested units out
                    # Update: Considered - not gonna do it
                    mov = list()
                    req_units = min(tmp_node['old_units']-1, units_needed)

                    mov.append((copy.copy(path), req_units))
                    self.long_term_movements[src] = mov
                    units_needed -= self.long_term_movements[src][0][1]
                if (units_needed <= 0):
                    curr_target_num = curr_target_num + 1
                    if (curr_target_num >= len(targets)):
                        break
                    units_needed = targets[curr_target_num][1]


    def execute_multi_turn_actions(self):        
        for mov_src in copy.copy(self.long_term_movements): #Work on cached copy of requests
            actions = self.long_term_movements.pop(mov_src)
            for act in copy.copy(actions):
                actions.remove(act)
                dst = act[0].pop(0)

                if (self.board.nodes[mov_src]['old_units'] <= act[1]):
                    continue # Throw away requests that are no longer valid

                if (self.board.nodes[mov_src]['owner'] != self.player_num):
                    continue # Throw away requests that are no longer valid

                self.verify_and_move_unit(mov_src, dst, act[1])

                if (act[0]):
                    if (dst in self.long_term_movements):
                        self.long_term_movements[dst].append(copy.copy(act))
                    else:
                        self.long_term_movements[dst] = list()
                        self.long_term_movements[dst].append(copy.copy(act))
                


    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """

        self.execute_single_turn_actions();
        self.schedule_multi_turn_actions();
        self.execute_multi_turn_actions();

        #TODO: Consider pruning long_term_*_targets
        #Update: Considered!

        
        return self.dict_moves #Returns moves built up over the phase. Do not modify!

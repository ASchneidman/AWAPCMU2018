import networkx as nx
import copy
import random
import time
import matplotlib.pyplot as plt
import test_board
import grid_board
import circlePoints
import flower_board

class Board():
    def __init__(self, board = None):
        #self.G = self.generate_graph()     #Uncomment this if you want a random graph
        if(board == 'ring'):
            self.G = circlePoints.generate_board()
            self.pos = circlePoints.draw_circle()
        elif(board == 'grid'):
            self.G = grid_board.generateGrid0(12)
            self.pos = grid_board.grid_pos(12)
        elif(board == 'flower'):
            self.G = flower_board.generate_board()
            self.pos = flower_board.draw_circle()
        else:
            self.G = self.generate_random_board(20,25,4)
            self.pos = nx.spring_layout(self.G)
        self.players = {1: {'player': 'p1', 'gain': 1}, 2: {'player': 'p2', 'gain': 1}, 3: {'player': 'p3', 'gain': 1}, 4: {'player': 'p4', 'gain': 1}}


    def generate_random_board(self,num_nodes, num_edges, num_players, num_starting_units = 10):
        # please make edges at least nodes-1
        # please have more nodes than players
        # thx

        if(num_edges < num_nodes-1 or num_edges > (num_nodes-1) * num_nodes / 2):
            print ('Please pick a valid number of edges (between num_nodes-1 and (num_nodes-1) * num_nodes / 2)')
            return

        if(num_nodes < num_players):
            print ('Less nodes than players')
            return

        # first generate a graph with n nodes that has one connection between each one

        nodes = list(range(num_nodes))
        random.shuffle(nodes)

        nodes_in_graph = [nodes[0]]
        edges_in_graph = []

        for new_node in nodes[1:]:
            node_to_link_to_in_graph = random.choice(nodes_in_graph)
            edges_in_graph.append((new_node, node_to_link_to_in_graph))
            nodes_in_graph.append(new_node)

        # fill in the rest of the desired edges with random edges

        num_edges -= len(edges_in_graph)

        for i in range(num_edges):
            node1 = random.choice(nodes_in_graph)
            node2 = random.choice(nodes_in_graph)
            while(node1 == node2 or (node1,node2) in edges_in_graph or (node2,node1) in edges_in_graph):
                node2 = random.choice(nodes_in_graph)
                node1 = random.choice(nodes_in_graph)


            edges_in_graph.append((node1, node2))

        board = {}

        for node in nodes_in_graph:
            board[node] = {'owner':None, 'old_units': 10, 'new_units': 0}

        for player in range(1,num_players+1):
            node = random.choice(nodes_in_graph)
            while(board[node]['owner'] is not None):
                node = random.choice(nodes_in_graph)
            board[node]['owner'] = player
            board[node]['old_units'] = num_starting_units

        G = nx.Graph(edges_in_graph)
        nx.set_node_attributes(G, board)

        return G


    def generate_graph(self):
        init = {0: {'owner': 1, 'old_units': 20, 'new_units': 0}, 1: {'owner': 0, 'old_units': 10, 'new_units': 0}, 2: {'owner': None, 'old_units': 0, 'new_units': 0}}
        edges = [(0, 1), (1, 2)]
        G = nx.Graph(edges)
        nx.set_node_attributes(G, init)
        return G

    def get_owned_nodes(self, owner):
        nodes = {}
        for val in filter(lambda node: node[1]['owner'] == owner, self.G.nodes(data=True)):
            nodes[val[0]] = val[1]
        return nodes, self.players[owner]

    def draw(self):
        pos = self.pos
        # print (list(self.G.nodes))
        colors = nx.get_node_attributes(self.G,'owner')
        colorlist = list(colors.keys())
        nodes = list(self.G.nodes())

        playerColors = {1 : 0.25,   # blue
                        2 : 0.5,    # green
                        3 : 0.7,    # yellow
                        4 : 0.9}    # red

        colorlist = [playerColors.get(colors[node], 1.0) for node in nodes]
        # print ("colors",colorlist, type(colors))

        nodelabels=nx.get_node_attributes(self.G,'old_units')
        for node in nodes:
            nodelabels[node] = str(node) + '\n' + str(nodelabels[node]) + '\n'

        nx.draw(self.G,pos = pos,node_color = colorlist, vmin = 0, vmax = 1)
        nx.draw_networkx_labels(self.G,pos=pos,labels=nodelabels)
        plt.show()


    def check_moves(self, dict_moves, p_id):
        copy_graph = self.G.copy()
        copy_players = copy.deepcopy(self.players)
        total_possible = self.players[p_id].get('gain')

        # geometric sum, nodes are worth 1, .9, .9^2, .9^3....

        total_possible = 4 + int(  (1-pow(.9,total_possible))/(1-.9)   )

        place = dict_moves.get('place')
        nodes_accessed = set()
        if place:
            for node, units in place:
                if units > total_possible:
                    print('Error: Number of units is greater than the total possible.')
                    return None, None
                total_possible -= units
                if copy_graph.nodes[node]['owner'] != p_id:
                    print('Error: Player does not own tile they are placing into.')
                    return None, None
                copy_graph.nodes[node]['old_units'] += units
                nodes_accessed.add(node)

        movement = dict_moves.get('move')
        if movement:
            for start, end, units in movement:
                if copy_graph.nodes[start]['owner'] != p_id:
                    print('Error: Player does not own tile they are starting from.')
                    print('Player ' + str(p_id) + ' is moving from ' + str(start) + ' which is owned by player ' + str(copy_graph.nodes[start]['owner']))
                    return None, None
                if copy_graph.nodes[start]['old_units'] <= units:
                    print('Error: Player does not have enough units to move from start.')
                    return None, None

                copy_graph.nodes[start]['old_units'] -= units
                if end not in copy_graph.neighbors(start):
                    print('Error: End node is not a neighbor of the start node.')
                    return None, None
                elif copy_graph.nodes[end]['owner'] == p_id:
                    copy_graph.nodes[end]['new_units'] += units
                    nodes_accessed.add(end)
                elif copy_graph.nodes[end]['old_units'] >= units:
                    copy_graph.nodes[end]['old_units'] = max(copy_graph.nodes[end]['old_units'] - units, 1)
                    nodes_accessed.add(end)
                else:
                    copy_graph.nodes[end]['new_units'] = units - copy_graph.nodes[end]['old_units']
                    copy_graph.nodes[end]['old_units'] = 0
                    if copy_graph.nodes[end]['owner']:
                        copy_players[copy_graph.nodes[end]['owner']]['gain'] -= 1
                    copy_graph.nodes[end]['owner'] = p_id
                    copy_players[p_id]['gain'] += 1
                    nodes_accessed.add(end)

        for node in nodes_accessed:
            copy_graph.nodes[node]['old_units'] += copy_graph.nodes[node]['new_units']
            copy_graph.nodes[node]['new_units'] = 0

        self.G = copy_graph.copy()
        return copy_graph, copy_players

    def format_for_vis(self):
        g = {}
        for node in self.G.nodes:
            g[node] = {'x':self.pos[node][0], 'y':self.pos[node][1],'n':list(self.G.neighbors(node))}
        return g
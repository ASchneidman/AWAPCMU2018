import networkx as nx
import matplotlib.pyplot as plt


def generate_board():

    nodes = list(range(0,100))

    edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,0),
             (0,2),(2,4),(4,6),(6,8),(8,0),
             (10,11),(11,12),(12,13),(13,14),(14,15),(15,16),(16,17),(17,18),(18,19),(19,10),
             (10,12),(12,14),(14,16),(16,18),(18,10),
             (20,21),(21,22),(22,23),(23,24),(24,25),(25,26),(26,27),(27,28),(28,29),(29,20),
             (20,22),(22,24),(24,26),(26,28),(28,20),
             (30,31),(31,32),(32,33),(33,34),(34,35),(35,36),(36,37),(37,38),(38,39),(39,30),
             (30,32),(32,34),(34,36),(36,38),(38,30)

             ]
    edges += [(x,x+1) for x in range(40,99)] + [(99,40)]
    edges += [(x,x+2) for x in range(40,98)] + [(98,40)]
    edges += [(x,x+10) for x in range(40,90)] + [(90,40)]

    # edges += [(9,40),(0,41),(1,42), # opposite is 5
    #           (19,55),(10,56),(11,57), # opposite is 15
    #           (29,70),(20,71),(21,72), # opposite is 25
    #           (39,85),(30,86),(31,87)] # opposite is 35

    print (edges)

    board = {}

    for node in nodes:
        board[node] = {'owner':None, 'old_units': 10, 'new_units': 0}

    board[5] = {'owner':1, 'old_units': 10, 'new_units': 0}
    board[15] = {'owner':2, 'old_units': 10, 'new_units': 0}

    G = nx.Graph(edges)
    nx.set_node_attributes(G,board)

    return G

def draw_graph(G):


    pos = nx.spring_layout(G)

    nodelabels = {}
    for node in range(0,100):
        nodelabels[node] = str(node)

    nx.draw(G,pos = pos,labels = nodelabels)
    plt.show()
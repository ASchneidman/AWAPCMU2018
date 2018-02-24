
import networkx as nx
import math
import matplotlib.pyplot as plt
from numpy import array

def draw_circle():

    pentagonPoints = []
    circlePoints = []

    r = 1  #radius
    n = 5 #points to generate
    pentagonPoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n-1/8 - 1/10) for i in range(n))
    ]
    r = .5  #radius
    n = 5 #points to generate
    pentagonPoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n - 1/8) for i in range(n))
    ]

    circlePoints += [(x[0] - 1 -2.00739182,x[1] + 1+2.22943448) for x in pentagonPoints]

    pentagonPoints = []

    r = 1  #radius
    n = 5 #points to generate
    pentagonPoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n-1/8 - 1/10 - 1/4) for i in range(n))
    ]
    r = .5  #radius
    n = 5 #points to generate
    pentagonPoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n - 1/8 - 1/4) for i in range(n))
    ]

    circlePoints += [(x[0] + 1+2.00739182,x[1] + 1+2.22943448) for x in pentagonPoints]

    pentagonPoints = []
    r = 1  #radius
    n = 5 #points to generate
    pentagonPoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n-1/8 - 1/10 - 1/2) for i in range(n))
    ]
    r = .5  #radius
    n = 5 #points to generate

    pentagonPoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n - 1/8 - 1/2) for i in range(n))
    ]

    circlePoints += [(x[0] + 1 + 2.00739182,x[1] - 1-2.22943448) for x in pentagonPoints]

    pentagonPoints = []
    r = 1  #radius
    n = 5 #points to generate
    pentagonPoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n-1/8 - 1/10 + 1/4) for i in range(n))
    ]
    r = .5  #radius
    n = 5 #points to generate
    pentagonPoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n - 1/8 + 1/4) for i in range(n))
    ]

    circlePoints += [(x[0] - 1 -2.00739182,x[1] - 1-2.22943448) for x in pentagonPoints]


    r = 3  #radius
    n = 30 #points to generate
    circlePoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * i/n for i in range(n))
    ]
    r = 2  #radius
    n = 20 #points to generate
    circlePoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n+1/40) for i in range(n))
    ]
    r = 1  #radius
    n = 10 #points to generate
    circlePoints += [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * i/n for i in range(n))
    ]

    maxX = max([x[0] for x in circlePoints])
    maxY = max([x[1] for x in circlePoints])

    circlePoints = [(x[0] * 4.5/maxX + 4.5, x[1] * 4.5/maxY + 4.5) for x in circlePoints]

    circlePointDict = {}

    for i in range(100):
        circlePointDict[i] = array(circlePoints[i])

    return circlePointDict
"""
    x = [p[0] for p in circlePoints]
    y = [p[1] for p in circlePoints]

    plt.plot(x,y,'ro')
    plt.show()
"""



def generate_board():

    nodes = list(range(0,100))

    edges = [(0,5),(5,1),(1,6),(6,2),(2,7),(7,3),(3,8),(8,4),(4,9),(9,0),
             (5,6),(6,7),(7,8),(8,9),(9,5)]
    edges += [(x[0]+10,x[1]+10) for x in edges]
    edges += [(x[0]+20,x[1]+20) for x in edges]
    edges += [(0,52),(5,51),(1,50),(10,45),(15,44),(11,43),(20,67),(25,66),(21,65),(30,60),(35,59),(31,58)]
    edges += [(91,94),(94,96),(96,99),(99,91)]

    edges = [(x[0]-40,x[1]-40) for x in edges]



    # corner nodes: 11,13; 12 at ([-2.42705098,  1.76335576])
                  # 17,19; 18 at ([-2.42705098, -1.76335576])
                  # 2,4;   3  at ([ 2.42705098,  1.76335576])
                  # 26,28; 27 at ([ 2.42705098, -1.76335576])

    edges += [(x,x+1) for x in range(0,29)] + [(29,0)]
    edges += [(x,x//3+50) for x in range(0,30,3)]
    edges += [(x,x//3*2+30) for x in range(1,30,3)]
    edges += [(x,x//3*2+31) for x in range(2,30,3)]
    edges += [(x,x+1) for x in range(50,59)] + [(59,50)]
    edges += [(x,50 + (x-30)//2) for x in range(30,49,2)]
    edges += [(x,50 + (x-30+1)//2) for x in range(31,49,2)]
    edges += [(49,50)]
    edges += [(x,x//3*2+30) for x in range(0,30,3)]
    edges += [(x,x//3*2-1+30) for x in range(0,30,3)]
    edges += [(x,x+1) for x in range(30,50,2)]

    edges = [(x[0]+40,x[1]+40) for x in edges]

    # edges += [(9,40),(0,41),(1,42), # opposite is 5
    #           (19,55),(10,56),(11,57), # opposite is 15
    #           (29,70),(20,71),(21,72), # opposite is 25
    #           (39,85),(30,86),(31,87)] # opposite is 35


    board = {}

    for node in nodes:
        board[node] = {'owner':None, 'old_units': 10, 'new_units': 0}

    board[3] = {'owner':1, 'old_units': 10, 'new_units': 0}
    board[13] = {'owner':2, 'old_units': 10, 'new_units': 0}
    board[23] = {'owner':3, 'old_units': 10, 'new_units': 0}
    board[33] = {'owner':4, 'old_units': 10, 'new_units': 0}

    G = nx.Graph(edges)
    nx.set_node_attributes(G,board)

    return G

def draw_graph(G):


    pos = draw_circle()
    print (pos)

    nodelabels = {}
    for node in range(0,100):
        nodelabels[node] = str(node)
    plt.figure(figsize=(5,5))
    nx.draw(G,pos = pos,labels = nodelabels)
    plt.show()


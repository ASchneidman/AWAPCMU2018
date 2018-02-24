
import networkx as nx
import math
import matplotlib.pyplot as plt
from numpy import array

NUMNODES = 80

def draw_circle():

    r = 4  #radius
    n = 8 #points to generate
    centerPoints = [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n + 1/32) for i in range(n))
    ]
    r = 1.2  #radius
    n = 15 #points to generate

    flowerPointsDone = []



    for j in range(8):    
        flowerPoints = [
            (r * math.cos(theta), r * math.sin(theta))
            for r,theta in ((r*((i%2)/4+1),math.pi*2 * ((i+5.5)/n + j/8 + 1/32)) for i in range(n))
        ]
        i = j
        flowerPointsDone += ([(x[0] + centerPoints[i][0],x[1]+centerPoints[i][1]) for x in flowerPoints]*3)[0:5]




    r = 5  #radius
    n = 16 #points to generate
    outerPoints = [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n) for i in range(n))
    ]

    r = .8  #radius
    n = 4 #points to generate
    start_points_1 = []
    start_points = [
        (r * math.cos(theta), r * math.sin(theta))
        for theta in (math.pi*2 * (i/n) for i in range(n))
    ]
    for i in range(4):
        start_points_1 += [(x[0] + outerPoints[4*i][0] * 1.3,x[1] + outerPoints[4*i][1] * 1.3) for x in start_points]

    circlePoints = centerPoints + flowerPointsDone + outerPoints + start_points_1
    maxX = max([x[0] for x in circlePoints])
    maxY = max([x[1] for x in circlePoints])

    circlePoints = [(x[0] * 4.5/maxX + 4.5, x[1] * 4.5/maxY + 4.5) for x in circlePoints]
    print(len(circlePoints))
    circlePointDict = {}


    for i in range(NUMNODES):
        circlePointDict[i] = array(circlePoints[i])

    return circlePointDict
"""
    x = [p[0] for p in circlePoints]
    y = [p[1] for p in circlePoints]

    plt.plot(x,y,'ro')
    plt.show()
"""



def generate_board():

    # nodes = list(range(0,100))

    # edges = [(0,5),(5,1),(1,6),(6,2),(2,7),(7,3),(3,8),(8,4),(4,9),(9,0),
    #          (5,6),(6,7),(7,8),(8,9),(9,5)]
    # edges += [(x[0]+10,x[1]+10) for x in edges]
    # edges += [(x[0]+20,x[1]+20) for x in edges]
    # edges += [(0,52),(5,51),(1,50),(10,45),(15,44),(11,43),(20,67),(25,66),(21,65),(30,60),(35,59),(31,58)]
    # edges += [(91,94),(94,96),(96,99),(99,91)]

    # edges = [(x[0]-NUMNODES,x[1]-NUMNODES) for x in edges]



    # # corner nodes: 11,13; 12 at ([-2.42705098,  1.76335576])
    #               # 17,19; 18 at ([-2.42705098, -1.76335576])
    #               # 2,4;   3  at ([ 2.42705098,  1.76335576])
    #               # 26,28; 27 at ([ 2.42705098, -1.76335576])

    # edges += [(x,x+1) for x in range(0,29)] + [(29,0)]
    # edges += [(x,x//3+50) for x in range(0,30,3)]
    # edges += [(x,x//3*2+30) for x in range(1,30,3)]
    # edges += [(x,x//3*2+31) for x in range(2,30,3)]
    # edges += [(x,x+1) for x in range(50,59)] + [(59,50)]
    # edges += [(x,50 + (x-30)//2) for x in range(30,49,2)]
    # edges += [(x,50 + (x-30+1)//2) for x in range(31,49,2)]
    # edges += [(49,50)]
    # edges += [(x,x//3*2+30) for x in range(0,30,3)]
    # edges += [(x,x//3*2-1+30) for x in range(0,30,3)]
    # edges += [(x,x+1) for x in range(30,50,2)]

    # edges = [(x[0]+NUMNODES,x[1]+NUMNODES) for x in edges]

    # edges += [(9,NUMNODES),(0,41),(1,42), # opposite is 5
    #           (19,55),(10,56),(11,57), # opposite is 15
    #           (29,70),(20,71),(21,72), # opposite is 25
    #           (39,85),(30,86),(31,87)] # opposite is 35

    edges = []

    for i in range(8):
        for j in range(5):
            edges.append((i, i*5+8+j))
        for j in range(2):
            edges.append((i, i*2+48+j))
    for i in range(48,63):
        edges.append((i,i+1))
    edges.append((48,63))
    edges += [(64,65),(65,66),(66,67),(64,67),(66,48),(65,49),(67,63)]
    edges += [(68,69),(69,70),(70,71),(68,71),(71,52),(70,53),(68,51)]
    edges += [(72,73),(73,74),(74,75),(75,72),(73,55),(72,56),(75,57)]
    edges += [(76,77),(77,78),(78,79),(79,76),(78,59),(77,60),(76,61)]

    board = {}

    nodes = range(NUMNODES)

    for node in nodes:
        board[node] = {'owner':None, 'old_units': 10, 'new_units': 0}

    board[64] = {'owner':1, 'old_units': 10, 'new_units': 0}
    board[69] = {'owner':2, 'old_units': 10, 'new_units': 0}
    board[74] = {'owner':3, 'old_units': 10, 'new_units': 0}
    board[79] = {'owner':4, 'old_units': 10, 'new_units': 0}

    G = nx.Graph(edges)
    nx.set_node_attributes(G,board)

    return G

def draw_graph(G):


    pos = draw_circle()
    print (pos)

    nodelabels = {}
    for node in range(0,NUMNODES):
        nodelabels[node] = str(node)
    plt.figure(figsize=(5,5))
    nx.draw(G,pos = pos,labels = nodelabels)
    plt.show()

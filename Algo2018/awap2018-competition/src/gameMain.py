from __future__ import print_function
SERVER_MODE = 1
import sys
import os

if(SERVER_MODE):
    temp_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

from board import Board
import importlib
import json

NUM_TURNS = 200
NUM_PLAYERS = 4

VERBOSE = 1
VISUALIZE = 0

COMPETITION_MODE = 0


def verbose_print(msg):
    if VERBOSE:
        print(msg)

def main():
    players = []
    global NUM_PLAYERS
    NUM_PLAYERS = len(sys.argv) - 2
    for i in range(1,NUM_PLAYERS + 1):
        try:
            input_module = importlib.import_module(sys.argv[i])
        except:
            print('Player module: ' + sys.argv[i] + ' not found.')
            raise
        players.append(input_module.Player(i))

    board = Board(sys.argv[-1]) # if you change command line imputs you might have to change this

    if (board.G is None):
        print('Error: Generated board is null')
        return
    
    run_game(board, players)

def run_game(board, players):


    # construct the output starting from here
    data = {}
    # an array where index:turn, val:dict of board, placements and movements
    # placeholder version right now, update this later.
    data["state"] = []
    data["board"] = board.format_for_vis()

    starting_locations = {}

    for i in range(1,1+NUM_PLAYERS):
        nodes, player = board.get_owned_nodes(i)
        starting_locations[i] = nodes
    data["starting_locations"] = starting_locations
    score = [0] * NUM_PLAYERS
    for i in range(NUM_TURNS):

        if (VISUALIZE):
            board.draw()
        curr_turn = {'1':{'placement':[],'moves':[]},'2':{'placement':[],'moves':[]},'3':{'placement':[],'moves':[]},'4':{'placement':[],'moves':[]}}
        score_str = "Score: "
        for j in range(NUM_PLAYERS):

            verbose_print('Running Turn for ' + str(1+j) + ' Iteration: ' + str(i))

            curr_player = players[j]

            # Player IDs start at 1, so we use 1+j instead of j
            nodes, player = board.get_owned_nodes(1+j)
            score[j] = len(nodes)
            curr_turn[str(1+j)]["score"] = len(nodes)
            score_str = score_str + "P" + str(j) + "(" + str(score[j]) + ") - "
            if score[j] == 0:
                continue

            # Adding nodes for the current player turn into the player key


            # Placement Turn

            try:
                curr_player.init_turn(board.G.copy(), nodes, 4 + int(  (1-pow(.9,player['gain']))/(1-.9)   ))
                placements = curr_player.player_place_units()
                temp_G, temp_players = board.check_moves(placements, 1+j)
            except Exception as ex:
                verbose_print(ex)
                continue

            # Adding placement data into the player key

            if ((temp_G is None) or (temp_players is None)):
                print('Check moves failed after placement. Illegal action detected')
                continue
            else:
                board.G = temp_G
                board.players = temp_players

            curr_turn[str(1+j)]["placement"] = placements["place"];

            # Movement Turn
            try:
                curr_player.init_turn(board.G.copy(), nodes, player['gain'])
                movements = curr_player.player_move_units()
            except Exception as ex:
                verbose_print(ex)
                continue

            temp_G, temp_players = board.check_moves(movements, 1+j)

            # Adding placement data into the player key

            if ((temp_G is None) or (temp_players is None)):
                print('Check moves failed after movement. Illegal action detected.')
                return
            else:
                board.G = temp_G
                board.players = temp_players
            
            curr_turn[str(1+j)]["moves"] = movements["move"];

            nodes, player = board.get_owned_nodes(1+j)
            score[j] = len(nodes)
            curr_turn[str(1+j)]["score"] = len(board.get_owned_nodes(1+j)[0])

        if (COMPETITION_MODE):
            if (len(list(filter(lambda x: x > 0,score))) == 1):
                break

        verbose_print(score_str);

        data["state"].append(curr_turn)
    print('Final Board State')
    
    if (VISUALIZE):
        board.draw()
    # data['score'] = score
    jsonData = json.dumps(data)
    if(SERVER_MODE):
        sys.stdout = temp_stdout
    print(jsonData,end="")
main()

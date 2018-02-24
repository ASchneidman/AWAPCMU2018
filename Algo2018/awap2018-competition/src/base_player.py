class BasePlayer:
    """
    This class provides the necessary interface to communicate with the rest of the code.
    Do not modify this code!
    """

    def __init__(self, p_id):
        self.dict_moves = {'place': [], 'move': []} # Action dictionary (you should only use our interface to modify this)
        self.player_num = p_id      # each player on a board will have a unique player number
        self.max_units = 0          # max number of units the player can place (updated after calling a place command)
        self.nodes = None           # list of nodes that this player owns (updated every turn)
        self.board = None           # networkx object (updated every turn)
        self.list_graph = None      # list representation of the entire board (updated every turn)

        return


    def init_turn(self, board, nodes, max_units):
        self.dict_moves = {'place': [], 'move': []}
        self.max_units = max_units
        self.nodes = nodes
        self.board = board
        
        return
    
    """
    Formats command to interface with Board API for placing units
    Entries do not have to be unique.

    Note: This does not do any error checking! It is up to you to do your own error checking.
          If the board does not validate your move, your action will be thrown out.
          Suggestions for self-checks are provided in the sample AI distributed to you

        --- Parameters ---
        node   : int - node id where you want to place units
        amount : int - amount of units to place at this node
    """    
    def place_unit(self, node, amount):
        place = (node, amount)
        self.dict_moves['place'].append(place)
        self.max_units -= amount
        
        return


    """
    Formats command to interface with Board API for moving units
    Entries do not have to be unique.

    Note: This does not do any error checking! It is up to you to do your own error checking.
          If the board does not validate your move, your action will be thrown out.
          Suggestions for self-checks are provided in the sample AI distributed to you

        --- Parameters ---
        start  : int - node id where you want to move units from
        end    : int - node id where you want to move units to
        amount : int - amount of units to move from start to end
    """
    def move_unit(self, start, end, amount):
        move = (start, end, amount)
        self.dict_moves['move'].append(move)
        self.board.nodes(data=True)[start]['old_units'] -= amount
        
        return

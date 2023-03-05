from utils import *

# directions:
SOUTH = 0
NORTH = 1
EAST = 2
WEST = 3

# pick-up and drop off
PICKUP_PASSENGER = 4
DROP_OFF_PASSENGER = 5


def best_first_graph_search(problem, f):
    """
    depending on lambda function f it is either a A* search, breadth first search or greedy best first search algorithm
    :param problem: the problem for the search algorithm
    :param f: lambda function
    :return: path or none if no path were found
    """
    f = memoize(f, 'f')
    node = problem.initial
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        problem.penalty(1)
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node.getPath()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                newPath = node.getPath()
                child.path.extend(newPath)
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    print("error")
    return None


def move(fromPos, toPos):
    """
    get two adjacent positions and returns the direction
    :param fromPos: position from
    :param toPos: next position has to be an adjacent one
    :return: the direction, -1 if parameters are not adjacent or -2 if fromPos and toPos are equal
    """
    arrP = [0, 0]
    arrP[0] = toPos[0] - fromPos[0]
    arrP[1] = toPos[1] - fromPos[1]
    if arrP == [0, 0]:
        return -2
    elif arrP == [-1, 0]:
        return NORTH
    elif arrP == [1, 0]:
        return SOUTH
    elif arrP == [0, 1]:
        return EAST
    elif arrP == [0, -1]:
        return WEST
    return -1


def setNodes():
    """
    creates the nodes for the environment
    :return: nodes
    """
    nodes = [Node(State([0, 0]))] * 25
    for k in range(25):
        i = int(k / 5)
        j = k % 5
        north = i > 0
        south = i < 4
        west = (j > 0) \
               & ((j != 2) | (i != 0)) \
               & ((j != 1) | (i != 3)) \
               & ((j != 1) | (i != 4)) \
               & ((j != 3) | (i != 3)) \
               & ((j != 3) | (i != 4))
        east = (j < 4) \
               & ((j != 1) | (i != 0)) \
               & ((j != 0) | (i != 3)) \
               & ((j != 0) | (i != 4)) \
               & ((j != 2) | (i != 3)) \
               & ((j != 2) | (i != 4))
        nodes[k] = Node(State([i, j]), north, south, west, east)
    return nodes


def movePath(path, row, column, world, problem):
    """
    This function moves the taxi through the environment
    :param path: path to destination
    :param row: taxi position row
    :param column: taxi position column
    :param world: environment
    :param problem: problem
    :return: taxi position,
    """
    taxi_r = row
    taxi_c = column
    passenger_index = 0
    destination_index = 0
    for i in range(len(path)):
        p = path[i]
        step = move([taxi_r, taxi_c], p)
        if step != -2:
            problem.penalty(1)  # penalty for one step
            state, re, done, info = world.step(step)
            taxi_r, taxi_c, passenger_index, destination_index = world.decode(state)
            world.render()
    return [taxi_r, taxi_c, passenger_index, destination_index]


def getPassengerLocation(index, taxi_row, taxi_col):
    """
    decode the index to get the position of the passenger
    :param index: location passenger
    :param taxi_row: taxi position
    :param taxi_col: taxi position
    :return: position of the passenger
    """
    passenger_pos = [0, 0]
    if index == 1:
        passenger_pos = [0, 4]
    elif index == 2:
        passenger_pos = [4, 0]
    elif index == 3:
        passenger_pos = [4, 3]
    elif index == 4:
        passenger_pos = [taxi_row, taxi_col]
    return passenger_pos


def getDropOffLocation(index):
    """
    decode the index to get the position of the drop off location
    :param index: location of passenger
    :return: drop off position
    """
    destination_pos = [0, 0]
    if index == 1:
        destination_pos = [0, 4]
    elif index == 2:
        destination_pos = [4, 0]
    elif index == 3:
        destination_pos = [4, 3]
    return destination_pos


class State:
    def __init__(self, position):
        """
        creates the state object
        :param position: position of the state
        """
        self.position = position

    def __repr__(self):
        """
        representation of state class
        :return: string
        """
        return "{}".format(self.position)

    def getPosition(self):
        """
        gets the position of the taxi
        :return: position as a list
        """
        return self.position


class Problem:

    def __init__(self, initial, nodes, goal=None):
        """
        creates problem class
        :param initial: starting point
        :param nodes: nodes of taxi environment
        :param goal: goal of problem -> destination of taxi
        """
        self.initial = initial
        self.goal = goal
        self.nodes = nodes
        self.reward = 0

    def goal_test(self, state):
        """
        tests if goal is reached
        :param state: state which will be tested
        :return: returns True if goal is reached
        """
        goalTest = state.getPosition()
        isGoalOne = goalTest[0] == self.goal[0]
        isGoalTwo = goalTest[1] == self.goal[1]
        isGoal = isGoalOne & isGoalTwo
        return isGoal

    def path_cost(self, c):
        """
        calculates the path cost to this node
        :param c: last path cost
        :return: last path cost + 1
        """
        return c + 1

    def penalty(self, n):
        """
        adds a penalty to the problem
        :param n: penalty
        :return: the current reward of problem
        """
        self.reward -= n
        return self.reward

    def getReward(self):
        """
        returns the reward
        :return: reward
        """
        return self.reward

    def next_to(self, location):
        """
        returns the next to locations
        :param location: location which will be checked
        :return: returns the node of the location
        """
        return self.nodes[location[0]*5+location[1]]


class Node:
    def __init__(self,
                 state,
                 next_north=None,
                 next_south=None,
                 next_west=None,
                 next_east=None
                 ):
        """
        creates node class
        :param state: state of node
        :param next_north: position north node or None if not reachable
        :param next_south: position south node or None if not reachable
        :param next_west: position west node or None if not reachable
        :param next_east: position east node or None if nto reachable
        """
        self.state = state
        self.path = []
        if next_north:
            self.next_north = [state.getPosition()[0] - 1, state.getPosition()[1]]
        else:
            self.next_north = None
        if next_south:
            self.next_south = [state.getPosition()[0] + 1, state.getPosition()[1]]
        else:
            self.next_south = None
        if next_west:
            self.next_west = [state.getPosition()[0], state.getPosition()[1] - 1]
        else:
            self.next_west = None
        if next_east:
            self.next_east = [state.getPosition()[0], state.getPosition()[1] + 1]
        else:
            self.next_east = None
        self.path_cost = 0
        self.depth = 0

    def __repr__(self):
        """
        representation of node class
        :return: string
        """
        return "<Node {}, next south {}, next north {}, next east {}, next west {}>".format(self.state,
                                                                                            self.next_south,
                                                                                            self.next_north,
                                                                                            self.next_east,
                                                                                            self.next_west)

    def __lt__(self, node):
        """
        compare norm of positions
        :param node: node
        :return: True if norm of node position is higher than self position
        """
        this = np.linalg.norm(self.state.getPosition())
        that = np.linalg.norm(node.state.getPosition())
        return this < that

    def expand(self, problem):
        """
        getting list of adjacent nodes
        :param problem: problem where the nodes are saved
        :return: adjacent nodes
        """
        listExpand = []
        if self.next_east:
            listExpand.append(problem.next_to(self.next_east))
        if self.next_west:
            listExpand.append(problem.next_to(self.next_west))
        if self.next_south:
            listExpand.append(problem.next_to(self.next_south))
        if self.next_north:
            listExpand.append(problem.next_to(self.next_north))
        return listExpand

    def getPath(self):
        """
        path from start to this node
        :return: path
        """
        path = self.path
        path.append(self.state.getPosition())
        return path

    def __eq__(self, other):
        """
        checks if other state is equal to self state
        :param other: other node
        :return: True if equal
        """
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        """
        hashes state
        :return: hash of state
        """
        return hash(self.state)

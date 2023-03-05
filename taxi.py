import gym
from search import *

rewards = 0


def breadth_first_search(problem):
    """
    Creates a lambda function which calculates the path cost
    :param problem: problem for the search algorithm
    :return: path from the breadth first search algorithm
    """
    f = lambda n: n.path_cost
    return best_first_graph_search(problem, f)


'''
    create environment:
'''
world = gym.make("Taxi-v2").env
world.render()
state, reward, done, info = world.step(DROP_OFF_PASSENGER) # no action -> just getting information about the environment
taxi_row, taxi_col, passenger_index, destination_index = world.decode(state)

# print information:
print("Taxi row:")
print(taxi_row)
print("Taxi column:")
print(taxi_col)
print("Passenger index:")
print(passenger_index)
print("Destination index")
print(destination_index)

world.render()

'''
    create nodes for calculating the route
'''
nodes = setNodes()

'''
    create problem for finding the best route
'''
problem1 = Problem(nodes[taxi_row * 5 + taxi_col], nodes, getPassengerLocation(passenger_index, taxi_row, taxi_col))

'''
    use search algorithm to find the best path to the pick-up destination
'''
path1 = breadth_first_search(problem1)

'''
    move to pick-up destination using the best path
'''
taxi_row, taxi_col, passenger_index, destination_index = movePath(path1,
                                                                  taxi_row,
                                                                  taxi_col,
                                                                  world,
                                                                  problem1)


print("pickup: row " + str(taxi_row) + " col " + str(taxi_col))

'''
    pick-up passenger
'''
step, reward, done, info = world.step(PICKUP_PASSENGER)
print("passenger index: " + str(passenger_index))
print("destination index: " + str(destination_index))
taxi_row, taxi_col, passenger_index, destination_index = world.decode(step)

# add reward
if passenger_index == 4:
    rewards += 10

print("passenger index after pick up: " + str(passenger_index))
print("Taxi row:")
print(taxi_row)
print("Taxi column:")
print(taxi_col)

world.render()

'''
    create nodes for calculating the route
'''
nodes = setNodes()

'''
    create problem for finding the best route
'''
problem2 = Problem(nodes[taxi_row * 5 + taxi_col], nodes, getDropOffLocation(destination_index))

'''
    use search algorithm to find the best path to the drop-off destination
'''
path2 = breadth_first_search(problem2)

'''
    move to drop off destination using the best path
'''
taxi_row, taxi_col, passenger_index, destination_index = movePath(path2,
                                                                  taxi_row,
                                                                  taxi_col,
                                                                  world,
                                                                  problem2)

print("drop-off: row " + str(taxi_row) + " col " + str(taxi_col))
print("Done: " + str(done))

'''
    drop off passenger
'''
step, reward, done, info = world.step(DROP_OFF_PASSENGER)
print("destination index: " + str(destination_index))

# rewards
if done:
    rewards += 10
rewards += problem1.getReward()
rewards += problem2.getReward()

taxi_row, taxi_col, passenger_index, destination_index = world.decode(step)
world.render()

# info
print("Done: " + str(done))
print("Reward: " + str(rewards))

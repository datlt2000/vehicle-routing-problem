"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""
import math

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from data import read_dataset
import matplotlib.pyplot as plt

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    file_name = "custom/e.vrp"
    distance = read_dataset(file_name)
    data['distance_matrix'] = distance
    data['num_vehicles'] = 4
    data['depot'] = 0
    print(data)
    return data

def visualize(routes, distance):
    for i in routes:
        x = []
        y = []
        for j in i:
            x.append(distance["distance_matrix"][j + 1]['x'])
            y.append(distance["distance_matrix"][j + 1]['y'])
        plt.plot(x, y)
    plt.show()

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    vi_data = []
    for vehicle_id in range(data['num_vehicles']):
        vehicle_route = []
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            vehicle_route.append(manager.IndexToNode(index))
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        vehicle_route.append(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
        with open("./result/vrp-ortool/vrp-ortool.txt", 'a') as f:
            f.write(plan_output)
        vi_data.append(vehicle_route)
    print('Maximum of the route distances: {}m'.format(max_route_distance))
    with open("./result/vrp-ortool/vrp-ortool.txt", 'a') as f:
        f.write('\n optimal: ' + str(max_route_distance))
        f.write("\n-------------------------\n")
    visualize(vi_data, data)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        d = data['distance_matrix'][to_node + 1]['d'] + math.sqrt(
            math.pow(data['distance_matrix'][from_node + 1]['x'] - data['distance_matrix'][to_node + 1]['x'], 2) + math.pow(
                data['distance_matrix'][from_node + 1]['y'] - data['distance_matrix'][to_node + 1]['y'], 2))
        return d

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('No solution found !')


if __name__ == '__main__':
    main()

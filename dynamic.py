import itertools
import time
import pandas as pd
import matplotlib.pyplot as plt
from generator import City, cost

def read_data(size):
    cities = []
    with open(f'data/cities_{size}.data', 'r') as f:
        lines = f.readlines()
        for line in lines:
            x, y = map(float, line.split())
            cities.append(City(x, y))
    return cities

def solve(cities):
    distance_matrix = [[x.distance(y) for y in cities] for x in cities]
    route_matrix = {(frozenset([0, idx + 1]), idx + 1): (dist, [0, idx + 1]) for idx, dist in enumerate(distance_matrix[0][1:])}
    for m in range(2, len(cities)):
        temp_matrix = {}
        for cities_set in [frozenset(C) | {0} for C in itertools.combinations(range(1, len(cities)), m)]:
            for j in cities_set - {0}:
                temp_matrix[(cities_set, j)] = min([(route_matrix[(cities_set - {j}, k)][0] + distance_matrix[k][j], 
                route_matrix[(cities_set - {j}, k)][1] + [j]) for k in cities_set if k != 0 and k != j])
        route_matrix = temp_matrix  
    res = min([(route_matrix[d][0] + distance_matrix[0][d[1]], route_matrix[d][1]) for d in iter(route_matrix)])
    route = [cities[i] for i in res[1]]
    return route

def display(cities, size):
    fig = plt.figure()
    fig.suptitle("Dynamic TSP")
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.savefig(f'images/dynamic_{size}.png')
    plt.show(block=True)

def main():
    runtime_dict = {}
    avg = 1
    for size in range(11,12):
        runtime = 0
        cost_total = 0
        for iteration in range(0, avg):
            begin = time.time()
            cities = read_data(size)
            route = solve(cities)
            end = time.time()
            print(f"Path cost for graph of size {size}: {cost(route)}; Time taken : {end - begin}")
            # display(cities, size)
            runtime += end - begin
            cost_total += cost(route)
        runtime_dict[size] = str(runtime/avg) + "   " + str(cost_total/avg)
    # df = pd.DataFrame(runtime_dict.items()) 
    # writer = pd.ExcelWriter(f'output/dynamic__runtime.xlsx')
    # df.to_excel(writer, f'dynamic_runtime')
    # writer.save()

if __name__ == "__main__":
    main()
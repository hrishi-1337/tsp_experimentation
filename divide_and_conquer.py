import itertools
import math
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


def split_longer_dim(cities):
    cities_by_x = sorted(cities, key=lambda city: city.x)
    cities_by_y = sorted(cities, key=lambda city: city.y)
    middle_length = len(cities_by_x) // 2
    if abs(cities_by_x[0].x - cities_by_x[-1].x) > abs(cities_by_y[0].y - cities_by_y[-1].y):
        return cities_by_x[:middle_length], cities_by_x[middle_length:]
    else:
        return cities_by_y[:middle_length], cities_by_y[middle_length:]

def merge(graph_1, graph_2):
    if isinstance(graph_1, City):
        graph_2.append((graph_1, graph_2[0][0]))
        graph_2.append((graph_1, graph_2[0][1]))
        return graph_2
    min_cost = math.inf
    for edge_1_index, (city_00, city_01) in enumerate(graph_1):
        for edge_2_index, (city_10, city_11) in enumerate(graph_2):
            cost = city_00.distance(city_10) + city_01.distance(city_11) - \
                    city_00.distance(city_01) - city_01.distance(city_10)
            cost2 = city_00.distance(city_11) + city_01.distance(city_10) - \
                    city_00.distance(city_01) - city_01.distance(city_10)
            if cost < min_cost:
                min_cost = cost
                min_edge_1 = (city_00, city_10)
                min_edge_2 = (city_01, city_11)
                old_edge_1_index = edge_1_index
                old_edge_2_index = edge_2_index
            if cost2 < min_cost:
                min_cost = cost2
                min_edge_1 = (city_00, city_11)
                min_edge_2 = (city_01, city_10)
                old_edge_1_index = edge_1_index
                old_edge_2_index = edge_2_index
    if len(graph_1) + len(graph_2) > 4:
        del graph_1[old_edge_1_index]
        del graph_2[old_edge_2_index]
    elif len(graph_1) + len(graph_2) == 4:
        del graph_2[old_edge_2_index]
    graph_1.extend([min_edge_1, min_edge_2])
    graph_1.extend(graph_2)
    return graph_1

def solve(cities):
    if len(cities) < 1:
            raise Exception('recursing on cities length < 0')
    elif len(cities) == 1:
        return cities[0]
    elif len(cities) == 2:
        return [(cities[0], cities[1])]
    else:
        half_1, half_2 = split_longer_dim(cities)
        graph_1 = solve(half_1)
        graph_2 = solve(half_2)
        merged = merge(graph_1, graph_2)
        return merged


def display(cities, size):
    fig = plt.figure()
    fig.suptitle("Divide & Conquer TSP")
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
    for size in range(3,12):
        runtime = 0
        cost_total = 0
        for iteration in range(0, avg):
            begin = time.time()
            cities = read_data(size)
            route = solve(cities)
            path_cost = sum([edge[0].distance(edge[1]) for edge in route])
            end = time.time()
            print(f"Path cost for graph of size {size}: {path_cost}; Time taken : {end - begin}")
            display(cities, size)
            runtime += end - begin
            cost_total += path_cost
        runtime_dict[size] = str(runtime/avg) + "   " + str(cost_total/avg)
    df = pd.DataFrame(runtime_dict.items()) 
    writer = pd.ExcelWriter(f'output/dnc__runtime.xlsx')
    df.to_excel(writer, f'dnc_runtime')
    writer.save()

if __name__ == "__main__":
    main()
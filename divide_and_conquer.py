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


def split(cities):
    x_sort = sorted(cities, key=lambda city: city.x)
    y_sort = sorted(cities, key=lambda city: city.y)
    mid = len(x_sort) // 2
    if abs(x_sort[0].x - x_sort[-1].x) > abs(y_sort[0].y - y_sort[-1].y):
        return x_sort[:mid], x_sort[mid:]
    else:
        return y_sort[:mid], y_sort[mid:]

def merge(subgraph_1, subgraph_2):
    if isinstance(subgraph_1, City):
        subgraph_2.append((subgraph_1, subgraph_2[0][0]))
        subgraph_2.append((subgraph_1, subgraph_2[0][1]))
        return subgraph_2
    min_cost = math.inf
    for index_1, (city_00, city_01) in enumerate(subgraph_1):
        for index_2, (city_10, city_11) in enumerate(subgraph_2):
            cost = city_00.distance(city_10) + city_01.distance(city_11) - city_00.distance(city_01) - city_10.distance(city_11)
            cost2 = city_00.distance(city_11) + city_01.distance(city_10) - city_00.distance(city_01) - city_10.distance(city_11)
            if cost < min_cost:
                min_cost = cost
                min_edge_1 = (city_00, city_10)
                min_edge_2 = (city_01, city_11)
                del_index_1 = index_1
                del_index_2 = index_2
            if cost2 < min_cost:
                min_cost = cost2
                min_edge_1 = (city_00, city_11)
                min_edge_2 = (city_01, city_10)
                del_index_1 = index_1
                del_index_2 = index_2
    if len(subgraph_1) + len(subgraph_2) > 4:
        del subgraph_1[del_index_1]
        del subgraph_2[del_index_2]
    elif len(subgraph_1) + len(subgraph_2) == 4:
        del subgraph_2[del_index_2]
    subgraph_1.extend([min_edge_1, min_edge_2])
    subgraph_1.extend(subgraph_2)
    return subgraph_1

def solve(cities):
    if len(cities) < 1:
        print("Empty graph")
    elif len(cities) == 1:
        return cities[0]
    elif len(cities) == 2:
        return [(cities[0], cities[1])]
    else:
        half_1, half_2 = split(cities)
        subgraph_1 = solve(half_1)
        subgraph_2 = solve(half_2)
        merged = merge(subgraph_1, subgraph_2)
        return merged


def display(cities, size):
    fig = plt.figure()
    fig.suptitle("Divide & Conquer TSP")
    x_list, y_list = [], []
    for city1, city2 in cities:
        x_list.append(city1.x)
        x_list.append(city2.x)
        y_list.append(city1.y)
        y_list.append(city2.y)
        plt.plot([city1.x, city2.x], [city1.y, city2.y], 'g')
    plt.plot(x_list, y_list, 'ro')
    plt.savefig(f'images/dnc_{size}.png')
    plt.show(block=True)

def main():
    runtime_dict = {}
    avg = 5
    sizes = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 32, 64, 128, 256, 512, 1024, 2048]
    # sizes = [32]
    for size in sizes:
        runtime = 0
        cost_total = 0
        for iteration in range(0, avg):
            begin = time.time()
            cities = read_data(size)
            route = solve(cities)
            print(route)
            path_cost = sum([edge[0].distance(edge[1]) for edge in route])
            end = time.time()
            print(f"Path cost for graph of size {size}: {path_cost}; Time taken : {end - begin}")
            # display(route, size)
            runtime += end - begin
            cost_total += path_cost
        runtime_dict[size] = str(runtime/avg) + "   " + str(cost_total/avg)
    df = pd.DataFrame(runtime_dict.items()) 
    writer = pd.ExcelWriter(f'output/dnc__runtime.xlsx')
    df.to_excel(writer, f'dnc_runtime')
    writer.save()

if __name__ == "__main__":
    main()
import itertools
import time
import pandas as pd
import matplotlib.pyplot as plt
from generator import City, cost

def read_data(size):
    cities = []
    with open(f'data/cities_{size}.data', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            x, y = map(float, line.split())
            cities.append(City(x, y))
    return cities

def solve(cities):
    cities = min(itertools.permutations(cities), key=lambda path: cost(path))
    return cost(cities)


def display(cities, size):
    fig = plt.figure()
    fig.suptitle("Naive TSP")
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.savefig(f'images/naive_{size}.png')
    plt.show(block=True)


def main():
    runtime_dict = {}
    avg = 1
    for size in range(3,12):
        runtime = 0
        for iteration in range(0, avg):
            begin = time.time()
            cities = read_data(size)
            path_cost = solve(cities)
            end = time.time()
            print(f"Path cost for graph of size {size}: {path_cost}; Time taken : {end - begin}")
            display(cities, size)
            runtime += end - begin
        runtime_dict[size] = runtime/avg
    # df = pd.DataFrame(runtime_dict.items()) 
    # writer = pd.ExcelWriter(f'output/naive_runtime.xlsx')
    # df.to_excel(writer, f'runtime_naive')
    # writer.save()

if __name__ == "__main__":
    main()
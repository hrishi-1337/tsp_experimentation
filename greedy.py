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
    unvisited = cities[1:]
    route = [cities[0]]
    while len(unvisited):
        index, nearest_city = min(enumerate(unvisited),key=lambda item: item[1].distance(route[-1]))
        route.append(nearest_city)
        del unvisited[index]
    return route

def display(cities, size):
    fig = plt.figure()
    fig.suptitle("Greedy TSP")
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.savefig(f'images/greedy_{size}.png')
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
            print(route)
            end = time.time()
            print(f"Path cost for graph of size {size}: {cost(route)}; Time taken : {end - begin}")
            display(cities, size)
            runtime += end - begin
            cost_total += cost(route)
        runtime_dict[size] = str(runtime/avg) + "   " + str(cost_total/avg)
    df = pd.DataFrame(runtime_dict.items()) 
    writer = pd.ExcelWriter(f'output/greedy_runtime.xlsx')
    df.to_excel(writer, f'greedy_runtime')
    writer.save()

if __name__ == "__main__":
    main()
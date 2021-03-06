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
    path = [cities[0]]
    while len(unvisited):
        index, closest_city = min(enumerate(unvisited),key=lambda city: city[1].distance(path[-1]))
        path.append(closest_city)
        del unvisited[index]
    return path

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
    # sizes = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 32, 64, 128, 256, 512, 1024, 2048]
    sizes = [16384]
    for size in sizes:
        runtime = 0
        cost_total = 0
        for iteration in range(0, avg):
            begin = time.time()
            cities = read_data(size)
            route = solve(cities)
            print(route)
            end = time.time()
            print(f"Path cost for graph of size {size}: {cost(route)}; Time taken : {end - begin}")
            # display(route, size)
            runtime += end - begin
            cost_total += cost(route)
        runtime_dict[size] = str(runtime/avg) + "   " + str(cost_total/avg)
    df = pd.DataFrame(runtime_dict.items()) 
    writer = pd.ExcelWriter(f'output/greedy_runtime.xlsx')
    df.to_excel(writer, f'greedy_runtime')
    writer.save()

if __name__ == "__main__":
    main()
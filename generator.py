import math
import random
import matplotlib.pyplot as plt
    

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    # def __repr__(self):
    #     return f"({self.x}, {self.y})"


def generate_data():
    counts = []
    for i in range(3, 10):
        counts.append(int(math.pow(2,i)))
    for count in counts:        
        cities = []
        for i in range(count):
            cities.append(City(x=int(random.random() * 1000), y=int(random.random() * 1000)))
        with open(f'data/cities_{count}.data', 'w+') as f:
            for city in cities:
                f.write(f'{city.x} {city.y}\n')

def cost(route):
    return sum([city.distance(route[index - 1]) for index, city in enumerate(route)])


def display(title, cities):
    fig = plt.figure()
    fig.suptitle(title)
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)


generate_data()
import math
import random
    

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

def generate_data(size):     
    cities = []
    for j in range(size):
        cities.append(City(x=int(random.random() * 1000), y=int(random.random() * 1000)))
    with open(f'data/cities_{size}.data', 'w+') as f:
        for city in cities:
            f.write(f'{city.x} {city.y}\n')

def cost(route):
    return sum([city.distance(route[index - 1]) for index, city in enumerate(route)])

if __name__ == "__main__":
    for i in range(3, 12):
        generate_data(i)
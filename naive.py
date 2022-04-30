import itertools
import math
import time
from generator import City, cost, display

class Naive:
    def __init__(self, size):
        self.size = size
        self.cities = []

    def read_data(self):
        with open(f'data/cities_{self.size}.data', 'r') as handle:
            lines = handle.readlines()
            for line in lines:
                x, y = map(float, line.split())
                self.cities.append(City(x, y))
        return self.cities

    def solve(self):
        self.cities = min(itertools.permutations(self.cities), key=lambda path: cost(path))
        return cost(self.cities)

    def main(self):
        begin = time.time()
        self.read_data()
        path_cost = self.solve()
        end = time.time()
        print(f"Path cost for graph of size {self.size}: {path_cost}; Time taken : {end - begin}")
        display("Naive", self.cities)

if __name__ == "__main__":
    naive = Naive(16)
    naive.main()
import math
import numpy as np
import matplotlib.pyplot as plt
import statistics
import utility

class Approximation:
    """Class for approximation"""
    def __init__(self, x, eps = 1e-9, max_iterations = 500):
        self.x = x
        self.eps = eps
        self.results = []
        self.max_iterations = max_iterations
    
    def power_series_generator(self, x):
        """Generates the next sum of decomposition"""
        res = 0
        n = 0
        while True:
            res += math.pow(-1, n) * math.pow(x, 2*n) / math.factorial(2*n)
            n += 1
            yield res

    def approximation(self):
        """Decompositions of a function into a power series and returns table"""
        n = 0
        result = math.cos(self.x)
        my_result = 0
        self.results.append(my_result)
        gen = self.power_series_generator(self.x)
        while n <= 500 and math.fabs(result - my_result) > self.eps:
            my_result = next(gen)
            self.results.append(my_result)
            n += 1
        return result, my_result, n

class PlotApproximation(Approximation):
    """Class for approximation and building"""
    def __init__(self, x, eps=1e-9, max_iterations=500):
        super().__init__(x, eps, max_iterations)
        
    def calculate_statistics(self):
        """Method for calculating statistics"""
        mean = statistics.mean(self.results)
        median = statistics.median(self.results)
        mode = statistics.mode(self.results)
        variance = statistics.variance(self.results)
        stdev = statistics.stdev(self.results)
        return mean, median, mode, variance, stdev  
    
    def plot_approximation(self):
        """Method for drawing plot"""
        points = np.linspace(-np.pi, np.pi, 100)
        X = []
        Y1 = []
        Y2 = []
        dot = self.x
        y_dot = 0
        for x in points:
            self.x = x
            y1, y2, n = self.approximation()
            y_dot = y2 if dot == x else y_dot
            X.append(x)
            Y1.append(y1)
            Y2.append(y2)
        plt.plot(X, Y1, label="math")
        plt.plot(X, Y2, label="my")
        plt.scatter(dot, np.cos(dot), color='red', label='x')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)
        plt.savefig('LR4/plot.png')
        plt.title('Approximation of cos(x)')
        plt.show()


def main():
    
    while True:
        x = utility.get_float_from_input('x')
        eps = utility.get_float_from_input('eps')
        pa = PlotApproximation(x, eps)
        pa.approximation()
        pa.plot_approximation()
        mean, median, mode, variance, stdev = pa.calculate_statistics()
        print('Mean:', mean)
        print('Median:', median)
        print('Mode:', mode)
        print('Variance:', variance)
        print('Standart deviation:', stdev)
        t = input('exit? y/n\n')
        if t == 'y':
            break

if __name__ =="__main__":
    main()
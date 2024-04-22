import numpy as np
import utility

class MatrixStatisticMixin:
    def stats(self):
        mean = np.mean(self.matrix)
        median = np.median(self.matrix)
        corcroef = np.corrcoef(self.matrix)
        variance = np.var(self.matrix)
        stdev = np.std(self.matrix)
        print('Mean:', mean)
        print('Median:', median)
        print('Corrcoef:', corcroef)
        print('Variance:', variance)
        print('Stdev:', stdev)

class MatrixOperations(MatrixStatisticMixin):
    
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.matrix = np.full((n, m), 0)
    
    def create_random_matrix(self):
        gen = utility.random_generator(self.n * self.m)
        for i in range(self.n):
            tmp = []
            for j in range(self.m):
                self.matrix[i][j] = next(gen)
                
    def min_side_diagonal(self):
        x = 0
        y = self.m - 1
        elems = []
        while x < self.n and y >= 0:
            elems.append(self.matrix[x][y])
            x += 1
            y -= 1
        return min(elems)
    
    def variance_side_diagonal_my(self):
        x = 0
        y = self.m - 1
        elems = []
        s = 0
        c = 0
        while x < self.n and y >= 0:
            elems.append(self.matrix[x][y])
            s += self.matrix[x][y]
            c += 1
            x += 1
            y -= 1
        res = 0
        sr = s / c
        print(elems)
        for x in elems:
            res += (x - sr) * (x - sr)
        return np.round(res / c, 2)
        
    def variance_side_diagonal(self):
        x = 0
        y = self.m - 1
        elems = []
        while x < self.n and y >= 0:
            elems.append(self.matrix[x][y])
            x += 1
            y -= 1
        print(elems)
        return np.round(np.var(elems), 2)
    
    def swap_min_elements(self):
        """Method for swapping min elements of first and last rows"""
        if self.matrix is None:
            print("Matrix is empty!")
            return

        min_first_column = np.argmin(self.matrix[:, 0])
        min_last_column = np.argmin(self.matrix[:, -1]) 

        self.matrix[min_first_column, 0], self.matrix[min_last_column, -1] = self.matrix[min_last_column, -1], self.matrix[min_first_column, 0]

    
    def __str__(self):
        return str(self.matrix)


def main():
    
    while True:
        print('1 - create matrix')
        print('2 - min on side diagonal')
        print('3 - variance on side diagonal numpy')
        print('4 - variance on side diagonal my')
        print('5 - statistic')
        print('6 - swap min elements of first and last rows')
        t = utility.get_int_from_input('option')
        if t == 1:
            n = utility.get_int_from_input('N')
            m = utility.get_int_from_input('M')
            matrix = MatrixOperations(n, m) 
            matrix.create_random_matrix()
            print(matrix)
        if t == 2:
            print(matrix.min_side_diagonal())
        if t == 3:
            print(matrix.variance_side_diagonal())
        if t == 4:
            print(matrix.variance_side_diagonal_my())
        if t == 5:
            matrix.stats()
        if t == 6:
            matrix.swap_min_elements()
            print(matrix)
            

if __name__ =="__main__":
    main()
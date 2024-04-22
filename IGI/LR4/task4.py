from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
import numpy as np
import utility

class GeometricalFigure(ABC):
    @abstractmethod
    def area(self):
        pass

class Color:
    
    def __init__(self, color):
        self.color = color

    @property 
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        
class Hexagon(GeometricalFigure):
    name = 'hexagon'
    
    def __init__(self, side, color):
        self.side = side
        self.color = Color(color)
    
    def area(self):
        return 3.0 * math.sqrt(3) / 2.0 * math.pow(self.side, 2)
    
    def plot(self, label):
        angles = np.linspace(0, 2*np.pi, 7)
        x = self.side * np.cos(angles)
        y = self.side * np.sin(angles)

        plt.figure()
        plt.plot(x, y, color=self.color.color)
        
        plt.title(label)
        plt.xlabel('X')
        plt.ylabel('Y')

        plt.grid(True)
        plt.savefig('LR4/plot2.png')
        plt.show()
        
    def __str__(self):
        return "{} color: {} side: {} area: {}".format(self.name, self.color.color, self.side, self.area())
    

def main():
    while True:
        side = utility.get_float_from_input('side')
        color = input('Input color\n')
        while not color in ['black', 'red', 'blue', 'green', 'grey', 'yellow']:
            color = input('Input color\n')
        text = input('Input label text\n')
        hex = Hexagon(side, color)
        print(hex)
        hex.plot(text)
        t = input('exit? y/n\n')
        if t == 'y':
            break


if __name__ =="__main__":
    main()
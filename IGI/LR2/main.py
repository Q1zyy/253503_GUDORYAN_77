import os
from circle import area as circle_area, perimeter as circle_perimetr
from square import area as square_area, perimeter as square_perimetr

storona = os.environ.get("STORONA")

print(square_area(5))
print(square_perimetr(5))
print(circle_area(5))
print(circle_perimetr(5))
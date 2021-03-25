from typing import List, Tuple
from math import ceil, dist


class Positionable:
    def __init__(self, position : Tuple):
        self.position = position
    
    def getX(self) -> int:
        return self.position[0]
    
    def getY(self) -> int:
        return self.position[1]

    def distanceTo(self, positionable : 'Positionable') -> int:
        return ceil(dist(self.position, positionable.position))

    def nearest(self, positionables : list('Positionable')) -> int:
        return min([(p, self.distanceTo(d)) for p, d in enumerate(positionables)], key=lambda x : x[1])[0]

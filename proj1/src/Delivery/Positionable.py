from math import ceil, dist
from typing import List, Tuple

from Delivery.Obj import Obj


class Positionable(Obj):
    def __init__(self, id, position: Tuple):
        super().__init__(id)
        self.position = position

    def getX(self) -> int:
        return self.position[0]

    def getY(self) -> int:
        return self.position[1]

    def distanceTo(self, positionable: 'Positionable') -> int:
        return ceil(dist(self.position, positionable.position))

    def nearest(self, positionables: List['Positionable']) -> int:
        return min([(p, self.distanceTo(d)) for p, d in enumerate(positionables)], key=lambda x: x[1])[0]


if (__name__ == "main"):
    p1 = Positionable((0, 0))
    p2 = Positionable((0, 1))
    p3 = Positionable((1, 1))

    print(p1.distanceTo(p2))
    print(p1.distanceTo(p3))
    print(p2.distanceTo(p3))
    print(p1.nearest([p3, p2]))

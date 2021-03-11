class Drone:
    def __init__(self, id, max_capacity, position):
        self.max_capacity = max_capacity
        self.used_capacity = 0
        self.position = position
        self.id = id
        self.products = {}
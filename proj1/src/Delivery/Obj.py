class Obj:
    def __init__(self, id):
        self.id : int = id
    
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, o: object) -> bool:
        return self.__class__ == o.__class__ and self.id == o.id
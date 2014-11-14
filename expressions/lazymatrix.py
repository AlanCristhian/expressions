class DictVector(dict):
    def __init__(self, vector=None):
        self.vector = vector
        self.stored = {}
        self.size = None

    def __getitem__(self, key):
        if key in self.stored.keys():
            return self.stored[key]
        else:
            value = self.vector[key]
            self.vector[key] = None
            self.stored[key] = value
            if not any(self.vector):
                del self.vector
            return value
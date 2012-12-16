class Keyboard:
    def __init__(self):
        self.keys = {}

    def is_down(self, key):
        return key in self.keys and self.keys[key]

    def keydown(self, key):
        self.keys[key] = True

    def keyup(self, key):
        self.keys[key] = False

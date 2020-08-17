class BoolClass:
    def __init__(self):
        self.redownload = bool()

    def get(self):
        return self.redownload

    def set(self, value):
        self.redownload = value
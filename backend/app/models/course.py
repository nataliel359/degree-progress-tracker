class Course:
    def __init__(self, code, name, credits):
        self.code = code
        self.name = name
        self.credits = credits

    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        return hash(self.code)
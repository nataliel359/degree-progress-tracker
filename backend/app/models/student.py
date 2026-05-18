class Student:
    def __init__(self, name):
        self.name = name
        self.completed_courses = set()

    def add_completed_course(self, course):
        self.completed_courses.add(course)

    def calculate_total_credits(self):
        return sum(course.credits for course in self.completed_courses)
class DegreeProgram:
    def __init__(self, name):
        self.name = name
        self.required_courses = set()
        self.gen_ed_courses = set()
        self.science_breadth_courses = set()
        self.elective_courses = set()

    def add_course(self, course, category):
        if category == "required":
            self.required_courses.add(course)
        elif category == "gen_ed":
            self.gen_ed_courses.add(course)
        elif category == "science_breadth":
            self.science_breadth_courses.add(course)
        elif category == "electives":
            self.elective_courses.add(course)
        else:
            raise ValueError(f"Unknown category: {category}")
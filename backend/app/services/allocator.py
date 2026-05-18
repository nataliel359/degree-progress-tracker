def allocate_courses(student, degree):
    allocation = {
        "required": [],
        "gen_ed": [],
        "science_breadth": [],
        "electives": []
    }

    counted_courses = set()

    category_map = {
        "required": degree.required_courses,
        "gen_ed": degree.gen_ed_courses,
        "science_breadth": degree.science_breadth_courses,
        "electives": degree.elective_courses
    }

    for category, degree_courses in category_map.items():
        for course in student.completed_courses:
            if course in degree_courses:
                allocation[category].append(course)
                counted_courses.add(course)

    total_credits = sum(course.credits for course in counted_courses)

    # for course in student.completed_courses:
    #     if course in degree.required_courses:
    #         allocation["required"].append(course)

    #     if course in degree.gen_ed_courses:
    #         allocation["gen_ed"].append(course)

    #     if course in degree.science_breadth_courses:
    #         allocation["science_breadth"].append(course)

    #     if course in degree.elective_courses:
    #         allocation["electives"].append(course)

    #     unique_courses.add(course)
    
    # total_credits = sum(course.credits for course in unique_courses)

    return allocation, total_credits
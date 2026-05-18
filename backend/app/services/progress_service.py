from app.services.allocator import allocate_courses

def get_missing_courses(student, degree):
    return {
        "required": list(degree.required_courses - student.completed_courses),
        "gen_ed": list(degree.gen_ed_courses - student.completed_courses),
        "science_breadth": list(degree.science_breadth_courses - student.completed_courses),
        "electives": list(degree.elective_courses - student.completed_courses)
    }


def generate_progress(student, degree):
    if "Minor" in degree.name:
        total_credits_needed = {
            "required": 24,
            "gen_ed": 0,
            "science_breadth": 0,
            "electives": 6
        }
    else:
        total_credits_needed = {
            "required": 77,
            "gen_ed": 18,
            "science_breadth": 6,
            "electives": 19
        } 

    allocation, total_completed = allocate_courses(student, degree)

    completed_credits = {
        category: sum(c.credits for c in courses)
        for category, courses in allocation.items()
    }

    missing_courses = get_missing_courses(student, degree)
    total_required = sum(total_credits_needed.values())

    active_categories = [
        cat
        for cat, credits in total_credits_needed.items()
        if credits > 0
    ]

    return {
        "program_name": degree.name,
        "summary": {
            "total_required": total_required,
            "total_completed": total_completed if "Minor" not in degree.name else completed_credits["required"] + completed_credits["electives"],
            "remaining_credits": max(0, total_required - total_completed),
            "progress_percent": round((total_completed / total_required) * 100, 1)
        },
        "requirements": {
            cat: {
                "required": total_credits_needed[cat],
                "completed": completed_credits[cat],
                "remaining": max(0, total_credits_needed[cat] - completed_credits[cat]),
                "completed_courses": [
                    {
                        "code": c.code,
                        "name": c.name,
                        "credits": c.credits
                    }
                    for c in allocation[cat]
                ],
                "missing_courses": [
                    {
                        "code": c.code,
                        "name": c.name,
                        "credits": c.credits
                    }
                    for c in missing_courses[cat]
                ],
            }
            for cat in active_categories
        }
    }
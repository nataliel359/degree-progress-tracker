from app.models.course import Course
from app.models.degree import DegreeProgram
from app.models.student import Student

def create_mock_data():
    student = Student("Natasha Romanoff")
    cs_major = DegreeProgram("Computer Science Major")
    business_minor = DegreeProgram("Business Minor")

    def add_courses(degree, courses, category):
        for course in courses:
            degree.add_course(course, category)

    # =======================
    # COMPUTER SCIENCE MAJOR
    # ======================

    # -----------------------
    # CS REQUIRED
    # -----------------------
    cs_required = [
        Course("LE/EECS 1001", "Research Directions in Computing", 1),
        Course("LE/EECS 1015", "Introduction to Computer Science and Programming", 3),
        Course("LE/EECS 1019", "Discrete Mathematics for Computer Science", 3),
        Course("LE/EECS 1022", "Introduction to Object Oriented Programming", 3),
        Course("LE/EECS 2001", "Introduction to the Theory of Computation", 3),
        Course("LE/EECS 2021", "Computer Organization", 4),
        Course("LE/EECS 2030", "Advanced Object Oriented Programming", 3),
        Course("LE/EECS 2031", "Software Tools", 3),
        Course("LE/EECS 2101", "Fundamentals of Data Structures", 3),
        Course("LE/EECS 3101", "Design and Analysis of Algorithms", 3),
        Course("LE/EECS 3311", "Software Design", 3),
        Course("SC/MATH 1090", "Introduction to Logic for Computer Science", 3),
        Course("SC/MATH 1013", "Applied Calculus I", 3),
        Course("SC/MATH 1014", "Applied Calculus II", 3),
        Course("SC/MATH 2030", "Elementary Probability", 3),
        Course("LE/EECS 3000", "Professional Practice in Computing", 3),
        Course("LE/EECS 3221", "Operating System Fundamentals", 3),
        Course("LE/EECS 3401", "Introduction to AI and Logic Programming", 3),

        # At least 12 credits from EECS 4000-level
        Course("LE/EECS 4413", "Building E-Commerce Systems", 3),
        Course("LE/EECS 4482", "Network Security and Forensics", 3),
        Course("LE/EECS 4484", "Malware Analysis", 3),
        Course("LE/EECS 4080", "Computer Science Project", 3),

        # At least 12 credits outside EECS, MATH, STATS and ITEC -> satisfied under Business Minor
        Course("AP/ADMS 1000", "Introduction to Business", 3),
        Course("AP/ADMS 1010", "Exploring the Functions of Business", 3),
        Course("AP/ADMS 2541", "Introduction to Personal Finance", 3),
        Course("AP/ADMS 2200", "Introductory Marketing", 3)
    ]
    add_courses(cs_major, cs_required, "required")

    # -----------------------
    # GEN ED
    # -----------------------
    gen_ed = [
        Course("SC/PHYS 1411", "Physics Fundamentals I", 3),
        Course("SC/PHYS 1412", "Physics Fundamentals II", 3),
        Course("AP/ECON 1000", "Introduction to Microeconomics", 3),
        Course("AP/PHIL 1100", "The Meaning of Life", 3),
        Course("AP/ECON 1010", "Introduction to Macroeconomics", 3),
        Course("FA/MUSI 1510", "The Musical Experience", 3)
    ]
    add_courses(cs_major, gen_ed, "gen_ed")

    # -----------------------
    # SCIENCE BREADTH
    # -----------------------
    science = [
        # 6 credits in SC/ outside of major
        Course("SC/MATH 1025", "Applied Linear Algebra", 3),
        Course("SC/MATH 1280", "Principles of Risk Management and Insurance", 3)
    ]
    add_courses(cs_major, science, "science_breadth")

    # -----------------------
    # CS ELECTIVES (ONLY CS)
    # -----------------------
    cs_electives = [
        # At least 15 credits at 3000-level or higher
        Course("LE/EECS 3214", "Computer Network Protocols and Applications", 3),
        Course("LE/EECS 3481", "Applied Cryptography", 3),
        Course("LE/EECS 3482", "Introduction to Computer Security", 3),
        Course("LE/EECS 3404", "Applied Machine Learning", 3),
        Course("AP/POLS 3190", "Public Administration", 6),

        # At least 4 credits of additional electives
        Course("AP/ADMS 2400", "Introduction to Organizational Behaviour", 3)
        
    ]
    add_courses(cs_major, cs_electives, "electives")

    # =======================
    # BUSINESS MINOR
    # ======================
    bs_required = [
        Course("AP/ADMS 1000", "Introduction to Business", 3),
        Course("AP/ADMS 1010", "Exploring the Functions of Business", 3),
        Course("AP/ADMS 2541", "Introduction to Personal Finance", 3),
        Course("AP/ADMS 2200", "Introductory Marketing", 3),
        Course("AP/ADMS 2400", "Introduction to Organizational Behaviour", 3),
        Course("AP/ADMS 1550", "Accounting for Non-Financial Managers", 3),
        Course("AP/ADMS 3920", "New venture and Small Business Management", 3),
        Course("AP/ADMS 2320", "Business Statistics", 3)
    ]
    add_courses(business_minor, bs_required, "required")

    bs_electives = [
        Course("AP/ADMS 3530", "Finance", 3),
        Course("AP/ADMS 4370", "Data Analysis Systems", 3)
    ]
    add_courses(business_minor, bs_electives, "electives")

    # =======================
    # COMPLETED COURSES
    # =======================
    completed_courses = [
        Course("LE/EECS 1001", "Research Directions in Computing", 1),
        Course("LE/EECS 1015", "Introduction to Computer Science and Programming", 3),
        Course("LE/EECS 1019", "Discrete Mathematics for Computer Science", 3),
        Course("LE/EECS 1022", "Introduction to Object Oriented Programming", 3),
        Course("LE/EECS 2001", "Introduction to the Theory of Computation", 3),
        Course("LE/EECS 2021", "Computer Organization", 4),
        Course("LE/EECS 2030", "Advanced Object Oriented Programming", 3),
        Course("LE/EECS 2031", "Software Tools", 3),
        Course("LE/EECS 2101", "Fundamentals of Data Structures", 3),
        Course("LE/EECS 3101", "Design and Analysis of Algorithms", 3),
        Course("LE/EECS 3311", "Software Design", 3),
        Course("SC/MATH 1090", "Introduction to Logic for Computer Science", 3),
        Course("SC/MATH 1013", "Applied Calculus I", 3),
        Course("SC/MATH 1014", "Applied Calculus II", 3),
        Course("SC/MATH 2030", "Elementary Probability", 3),
        Course("LE/EECS 3000", "Professional Practice in Computing", 3),
        Course("LE/EECS 3221", "Operating System Fundamentals", 3),
        Course("LE/EECS 3401", "Introduction to AI and Logic Programming", 3),

        # At least 12 credits from EECS 4000-level
        Course("LE/EECS 4413", "Building E-Commerce Systems", 3),
        Course("LE/EECS 4482", "Network Security and Forensics", 3),
        Course("LE/EECS 4484", "Malware Analysis", 3),
        Course("LE/EECS 4080", "Computer Science Project", 3),

        # At least 12 credits outside EECS, MATH, STATS and ITEC -> satisfied under Business Minor
        Course("AP/ADMS 1000", "Introduction to Business", 3),
        Course("AP/ADMS 1010", "Exploring the Functions of Business", 3),
        Course("AP/ADMS 2541", "Introduction to Personal Finance", 3),
        Course("AP/ADMS 2200", "Introductory Marketing", 3),
        
        Course("SC/PHYS 1411", "Physics Fundamentals I", 3),
        Course("SC/PHYS 1412", "Physics Fundamentals II", 3),
        Course("AP/ECON 1000", "Introduction to Microeconomics", 3),
        Course("AP/PHIL 1100", "The Meaning of Life", 3),
        Course("AP/ECON 1010", "Introduction to Macroeconomics", 3),
        Course("FA/MUSI 1510", "The Musical Experience", 3),

        Course("SC/MATH 1025", "Applied Linear Algebra", 3),
        Course("SC/MATH 1280", "Principles of Risk Management and Insurance", 3),

        # At least 15 credits at 3000-level or higher
        Course("LE/EECS 3214", "Computer Network Protocols and Applications", 3),
        Course("LE/EECS 3481", "Applied Cryptography", 3),
        Course("LE/EECS 3482", "Introduction to Computer Security", 3),
        Course("LE/EECS 3404", "Applied Machine Learning", 3),
        Course("AP/POLS 3190", "Public Administration", 6),

        # At least 4 credits of additional electives
        Course("AP/ADMS 2400", "Introduction to Organizational Behaviour", 3)
    ]

    # Add completed courses
    for course in completed_courses:
        student.add_completed_course(course)

    return student, cs_major, business_minor
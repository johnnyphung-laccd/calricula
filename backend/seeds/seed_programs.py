"""
Calricula - Program Seed Data
Seeds sample programs (degrees and certificates) for testing.
"""

import sys
from pathlib import Path
from decimal import Decimal

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlmodel import Session, select
from app.core.database import engine
from app.models.program import Program, ProgramType, ProgramStatus, ProgramCourse, RequirementType
from app.models.course import Course
from app.models.department import Department
from app.models.user import User


# Sample programs
SEED_PROGRAMS = [
    {
        "title": "Mathematics for Transfer",
        "type": ProgramType.AAT,
        "department_code": "MATH",
        "total_units": Decimal("60.0"),
        "status": ProgramStatus.APPROVED,
        "catalog_description": "The AA-T in Mathematics prepares students for transfer to California State University to complete a bachelor's degree in mathematics or a related field. The program emphasizes calculus, linear algebra, and differential equations.",
        "program_narrative": "The Associate in Arts in Mathematics for Transfer (AA-T) degree provides students with a clear pathway to transfer to a CSU as a junior. Students completing this degree will be able to apply mathematical reasoning to solve problems and will be prepared for upper-division coursework in mathematics.",
        "top_code": "1701.00",
        "required_courses": [
            {"subject": "MATH", "number": "101", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("3.0")},
            {"subject": "MATH", "number": "201", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("4.0")},
            {"subject": "MATH", "number": "202", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("4.0")},
        ],
    },
    {
        "title": "Computer Science",
        "type": ProgramType.AS,
        "department_code": "CS",
        "total_units": Decimal("62.0"),
        "status": ProgramStatus.REVIEW,
        "catalog_description": "The AS in Computer Science provides a strong foundation in computer science fundamentals. Students learn programming, data structures, algorithms, and software development practices.",
        "program_narrative": "The Associate in Science in Computer Science degree prepares students for transfer to a four-year institution or entry-level positions in the technology industry. Students develop skills in programming, data structures, and software development. This is a high-unit major approved by the LACCD Board.",
        "top_code": "0707.00",
        "required_courses": [
            {"subject": "CS", "number": "101", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("3.0")},
            {"subject": "CS", "number": "201", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("3.0")},
            {"subject": "CS", "number": "301", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("3.0")},
            {"subject": "MATH", "number": "201", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("4.0")},
        ],
    },
    {
        "title": "Business Administration Certificate",
        "type": ProgramType.CERTIFICATE,
        "department_code": "BUS",
        "total_units": Decimal("18.0"),
        "status": ProgramStatus.APPROVED,
        "catalog_description": "This certificate covers essential business topics including management, marketing, accounting, and business law. Prepares students for entry-level business positions.",
        "program_narrative": "The Certificate of Achievement in Business Administration provides students with foundational knowledge in business principles. This certificate is designed for students seeking entry-level positions or career advancement in business.",
        "top_code": "0505.00",
        "required_courses": [
            {"subject": "BUS", "number": "101", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("3.0")},
        ],
    },
    {
        "title": "Psychology for Transfer",
        "type": ProgramType.AAT,
        "department_code": "PSYCH",
        "total_units": Decimal("60.0"),
        "status": ProgramStatus.DRAFT,
        "catalog_description": "The AA-T in Psychology prepares students for transfer to California State University to pursue a bachelor's degree in psychology. Students study human behavior, cognition, and social processes.",
        "program_narrative": "The Associate in Arts in Psychology for Transfer (AA-T) provides a pathway for students to transfer to CSU as psychology majors. Students explore human behavior, research methods, and psychological theories.",
        "top_code": "2001.00",
        "required_courses": [
            {"subject": "PSYCH", "number": "101", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("3.0")},
        ],
    },
    {
        "title": "Web Development Certificate",
        "type": ProgramType.CERTIFICATE,
        "department_code": "CS",
        "total_units": Decimal("24.0"),
        "status": ProgramStatus.DRAFT,
        "catalog_description": "This certificate prepares students for entry-level web development positions. Students gain hands-on experience building responsive web applications.",
        "program_narrative": "The Certificate in Web Development provides students with skills in front-end and back-end web development. Students learn HTML, CSS, JavaScript, and modern web frameworks.",
        "top_code": "0707.00",
        "required_courses": [
            {"subject": "CS", "number": "101", "requirement_type": RequirementType.REQUIRED_CORE, "units": Decimal("3.0")},
            {"subject": "CS", "number": "201", "requirement_type": RequirementType.LIST_A, "units": Decimal("3.0")},
        ],
    },
]


def seed_programs():
    """
    Seed sample programs into the database.
    """
    with Session(engine) as session:
        # Get department lookup
        dept_map = {}
        departments = session.exec(select(Department)).all()
        for dept in departments:
            dept_map[dept.code] = dept.id

        # Get course lookup
        course_map = {}
        courses = session.exec(select(Course)).all()
        for course in courses:
            key = f"{course.subject_code} {course.course_number}"
            course_map[key] = course.id

        # Get a default user for created_by
        default_user = session.exec(select(User)).first()
        if not default_user:
            print("  ERROR: No users found. Run seed_users.py first.")
            return

        created_count = 0
        skipped_count = 0

        for prog_data in SEED_PROGRAMS:
            # Check if program already exists
            existing = session.exec(
                select(Program).where(Program.title == prog_data["title"])
            ).first()

            if existing:
                print(f"  Program '{prog_data['title']}' already exists, skipping")
                skipped_count += 1
                continue

            # Extract nested data
            required_courses = prog_data.pop("required_courses", [])
            dept_code = prog_data.pop("department_code", None)

            # Set department_id and created_by
            if dept_code and dept_code in dept_map:
                prog_data["department_id"] = dept_map[dept_code]
            prog_data["created_by"] = default_user.id

            # Create program
            program = Program(**prog_data)
            session.add(program)
            session.flush()  # Get the program ID

            # Create program-course relationships
            seq = 1
            for course_req in required_courses:
                course_key = f"{course_req['subject']} {course_req['number']}"
                course_id = course_map.get(course_key)

                if course_id:
                    program_course = ProgramCourse(
                        program_id=program.id,
                        course_id=course_id,
                        requirement_type=course_req["requirement_type"],
                        sequence=seq,
                        units_applied=course_req.get("units", Decimal("0")),
                    )
                    session.add(program_course)
                    seq += 1
                else:
                    print(f"    Warning: Course '{course_key}' not found, skipping")

            status_str = prog_data.get("status", ProgramStatus.DRAFT).value
            print(f"  Created program: {prog_data['title']} ({prog_data['type'].value}, {prog_data['total_units']} units, {status_str})")
            created_count += 1

        session.commit()
        print(f"\nSeeded {created_count} programs ({skipped_count} already existed)")


if __name__ == "__main__":
    print("Seeding programs...")
    print("NOTE: Run seed_departments.py, seed_users.py, and seed_courses.py first")
    seed_programs()
    print("Done!")

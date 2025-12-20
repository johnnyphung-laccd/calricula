"""
Calricula - Course Seed Data
Seeds sample courses in various statuses for testing.
"""

import sys
from pathlib import Path
from decimal import Decimal

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlmodel import Session, select
from app.core.database import engine
from app.models.course import Course, CourseStatus, StudentLearningOutcome, BloomLevel, CourseContent
from app.models.department import Department
from app.models.user import User


# Sample courses with realistic data
SEED_COURSES = [
    # ================== APPROVED COURSES (5) ==================
    {
        "subject_code": "MATH",
        "course_number": "101",
        "title": "College Algebra",
        "units": Decimal("3.0"),
        "lecture_hours": 54,
        "lab_hours": 0,
        "homework_hours": 108,
        "total_student_hours": 162,
        "status": CourseStatus.APPROVED,
        "catalog_description": "Fundamental algebraic concepts including polynomial, rational, exponential, and logarithmic functions. Topics include equations and inequalities, graphing techniques, and applications to real-world problems. Prepares students for calculus and STEM courses.",
        "effective_term": "Fall 2024",
        "ccn_id": "MATH C1051",
        "department_code": "MATH",
        "slos": [
            {"sequence": 1, "outcome_text": "Analyze and graph polynomial, rational, exponential, and logarithmic functions", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 2, "outcome_text": "Solve equations and inequalities using algebraic methods", "bloom_level": BloomLevel.APPLY},
            {"sequence": 3, "outcome_text": "Apply algebraic concepts to model and solve real-world problems", "bloom_level": BloomLevel.APPLY},
            {"sequence": 4, "outcome_text": "Evaluate functions and perform operations on functions including composition", "bloom_level": BloomLevel.EVALUATE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Equations and Inequalities", "subtopics": ["Linear equations", "Quadratic equations", "Polynomial equations", "Rational equations"], "hours_allocated": Decimal("9")},
            {"sequence": 2, "topic": "Functions and Graphs", "subtopics": ["Function notation", "Domain and range", "Graphing techniques", "Transformations"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Polynomial Functions", "subtopics": ["Graphing polynomials", "Zeros and factoring", "Division algorithms"], "hours_allocated": Decimal("9")},
            {"sequence": 4, "topic": "Rational Functions", "subtopics": ["Graphing rational functions", "Asymptotes", "Solving rational equations"], "hours_allocated": Decimal("9")},
            {"sequence": 5, "topic": "Exponential and Logarithmic Functions", "subtopics": ["Exponential functions", "Logarithmic functions", "Applications"], "hours_allocated": Decimal("12")},
            {"sequence": 6, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("3")},
        ],
    },
    {
        "subject_code": "ENGL",
        "course_number": "101",
        "title": "English Composition",
        "units": Decimal("3.0"),
        "lecture_hours": 54,
        "lab_hours": 0,
        "homework_hours": 108,
        "total_student_hours": 162,
        "status": CourseStatus.APPROVED,
        "catalog_description": "Instruction in expository writing with emphasis on clear, effective prose. Students develop skills in critical reading, thesis development, essay organization, and revision. Includes introduction to research and MLA documentation.",
        "effective_term": "Fall 2024",
        "ccn_id": "ENGL C1000",
        "department_code": "ENGL",
        "slos": [
            {"sequence": 1, "outcome_text": "Compose essays demonstrating clear thesis statements and logical organization", "bloom_level": BloomLevel.CREATE},
            {"sequence": 2, "outcome_text": "Apply revision strategies to improve clarity, coherence, and style", "bloom_level": BloomLevel.APPLY},
            {"sequence": 3, "outcome_text": "Integrate and document sources following MLA format", "bloom_level": BloomLevel.APPLY},
            {"sequence": 4, "outcome_text": "Analyze texts for rhetorical strategies and effectiveness", "bloom_level": BloomLevel.ANALYZE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "The Writing Process", "subtopics": ["Prewriting", "Drafting", "Revision", "Editing"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Essay Structure and Organization", "subtopics": ["Thesis statements", "Introduction", "Body paragraphs", "Conclusion"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Critical Reading", "subtopics": ["Annotation", "Summary", "Analysis", "Response"], "hours_allocated": Decimal("9")},
            {"sequence": 4, "topic": "Research and Documentation", "subtopics": ["Finding sources", "Evaluating sources", "MLA format", "Avoiding plagiarism"], "hours_allocated": Decimal("12")},
            {"sequence": 5, "topic": "Rhetorical Analysis", "subtopics": ["Audience", "Purpose", "Tone", "Persuasive techniques"], "hours_allocated": Decimal("12")},
            {"sequence": 6, "topic": "Grammar and Style", "subtopics": ["Sentence structure", "Word choice", "Common errors"], "hours_allocated": Decimal("3")},
        ],
    },
    {
        "subject_code": "PSYCH",
        "course_number": "101",
        "title": "Introduction to Psychology",
        "units": Decimal("3.0"),
        "lecture_hours": 54,
        "lab_hours": 0,
        "homework_hours": 108,
        "total_student_hours": 162,
        "status": CourseStatus.APPROVED,
        "catalog_description": "Survey of psychology as a behavioral science. Topics include research methods, biological bases of behavior, sensation, perception, learning, memory, development, personality, psychological disorders, and social psychology.",
        "effective_term": "Fall 2024",
        "ccn_id": "PSYC C1000",
        "department_code": "PSYCH",
        "slos": [
            {"sequence": 1, "outcome_text": "Describe the scientific method as applied to psychological research", "bloom_level": BloomLevel.UNDERSTAND},
            {"sequence": 2, "outcome_text": "Explain biological and environmental factors influencing behavior", "bloom_level": BloomLevel.UNDERSTAND},
            {"sequence": 3, "outcome_text": "Compare and contrast major psychological perspectives", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 4, "outcome_text": "Apply psychological principles to analyze real-world situations", "bloom_level": BloomLevel.APPLY},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Introduction and Research Methods", "subtopics": ["History of psychology", "Scientific method", "Research ethics"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Biological Bases of Behavior", "subtopics": ["Neurons", "Brain structure", "Neurotransmitters"], "hours_allocated": Decimal("6")},
            {"sequence": 3, "topic": "Sensation and Perception", "subtopics": ["Vision", "Hearing", "Perception processes"], "hours_allocated": Decimal("6")},
            {"sequence": 4, "topic": "Learning and Memory", "subtopics": ["Classical conditioning", "Operant conditioning", "Memory processes"], "hours_allocated": Decimal("9")},
            {"sequence": 5, "topic": "Development", "subtopics": ["Cognitive development", "Social development", "Lifespan changes"], "hours_allocated": Decimal("6")},
            {"sequence": 6, "topic": "Personality and Disorders", "subtopics": ["Personality theories", "Psychological disorders", "Treatment approaches"], "hours_allocated": Decimal("12")},
            {"sequence": 7, "topic": "Social Psychology", "subtopics": ["Social influence", "Attitudes", "Group behavior"], "hours_allocated": Decimal("6")},
            {"sequence": 8, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("3")},
        ],
    },
    {
        "subject_code": "CS",
        "course_number": "101",
        "title": "Introduction to Computer Science",
        "units": Decimal("3.0"),
        "lecture_hours": 36,
        "lab_hours": 54,
        "homework_hours": 72,
        "total_student_hours": 162,
        "status": CourseStatus.APPROVED,
        "catalog_description": "Introduction to programming concepts and problem-solving using Python. Topics include variables, control structures, functions, data structures, and object-oriented programming. Emphasizes computational thinking and algorithm design.",
        "effective_term": "Fall 2024",
        "department_code": "CS",
        "slos": [
            {"sequence": 1, "outcome_text": "Design algorithms to solve computational problems", "bloom_level": BloomLevel.CREATE},
            {"sequence": 2, "outcome_text": "Implement programs using variables, control structures, and functions", "bloom_level": BloomLevel.APPLY},
            {"sequence": 3, "outcome_text": "Debug and test programs systematically", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 4, "outcome_text": "Apply object-oriented principles to organize code", "bloom_level": BloomLevel.APPLY},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Introduction to Programming", "subtopics": ["Python basics", "Variables", "Data types", "Input/output"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Control Structures", "subtopics": ["Conditionals", "Loops", "Boolean logic"], "hours_allocated": Decimal("9")},
            {"sequence": 3, "topic": "Functions", "subtopics": ["Function definition", "Parameters", "Return values", "Scope"], "hours_allocated": Decimal("9")},
            {"sequence": 4, "topic": "Data Structures", "subtopics": ["Lists", "Dictionaries", "Strings", "File I/O"], "hours_allocated": Decimal("12")},
            {"sequence": 5, "topic": "Object-Oriented Programming", "subtopics": ["Classes", "Objects", "Inheritance"], "hours_allocated": Decimal("12")},
            {"sequence": 6, "topic": "Problem Solving", "subtopics": ["Algorithm design", "Debugging", "Testing"], "hours_allocated": Decimal("6")},
        ],
    },
    {
        "subject_code": "BIOL",
        "course_number": "101",
        "title": "General Biology",
        "units": Decimal("4.0"),
        "lecture_hours": 54,
        "lab_hours": 54,
        "homework_hours": 108,
        "total_student_hours": 216,
        "status": CourseStatus.APPROVED,
        "catalog_description": "Introduction to biological principles for science majors. Topics include cell biology, genetics, molecular biology, evolution, and ecology. Laboratory emphasizes scientific method, data analysis, and experimental techniques.",
        "effective_term": "Fall 2024",
        "ccn_id": "BIOL C1000",
        "department_code": "BIOL",
        "slos": [
            {"sequence": 1, "outcome_text": "Describe the structure and function of cells and their components", "bloom_level": BloomLevel.UNDERSTAND},
            {"sequence": 2, "outcome_text": "Explain the principles of genetics and inheritance", "bloom_level": BloomLevel.UNDERSTAND},
            {"sequence": 3, "outcome_text": "Analyze evidence supporting evolution by natural selection", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 4, "outcome_text": "Design and conduct laboratory experiments using proper techniques", "bloom_level": BloomLevel.CREATE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Introduction to Biology", "subtopics": ["Scientific method", "Characteristics of life", "Chemistry of life"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Cell Biology", "subtopics": ["Cell structure", "Membrane transport", "Cell division"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Genetics", "subtopics": ["Mendelian genetics", "DNA structure", "Gene expression"], "hours_allocated": Decimal("12")},
            {"sequence": 4, "topic": "Evolution", "subtopics": ["Natural selection", "Evidence for evolution", "Speciation"], "hours_allocated": Decimal("12")},
            {"sequence": 5, "topic": "Ecology", "subtopics": ["Ecosystems", "Population ecology", "Conservation"], "hours_allocated": Decimal("9")},
            {"sequence": 6, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("3")},
        ],
    },

    # ================== IN REVIEW COURSES (5) ==================
    {
        "subject_code": "MATH",
        "course_number": "201",
        "title": "Calculus I",
        "units": Decimal("4.0"),
        "lecture_hours": 72,
        "lab_hours": 0,
        "homework_hours": 144,
        "total_student_hours": 216,
        "status": CourseStatus.CURRICULUM_COMMITTEE,
        "catalog_description": "Introduction to differential and integral calculus. Topics include limits, continuity, derivatives, applications of derivatives, antiderivatives, and the Fundamental Theorem of Calculus. Includes transcendental functions.",
        "ccn_id": "MATH C1051",
        "department_code": "MATH",
        "slos": [
            {"sequence": 1, "outcome_text": "Evaluate limits using algebraic, graphical, and numerical techniques", "bloom_level": BloomLevel.EVALUATE},
            {"sequence": 2, "outcome_text": "Calculate derivatives using the definition and derivative rules", "bloom_level": BloomLevel.APPLY},
            {"sequence": 3, "outcome_text": "Apply derivatives to related rates and optimization problems", "bloom_level": BloomLevel.APPLY},
            {"sequence": 4, "outcome_text": "Evaluate definite and indefinite integrals using substitution", "bloom_level": BloomLevel.EVALUATE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Limits and Continuity", "subtopics": ["Definition of limits", "Limit laws", "Continuity"], "hours_allocated": Decimal("12")},
            {"sequence": 2, "topic": "Derivatives", "subtopics": ["Definition", "Derivative rules", "Chain rule"], "hours_allocated": Decimal("18")},
            {"sequence": 3, "topic": "Applications of Derivatives", "subtopics": ["Related rates", "Optimization", "Curve sketching"], "hours_allocated": Decimal("18")},
            {"sequence": 4, "topic": "Integration", "subtopics": ["Antiderivatives", "Definite integrals", "Fundamental theorem"], "hours_allocated": Decimal("18")},
            {"sequence": 5, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("6")},
        ],
    },
    {
        "subject_code": "ENGL",
        "course_number": "102",
        "title": "Critical Thinking and Composition",
        "units": Decimal("3.0"),
        "lecture_hours": 54,
        "lab_hours": 0,
        "homework_hours": 108,
        "total_student_hours": 162,
        "status": CourseStatus.DEPT_REVIEW,
        "catalog_description": "Instruction in argumentation and critical thinking through written discourse. Students analyze arguments, identify logical fallacies, evaluate evidence, and construct well-reasoned arguments on complex issues.",
        "ccn_id": "ENGL C1002",
        "department_code": "ENGL",
        "slos": [
            {"sequence": 1, "outcome_text": "Analyze arguments for validity and rhetorical effectiveness", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 2, "outcome_text": "Construct well-reasoned arguments supported by evidence", "bloom_level": BloomLevel.CREATE},
            {"sequence": 3, "outcome_text": "Identify logical fallacies and cognitive biases", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 4, "outcome_text": "Synthesize multiple perspectives on complex issues", "bloom_level": BloomLevel.EVALUATE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Introduction to Argument", "subtopics": ["Claims", "Evidence", "Warrants"], "hours_allocated": Decimal("9")},
            {"sequence": 2, "topic": "Logical Reasoning", "subtopics": ["Deductive reasoning", "Inductive reasoning", "Fallacies"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Evaluating Evidence", "subtopics": ["Sources", "Data", "Expert testimony"], "hours_allocated": Decimal("9")},
            {"sequence": 4, "topic": "Argumentation", "subtopics": ["Building arguments", "Counterarguments", "Synthesis"], "hours_allocated": Decimal("18")},
            {"sequence": 5, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("6")},
        ],
    },
    {
        "subject_code": "CS",
        "course_number": "201",
        "title": "Data Structures",
        "units": Decimal("3.0"),
        "lecture_hours": 36,
        "lab_hours": 54,
        "homework_hours": 72,
        "total_student_hours": 162,
        "status": CourseStatus.ARTICULATION_REVIEW,
        "catalog_description": "Study of fundamental data structures and their applications. Topics include arrays, linked lists, stacks, queues, trees, graphs, hash tables, and sorting algorithms. Emphasizes algorithm analysis and efficient implementation.",
        "department_code": "CS",
        "slos": [
            {"sequence": 1, "outcome_text": "Implement fundamental data structures in a programming language", "bloom_level": BloomLevel.APPLY},
            {"sequence": 2, "outcome_text": "Analyze time and space complexity of algorithms", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 3, "outcome_text": "Select appropriate data structures for specific problems", "bloom_level": BloomLevel.EVALUATE},
            {"sequence": 4, "outcome_text": "Design efficient algorithms using standard techniques", "bloom_level": BloomLevel.CREATE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Arrays and Linked Lists", "subtopics": ["Array operations", "Linked list types", "Comparison"], "hours_allocated": Decimal("9")},
            {"sequence": 2, "topic": "Stacks and Queues", "subtopics": ["Stack operations", "Queue operations", "Applications"], "hours_allocated": Decimal("9")},
            {"sequence": 3, "topic": "Trees", "subtopics": ["Binary trees", "BST", "Balanced trees"], "hours_allocated": Decimal("12")},
            {"sequence": 4, "topic": "Graphs", "subtopics": ["Graph representation", "Traversals", "Shortest paths"], "hours_allocated": Decimal("12")},
            {"sequence": 5, "topic": "Hash Tables", "subtopics": ["Hash functions", "Collision handling", "Applications"], "hours_allocated": Decimal("6")},
            {"sequence": 6, "topic": "Sorting and Analysis", "subtopics": ["Sorting algorithms", "Big-O notation", "Analysis"], "hours_allocated": Decimal("6")},
        ],
    },
    {
        "subject_code": "ART",
        "course_number": "101",
        "title": "Introduction to Art",
        "units": Decimal("3.0"),
        "lecture_hours": 54,
        "lab_hours": 0,
        "homework_hours": 108,
        "total_student_hours": 162,
        "status": CourseStatus.DEPT_REVIEW,
        "catalog_description": "Survey of visual arts from prehistoric to contemporary times. Students develop visual literacy and critical vocabulary for analyzing art across cultures. Explores the relationship between art and society.",
        "department_code": "ART",
        "slos": [
            {"sequence": 1, "outcome_text": "Identify major art movements and their characteristics", "bloom_level": BloomLevel.REMEMBER},
            {"sequence": 2, "outcome_text": "Analyze artworks using formal elements and principles of design", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 3, "outcome_text": "Evaluate art in its historical and cultural context", "bloom_level": BloomLevel.EVALUATE},
            {"sequence": 4, "outcome_text": "Apply critical vocabulary to discuss visual art", "bloom_level": BloomLevel.APPLY},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Elements and Principles of Art", "subtopics": ["Line", "Shape", "Color", "Composition"], "hours_allocated": Decimal("9")},
            {"sequence": 2, "topic": "Ancient and Medieval Art", "subtopics": ["Prehistoric", "Egyptian", "Greek", "Medieval"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Renaissance to Baroque", "subtopics": ["Italian Renaissance", "Northern Renaissance", "Baroque"], "hours_allocated": Decimal("9")},
            {"sequence": 4, "topic": "19th Century Art", "subtopics": ["Romanticism", "Impressionism", "Post-Impressionism"], "hours_allocated": Decimal("9")},
            {"sequence": 5, "topic": "Modern and Contemporary Art", "subtopics": ["Modernism", "Abstract", "Contemporary"], "hours_allocated": Decimal("12")},
            {"sequence": 6, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("3")},
        ],
    },
    {
        "subject_code": "BUS",
        "course_number": "101",
        "title": "Introduction to Business",
        "units": Decimal("3.0"),
        "lecture_hours": 54,
        "lab_hours": 0,
        "homework_hours": 108,
        "total_student_hours": 162,
        "status": CourseStatus.CURRICULUM_COMMITTEE,
        "catalog_description": "Overview of business principles and practices. Topics include management, marketing, finance, accounting, and business ethics. Explores entrepreneurship and career opportunities in the business world.",
        "department_code": "BUS",
        "slos": [
            {"sequence": 1, "outcome_text": "Describe the functions of management in business organizations", "bloom_level": BloomLevel.UNDERSTAND},
            {"sequence": 2, "outcome_text": "Explain marketing principles and their application", "bloom_level": BloomLevel.UNDERSTAND},
            {"sequence": 3, "outcome_text": "Analyze financial statements and basic accounting concepts", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 4, "outcome_text": "Evaluate ethical considerations in business decisions", "bloom_level": BloomLevel.EVALUATE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Introduction to Business", "subtopics": ["Economic systems", "Business types", "Environment"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Management", "subtopics": ["Planning", "Organizing", "Leading", "Controlling"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Marketing", "subtopics": ["Marketing mix", "Consumer behavior", "Strategy"], "hours_allocated": Decimal("12")},
            {"sequence": 4, "topic": "Finance and Accounting", "subtopics": ["Financial statements", "Budgeting", "Investment"], "hours_allocated": Decimal("12")},
            {"sequence": 5, "topic": "Ethics and Social Responsibility", "subtopics": ["Business ethics", "CSR", "Sustainability"], "hours_allocated": Decimal("9")},
            {"sequence": 6, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("3")},
        ],
    },

    # ================== DRAFT COURSES (5) ==================
    {
        "subject_code": "MATH",
        "course_number": "202",
        "title": "Calculus II",
        "units": Decimal("4.0"),
        "lecture_hours": 72,
        "lab_hours": 0,
        "homework_hours": 144,
        "total_student_hours": 216,
        "status": CourseStatus.DRAFT,
        "catalog_description": "Continuation of Calculus I. Topics include techniques of integration, applications of integration, infinite sequences and series, parametric equations, and polar coordinates.",
        "ccn_id": "MATH C1052",
        "department_code": "MATH",
        "slos": [
            {"sequence": 1, "outcome_text": "Apply integration techniques to evaluate complex integrals", "bloom_level": BloomLevel.APPLY},
            {"sequence": 2, "outcome_text": "Calculate areas, volumes, and arc lengths using integration", "bloom_level": BloomLevel.APPLY},
            {"sequence": 3, "outcome_text": "Analyze convergence of infinite series", "bloom_level": BloomLevel.ANALYZE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Integration Techniques", "subtopics": ["By parts", "Trigonometric", "Partial fractions"], "hours_allocated": Decimal("18")},
            {"sequence": 2, "topic": "Applications of Integration", "subtopics": ["Area", "Volume", "Arc length"], "hours_allocated": Decimal("18")},
            {"sequence": 3, "topic": "Sequences and Series", "subtopics": ["Sequences", "Series", "Convergence tests"], "hours_allocated": Decimal("24")},
            {"sequence": 4, "topic": "Parametric and Polar", "subtopics": ["Parametric curves", "Polar coordinates"], "hours_allocated": Decimal("9")},
            {"sequence": 5, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("3")},
        ],
    },
    {
        "subject_code": "CS",
        "course_number": "301",
        "title": "Database Systems",
        "units": Decimal("3.0"),
        "lecture_hours": 36,
        "lab_hours": 54,
        "homework_hours": 72,
        "total_student_hours": 162,
        "status": CourseStatus.DRAFT,
        "catalog_description": "Introduction to database design and management. Topics include relational model, SQL, normalization, and database administration. Students design and implement database solutions.",
        "department_code": "CS",
        "slos": [],  # Needs SLOs - demonstrating incomplete draft
        "content_items": [
            {"sequence": 1, "topic": "Database Concepts", "subtopics": ["Data models", "DBMS", "Architecture"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Relational Model", "subtopics": ["Relations", "Keys", "Integrity"], "hours_allocated": Decimal("9")},
            {"sequence": 3, "topic": "SQL", "subtopics": ["DDL", "DML", "Queries", "Joins"], "hours_allocated": Decimal("18")},
            {"sequence": 4, "topic": "Database Design", "subtopics": ["ER modeling", "Normalization", "Implementation"], "hours_allocated": Decimal("18")},
            {"sequence": 5, "topic": "Administration", "subtopics": ["Security", "Backup", "Performance"], "hours_allocated": Decimal("3")},
        ],
    },
    {
        "subject_code": "NURS",
        "course_number": "101",
        "title": "Fundamentals of Nursing",
        "units": Decimal("6.0"),
        "lecture_hours": 54,
        "lab_hours": 54,
        "activity_hours": 108,
        "homework_hours": 108,
        "total_student_hours": 324,
        "status": CourseStatus.DRAFT,
        "catalog_description": "Introduction to nursing theory and practice. Topics include patient assessment, basic nursing skills, medication administration, and professional responsibilities. Clinical experience in healthcare settings.",
        "department_code": "NURS",
        "slos": [
            {"sequence": 1, "outcome_text": "Perform systematic patient assessments", "bloom_level": BloomLevel.APPLY},
            {"sequence": 2, "outcome_text": "Demonstrate safe medication administration techniques", "bloom_level": BloomLevel.APPLY},
            {"sequence": 3, "outcome_text": "Apply infection control principles in clinical settings", "bloom_level": BloomLevel.APPLY},
            {"sequence": 4, "outcome_text": "Communicate effectively with patients and healthcare team", "bloom_level": BloomLevel.APPLY},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Introduction to Nursing", "subtopics": ["Nursing history", "Nursing process", "Ethics"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Patient Assessment", "subtopics": ["Health history", "Physical exam", "Documentation"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Basic Skills", "subtopics": ["Hygiene", "Mobility", "Vital signs"], "hours_allocated": Decimal("12")},
            {"sequence": 4, "topic": "Medication Administration", "subtopics": ["Pharmacology basics", "Routes", "Safety"], "hours_allocated": Decimal("12")},
            {"sequence": 5, "topic": "Clinical Practice", "subtopics": ["Clinical rotations", "Skills lab", "Simulation"], "hours_allocated": Decimal("12")},
        ],
    },
    {
        "subject_code": "HIST",
        "course_number": "101",
        "title": "U.S. History to 1877",
        "units": Decimal("3.0"),
        "lecture_hours": 54,
        "lab_hours": 0,
        "homework_hours": 108,
        "total_student_hours": 162,
        "status": CourseStatus.DRAFT,
        "catalog_description": "Survey of American history from pre-Columbian times through Reconstruction. Examines political, social, economic, and cultural developments including diverse perspectives and experiences.",
        "ccn_id": "HIST C1010",
        "department_code": "HIST",
        "slos": [
            {"sequence": 1, "outcome_text": "Analyze primary sources from American history", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 2, "outcome_text": "Evaluate causes and effects of major historical events", "bloom_level": BloomLevel.EVALUATE},
            {"sequence": 3, "outcome_text": "Compare perspectives of diverse groups in American history", "bloom_level": BloomLevel.ANALYZE},
            {"sequence": 4, "outcome_text": "Construct historical arguments using evidence", "bloom_level": BloomLevel.CREATE},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Pre-Columbian America", "subtopics": ["Indigenous peoples", "Culture areas", "Societies"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Colonization", "subtopics": ["European exploration", "Colonial development", "Slavery"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Revolution and New Nation", "subtopics": ["Causes", "War", "Constitution"], "hours_allocated": Decimal("12")},
            {"sequence": 4, "topic": "Antebellum America", "subtopics": ["Expansion", "Reform", "Sectionalism"], "hours_allocated": Decimal("12")},
            {"sequence": 5, "topic": "Civil War and Reconstruction", "subtopics": ["Causes", "War", "Reconstruction"], "hours_allocated": Decimal("9")},
            {"sequence": 6, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("3")},
        ],
    },
    {
        "subject_code": "CHEM",
        "course_number": "101",
        "title": "General Chemistry I",
        "units": Decimal("5.0"),
        "lecture_hours": 54,
        "lab_hours": 108,
        "homework_hours": 108,
        "total_student_hours": 270,
        "status": CourseStatus.DRAFT,
        "catalog_description": "First semester of general chemistry for science majors. Topics include atomic structure, chemical bonding, stoichiometry, states of matter, and thermochemistry. Laboratory emphasizes quantitative techniques.",
        "ccn_id": "CHEM C1001",
        "department_code": "CHEM",
        "slos": [
            {"sequence": 1, "outcome_text": "Apply stoichiometry to solve quantitative chemistry problems", "bloom_level": BloomLevel.APPLY},
            {"sequence": 2, "outcome_text": "Describe atomic structure and periodic trends", "bloom_level": BloomLevel.UNDERSTAND},
            {"sequence": 3, "outcome_text": "Predict molecular geometry and bonding characteristics", "bloom_level": BloomLevel.APPLY},
            {"sequence": 4, "outcome_text": "Perform laboratory experiments using proper safety procedures", "bloom_level": BloomLevel.APPLY},
        ],
        "content_items": [
            {"sequence": 1, "topic": "Introduction to Chemistry", "subtopics": ["Matter", "Measurements", "Significant figures"], "hours_allocated": Decimal("6")},
            {"sequence": 2, "topic": "Atomic Structure", "subtopics": ["Atomic theory", "Electron configuration", "Periodic trends"], "hours_allocated": Decimal("12")},
            {"sequence": 3, "topic": "Chemical Bonding", "subtopics": ["Ionic bonding", "Covalent bonding", "Molecular geometry"], "hours_allocated": Decimal("12")},
            {"sequence": 4, "topic": "Stoichiometry", "subtopics": ["Moles", "Chemical equations", "Limiting reagents"], "hours_allocated": Decimal("12")},
            {"sequence": 5, "topic": "States of Matter", "subtopics": ["Gases", "Liquids", "Solids"], "hours_allocated": Decimal("9")},
            {"sequence": 6, "topic": "Review and Assessment", "subtopics": ["Midterm review", "Final review"], "hours_allocated": Decimal("3")},
        ],
    },
]


def seed_courses():
    """
    Seed sample courses into the database.
    """
    with Session(engine) as session:
        # Get department lookup
        dept_map = {}
        departments = session.exec(select(Department)).all()
        for dept in departments:
            dept_map[dept.code] = dept.id

        # Get user lookup by department for assigning course ownership
        # This ensures courses are created by faculty in the appropriate department
        user_by_dept = {}
        users = session.exec(select(User)).all()
        for user in users:
            if user.department_id:
                # Find department code for this user's department
                for dept in departments:
                    if dept.id == user.department_id:
                        user_by_dept[dept.code] = user
                        break

        # Get a default user (preferably the MATH faculty for test purposes)
        default_user = user_by_dept.get("MATH") or (users[0] if users else None)
        if not default_user:
            print("  ERROR: No users found. Run seed_users.py first.")
            return

        created_count = 0
        skipped_count = 0

        for course_data in SEED_COURSES:
            # Check if course already exists
            existing = session.exec(
                select(Course).where(
                    Course.subject_code == course_data["subject_code"],
                    Course.course_number == course_data["course_number"]
                )
            ).first()

            if existing:
                print(f"  Course '{course_data['subject_code']} {course_data['course_number']}' already exists, skipping")
                skipped_count += 1
                continue

            # Extract nested data
            slos_data = course_data.pop("slos", [])
            content_data = course_data.pop("content_items", [])
            dept_code = course_data.pop("department_code", None)

            # Set department_id and created_by
            # Assign course to the faculty member in the same department if available
            if dept_code and dept_code in dept_map:
                course_data["department_id"] = dept_map[dept_code]
                # Use department-specific faculty if available, otherwise default
                course_owner = user_by_dept.get(dept_code, default_user)
                course_data["created_by"] = course_owner.id
            else:
                course_data["created_by"] = default_user.id

            # Create course
            course = Course(**course_data)
            session.add(course)
            session.flush()  # Get the course ID

            # Create SLOs
            for slo_data in slos_data:
                slo_data["course_id"] = course.id
                slo = StudentLearningOutcome(**slo_data)
                session.add(slo)

            # Create content items
            for content_item_data in content_data:
                content_item_data["course_id"] = course.id
                content_item = CourseContent(**content_item_data)
                session.add(content_item)

            status_str = course_data.get("status", CourseStatus.DRAFT).value if isinstance(course_data.get("status"), CourseStatus) else str(course_data.get("status", "Draft"))
            print(f"  Created course: {course_data['subject_code']} {course_data['course_number']} - {course_data['title']} ({status_str})")
            created_count += 1

        session.commit()
        print(f"\nSeeded {created_count} courses ({skipped_count} already existed)")


if __name__ == "__main__":
    print("Seeding courses...")
    print("NOTE: Run seed_departments.py and seed_users.py first")
    seed_courses()
    print("Done!")

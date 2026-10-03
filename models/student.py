import uuid
from datetime import datetime


GRADE_SCALE = [
    (90, 100, "O",  "Outstanding"),
    (80,  89, "A+", "Excellent"),
    (70,  79, "A",  "Very Good"),
    (60,  69, "B",  "Good"),
    (50,  59, "C",  "Average"),
    (40,  49, "D",  "Below Average"),
    (0,   39, "F",  "Fail"),
]

DEFAULT_SUBJECTS = ["Mathematics", "Science", "English", "Social Studies", "Computer Science", "Hindi"]


class Student:
    def __init__(self, name, roll_number, subjects=None, marks=None,
                 student_id=None, dob=None, division=None, academic_year=None):
        self.student_id = student_id or str(uuid.uuid4())[:8].upper()
        self.name = name
        self.roll_number = int(roll_number)
        self.subjects = subjects if subjects else DEFAULT_SUBJECTS[:]
        self.marks = marks if marks else {}
        self.dob = dob or ""
        self.division = division or "A"
        self.academic_year = academic_year or str(datetime.now().year)
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_marks(self, subject, mark):
        self.marks[subject] = float(mark)

    def get_total(self):
        return sum(self.marks.values())

    def get_max_total(self):
        return len(self.marks) * 100

    def get_percentage(self):
        if not self.marks:
            return 0.0
        return round((self.get_total() / self.get_max_total()) * 100, 2)

    def get_grade(self):
        pct = self.get_percentage()
        for low, high, grade, _ in GRADE_SCALE:
            if low <= pct <= high:
                return grade
        return "F"

    def get_grade_description(self):
        pct = self.get_percentage()
        for low, high, _, desc in GRADE_SCALE:
            if low <= pct <= high:
                return desc
        return "Fail"

    def is_pass(self):
        return self.get_percentage() >= 40 and all(m >= 35 for m in self.marks.values())

    def get_rank_info(self):
        return {
            "name": self.name,
            "roll": self.roll_number,
            "percentage": self.get_percentage(),
            "grade": self.get_grade(),
        }

    def get_highest_subject(self):
        if not self.marks:
            return None, 0
        subj = max(self.marks, key=self.marks.get)
        return subj, self.marks[subj]

    def get_lowest_subject(self):
        if not self.marks:
            return None, 0
        subj = min(self.marks, key=self.marks.get)
        return subj, self.marks[subj]

    def to_dict(self):
        d = {
            "student_id": self.student_id,
            "name": self.name,
            "roll_number": self.roll_number,
            "dob": self.dob,
            "division": self.division,
            "academic_year": self.academic_year,
        }
        for subj in self.subjects:
            d[subj] = self.marks.get(subj, "")
        return d

    @classmethod
    def from_dict(cls, d, subjects=None):
        subj_list = subjects or DEFAULT_SUBJECTS[:]
        marks = {}
        for s in subj_list:
            if s in d and d[s] != "":
                try:
                    marks[s] = float(d[s])
                except (ValueError, TypeError):
                    pass
        return cls(
            name=d.get("name", "Unknown"),
            roll_number=d.get("roll_number", 0),
            subjects=subj_list,
            marks=marks,
            student_id=d.get("student_id"),
            dob=d.get("dob", ""),
            division=d.get("division", "A"),
            academic_year=d.get("academic_year", str(datetime.now().year)),
        )

    def __repr__(self):
        return f"Student(name={self.name!r}, roll={self.roll_number}, pct={self.get_percentage()}%)"

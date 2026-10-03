import csv
import os
from models.student import Student, DEFAULT_SUBJECTS


class CSVReport:
    def __init__(self, filepath="data/students.csv"):
        self.filepath = filepath
        self.subjects = DEFAULT_SUBJECTS[:]
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def get_fieldnames(self):
        base = ["student_id", "name", "roll_number", "dob", "division", "academic_year"]
        return base + self.subjects

    def save(self, students):
        fieldnames = self.get_fieldnames()
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in students:
                row = s.to_dict()
                filtered = {k: row.get(k, "") for k in fieldnames}
                writer.writerow(filtered)
        return self.filepath

    def load(self):
        students = []
        if not os.path.exists(self.filepath):
            return students
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    s = Student.from_dict(row, subjects=self.subjects)
                    students.append(s)
                except Exception:
                    continue
        return students

    def export_result_csv(self, students, filepath):
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        fieldnames = ["rank", "student_id", "name", "roll_number", "division"] + self.subjects + [
            "total", "max_total", "percentage", "grade", "grade_desc", "result"
        ]
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            sorted_students = sorted(students, key=lambda s: s.get_percentage(), reverse=True)
            for rank, s in enumerate(sorted_students, 1):
                row = {
                    "rank": rank,
                    "student_id": s.student_id,
                    "name": s.name,
                    "roll_number": s.roll_number,
                    "division": s.division,
                }
                for subj in self.subjects:
                    row[subj] = s.marks.get(subj, "")
                row["total"] = s.get_total()
                row["max_total"] = s.get_max_total()
                row["percentage"] = f"{s.get_percentage():.2f}"
                row["grade"] = s.get_grade()
                row["grade_desc"] = s.get_grade_description()
                row["result"] = "PASS" if s.is_pass() else "FAIL"
                writer.writerow(row)
        return filepath

    def bulk_import(self, filepath):
        students = []
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    s = Student.from_dict(row, subjects=self.subjects)
                    students.append(s)
                except Exception:
                    continue
        return students

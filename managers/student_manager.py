from models.student import Student, DEFAULT_SUBJECTS


class StudentManager:
    def __init__(self):
        self._students = {}
        self.subjects = DEFAULT_SUBJECTS[:]

    @property
    def students(self):
        return list(self._students.values())

    def add_student(self, student):
        self._students[student.student_id] = student

    def get_by_id(self, sid):
        return self._students.get(sid)

    def get_by_roll(self, roll):
        for s in self._students.values():
            if s.roll_number == int(roll):
                return s
        return None

    def search_by_name(self, name):
        name_lower = name.strip().lower()
        return [s for s in self._students.values() if name_lower in s.name.lower()]

    def update_student(self, sid, **kwargs):
        student = self._students.get(sid)
        if not student:
            return False
        for key, val in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, val)
        return True

    def update_marks(self, sid, subject, mark):
        student = self._students.get(sid)
        if not student:
            return False
        student.add_marks(subject, mark)
        return True

    def delete_student(self, sid):
        if sid in self._students:
            del self._students[sid]
            return True
        return False

    def get_all_rolls(self):
        return {s.roll_number for s in self._students.values()}

    def get_sorted(self, by="percentage", ascending=False):
        def key_fn(s):
            if by == "percentage":
                return s.get_percentage()
            elif by == "name":
                return s.name.lower()
            elif by == "roll":
                return s.roll_number
            elif by == "grade":
                return s.get_percentage()
            return s.get_percentage()
        return sorted(self._students.values(), key=key_fn, reverse=not ascending)

    def get_toppers(self, n=5):
        return self.get_sorted(by="percentage", ascending=False)[:n]

    def get_pass_students(self):
        return [s for s in self._students.values() if s.is_pass()]

    def get_fail_students(self):
        return [s for s in self._students.values() if not s.is_pass()]

    def get_class_average(self):
        if not self._students:
            return 0.0
        return round(sum(s.get_percentage() for s in self._students.values()) / len(self._students), 2)

    def get_subject_averages(self):
        averages = {}
        for subj in self.subjects:
            marks_list = [s.marks[subj] for s in self._students.values() if subj in s.marks]
            averages[subj] = round(sum(marks_list) / len(marks_list), 2) if marks_list else 0.0
        return averages

    def get_highest_scorer(self):
        if not self._students:
            return None
        return max(self._students.values(), key=lambda s: s.get_percentage())

    def get_lowest_scorer(self):
        if not self._students:
            return None
        return min(self._students.values(), key=lambda s: s.get_percentage())

    def get_grade_distribution(self):
        dist = {"O": 0, "A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for s in self._students.values():
            g = s.get_grade()
            if g in dist:
                dist[g] += 1
        return dist

    def get_statistics(self):
        if not self._students:
            return {}
        percentages = [s.get_percentage() for s in self._students.values()]
        return {
            "total_students": len(self._students),
            "class_average": self.get_class_average(),
            "highest_percentage": max(percentages),
            "lowest_percentage": min(percentages),
            "pass_count": len(self.get_pass_students()),
            "fail_count": len(self.get_fail_students()),
            "pass_percentage": round(len(self.get_pass_students()) / len(self._students) * 100, 2),
            "grade_distribution": self.get_grade_distribution(),
        }

    def load_from_list(self, student_list):
        for s in student_list:
            self._students[s.student_id] = s

    def count(self):
        return len(self._students)

    def is_empty(self):
        return len(self._students) == 0

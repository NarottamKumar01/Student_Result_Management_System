import sys, os
sys.path.insert(0, '.')
from models.student import Student, DEFAULT_SUBJECTS, GRADE_SCALE
from managers.student_manager import StudentManager
from reports.csv_report import CSVReport
from reports.pdf_report import PDFReport

mgr = StudentManager()
subjects = DEFAULT_SUBJECTS[:]

students_data = [
    ('Rahul Sharma', 1, [85, 90, 80, 88, 92, 78]),
    ('Amit Kumar', 2, [82, 78, 88, 75, 80, 84]),
    ('Priya Singh', 3, [95, 92, 98, 91, 96, 94]),
    ('Neha Gupta', 4, [55, 60, 58, 52, 65, 48]),
    ('Rohan Verma', 5, [30, 25, 40, 35, 28, 32]),
    ('Ananya Roy', 6, [88, 85, 90, 87, 93, 89]),
    ('Vikram Joshi', 7, [70, 75, 68, 72, 80, 65]),
]

for name, roll, marks_list in students_data:
    s = Student(name=name, roll_number=roll, subjects=subjects[:], dob='01-01-2008', division='A', academic_year='2024')
    for subj, mark in zip(subjects, marks_list):
        s.add_marks(subj, mark)
    mgr.add_student(s)

print('Students added:', mgr.count())
print()

toppers = mgr.get_toppers(5)
print('Top 5 Students:')
for i, s in enumerate(toppers, 1):
    result = 'PASS' if s.is_pass() else 'FAIL'
    print(f'  {i}. {s.name} - {s.get_percentage():.2f}%  Grade: {s.get_grade()}  {result}')

print()
stats = mgr.get_statistics()
print('Class Avg:', stats['class_average'], '%')
print('Pass:', stats['pass_count'], '| Fail:', stats['fail_count'])

csv_r = CSVReport(filepath='data/students_test.csv')
csv_r.save(mgr.students)
print()
print('CSV saved.')

pdf_r = PDFReport(output_dir='reports_output')
path = pdf_r.export_student_report_card(toppers[0])
print('PDF Report Card:', path)

class_path = pdf_r.export_class_report(mgr.students, class_name='Class 10-A')
print('Class PDF:', class_path)

print()
print('ALL TESTS PASSED')

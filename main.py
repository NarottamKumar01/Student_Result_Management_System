import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.student import Student, DEFAULT_SUBJECTS, GRADE_SCALE
from managers.student_manager import StudentManager
from reports.csv_report import CSVReport
from reports.pdf_report import PDFReport
from utils.helpers import (
    color, clear_screen, pause, print_table, center_text,
    validate_name, validate_roll, validate_marks,
    get_int_input, get_str_input, get_float_input,
    format_percentage, COLORS
)


DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "students.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports_output")

manager = StudentManager()
csv_report = CSVReport(filepath=DATA_FILE)
pdf_report = PDFReport(output_dir=OUTPUT_DIR)


def banner():
    clear_screen()
    print(color("=" * 70, "blue", "bold"))
    print(color(center_text("  STUDENT RESULT MANAGEMENT SYSTEM  ", 70), "bold", "cyan"))
    print(color(center_text("  Excel Academy — Academic Performance Tracker  ", 70), "yellow"))
    print(color("=" * 70, "blue", "bold"))
    print(color(f"  Students Loaded: {manager.count()}  |  Data: {DATA_FILE}", "magenta"))
    print(color("=" * 70, "blue", "bold"))


def main_menu():
    banner()
    print()
    print(color("  MAIN MENU", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))
    options = [
        ("1", "Add New Student"),
        ("2", "Update Student Marks"),
        ("3", "Update Student Info"),
        ("4", "Delete Student"),
        ("5", "View All Students"),
        ("6", "Search Student"),
        ("7", "Display Toppers"),
        ("8", "Class Statistics & Analytics"),
        ("9", "Save Data to CSV"),
        ("10", "Export Result CSV"),
        ("11", "Import from CSV"),
        ("12", "Export PDF Report Card"),
        ("13", "Export Full Class PDF Report"),
        ("14", "Grade Scale Reference"),
        ("0", "Exit"),
    ]
    for num, label in options:
        bullet = color(f"  [{num}]", "yellow", "bold")
        print(f"{bullet}  {color(label, 'white')}")
    print()
    return get_str_input("Enter your choice: ")


def add_student():
    banner()
    print(color("  ADD NEW STUDENT", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    while True:
        raw_name = get_str_input("Student Full Name: ")
        try:
            name = validate_name(raw_name)
            break
        except ValueError as e:
            print(color(f"  Error: {e}", "red"))

    while True:
        raw_roll = get_str_input("Roll Number: ")
        try:
            roll = validate_roll(raw_roll, existing_rolls=manager.get_all_rolls())
            break
        except ValueError as e:
            print(color(f"  Error: {e}", "red"))

    dob = get_str_input("Date of Birth (DD-MM-YYYY) [optional, press Enter to skip]: ", allow_empty=True)
    division = get_str_input("Division (e.g. A, B, C) [default A]: ", allow_empty=True) or "A"
    academic_year = get_str_input(f"Academic Year [default {DEFAULT_SUBJECTS[0][:4]}]: ", allow_empty=True) or "2024"

    print()
    print(color(f"  Subjects for {name}:", "cyan", "bold"))
    for i, s in enumerate(manager.subjects, 1):
        print(color(f"    {i}. {s}", "white"))

    marks = {}
    print(color("\n  Enter marks for each subject (0-100):", "yellow"))
    for subj in manager.subjects:
        while True:
            raw_mark = get_str_input(f"    {subj}: ")
            try:
                m = validate_marks(raw_mark)
                marks[subj] = m
                break
            except ValueError as e:
                print(color(f"    Error: {e}", "red"))

    student = Student(
        name=name,
        roll_number=roll,
        subjects=manager.subjects[:],
        marks=marks,
        dob=dob,
        division=division.upper(),
        academic_year=academic_year,
    )
    manager.add_student(student)
    csv_report.save(manager.students)

    print()
    print(color(f"  ✓ Student '{name}' added successfully! ID: {student.student_id}", "green", "bold"))
    print(color(f"  Percentage: {format_percentage(student.get_percentage())}  |  Grade: {student.get_grade()}  |  Result: {'PASS' if student.is_pass() else 'FAIL'}", "cyan"))
    pause()


def select_student_prompt(action_label="select"):
    print(color(f"\n  How to {action_label} the student?", "yellow"))
    print(color("  [1] By Roll Number", "white"))
    print(color("  [2] By Student ID", "white"))
    print(color("  [3] By Name Search", "white"))
    choice = get_str_input("Choice: ")

    student = None
    if choice == "1":
        roll = get_int_input("Roll Number: ", min_val=1)
        student = manager.get_by_roll(roll)
        if not student:
            print(color(f"  No student found with Roll Number {roll}.", "red"))
    elif choice == "2":
        sid = get_str_input("Student ID: ").upper()
        student = manager.get_by_id(sid)
        if not student:
            print(color(f"  No student found with ID {sid}.", "red"))
    elif choice == "3":
        name_query = get_str_input("Name (partial match OK): ")
        results = manager.search_by_name(name_query)
        if not results:
            print(color("  No students found.", "red"))
        elif len(results) == 1:
            student = results[0]
        else:
            print(color(f"\n  Found {len(results)} students:", "yellow"))
            for i, s in enumerate(results, 1):
                print(color(f"  [{i}] {s.name} (Roll: {s.roll_number}, ID: {s.student_id})", "white"))
            idx = get_int_input("Select number: ", min_val=1, max_val=len(results))
            student = results[idx - 1]
    else:
        print(color("  Invalid choice.", "red"))
    return student


def update_marks():
    banner()
    print(color("  UPDATE STUDENT MARKS", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students found. Please add students first.", "red"))
        pause()
        return

    student = select_student_prompt("update marks for")
    if not student:
        pause()
        return

    print(color(f"\n  Student: {student.name} | Roll: {student.roll_number} | ID: {student.student_id}", "green", "bold"))
    print(color("\n  Current Marks:", "yellow"))
    for subj in student.subjects:
        current = student.marks.get(subj, "Not entered")
        print(color(f"    {subj}: {current}", "white"))

    print(color("\n  Which subject to update?", "yellow"))
    for i, s in enumerate(student.subjects, 1):
        print(color(f"  [{i}] {s}", "white"))
    print(color("  [0] Update All Subjects", "orange"))

    choice = get_int_input("Choice: ", min_val=0, max_val=len(student.subjects))

    if choice == 0:
        print(color("\n  Enter new marks for all subjects:", "yellow"))
        for subj in student.subjects:
            while True:
                raw = get_str_input(f"    {subj} [current: {student.marks.get(subj, 'N/A')}]: ")
                try:
                    m = validate_marks(raw)
                    manager.update_marks(student.student_id, subj, m)
                    break
                except ValueError as e:
                    print(color(f"    Error: {e}", "red"))
    else:
        subj = student.subjects[choice - 1]
        while True:
            raw = get_str_input(f"  New marks for {subj} [current: {student.marks.get(subj, 'N/A')}]: ")
            try:
                m = validate_marks(raw)
                manager.update_marks(student.student_id, subj, m)
                break
            except ValueError as e:
                print(color(f"  Error: {e}", "red"))

    csv_report.save(manager.students)
    print(color(f"\n  ✓ Marks updated! New percentage: {format_percentage(student.get_percentage())} | Grade: {student.get_grade()}", "green", "bold"))
    pause()


def update_student_info():
    banner()
    print(color("  UPDATE STUDENT INFORMATION", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students found.", "red"))
        pause()
        return

    student = select_student_prompt("update info for")
    if not student:
        pause()
        return

    print(color(f"\n  Student: {student.name} | Roll: {student.roll_number}", "green", "bold"))
    print(color("  [1] Update Name", "white"))
    print(color("  [2] Update Division", "white"))
    print(color("  [3] Update Date of Birth", "white"))
    print(color("  [4] Update Academic Year", "white"))

    choice = get_str_input("Choice: ")

    if choice == "1":
        while True:
            raw_name = get_str_input(f"New Name [current: {student.name}]: ")
            try:
                new_name = validate_name(raw_name)
                manager.update_student(student.student_id, name=new_name)
                break
            except ValueError as e:
                print(color(f"  Error: {e}", "red"))
    elif choice == "2":
        new_div = get_str_input(f"New Division [current: {student.division}]: ", allow_empty=True) or student.division
        manager.update_student(student.student_id, division=new_div.upper())
    elif choice == "3":
        new_dob = get_str_input(f"New DOB [current: {student.dob}]: ", allow_empty=True) or student.dob
        manager.update_student(student.student_id, dob=new_dob)
    elif choice == "4":
        new_year = get_str_input(f"New Academic Year [current: {student.academic_year}]: ", allow_empty=True) or student.academic_year
        manager.update_student(student.student_id, academic_year=new_year)
    else:
        print(color("  Invalid choice.", "red"))
        pause()
        return

    csv_report.save(manager.students)
    print(color("\n  ✓ Student information updated successfully!", "green", "bold"))
    pause()


def delete_student():
    banner()
    print(color("  DELETE STUDENT", "bold", "red"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students found.", "red"))
        pause()
        return

    student = select_student_prompt("delete")
    if not student:
        pause()
        return

    print(color(f"\n  ⚠  You are about to delete: {student.name} (Roll: {student.roll_number}, ID: {student.student_id})", "orange", "bold"))
    confirm = get_str_input("Type 'YES' to confirm deletion: ")
    if confirm.strip() == "YES":
        manager.delete_student(student.student_id)
        csv_report.save(manager.students)
        print(color(f"\n  ✓ Student '{student.name}' has been deleted.", "green"))
    else:
        print(color("  Deletion cancelled.", "yellow"))
    pause()


def view_all_students():
    banner()
    print(color("  ALL STUDENTS", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students found. Add students to get started.", "yellow"))
        pause()
        return

    print(color("  Sort by:", "yellow"))
    print(color("  [1] Percentage (High to Low)", "white"))
    print(color("  [2] Percentage (Low to High)", "white"))
    print(color("  [3] Roll Number", "white"))
    print(color("  [4] Name (A–Z)", "white"))
    sort_choice = get_str_input("Sort choice [default 1]: ", allow_empty=True) or "1"

    sort_map = {
        "1": ("percentage", False),
        "2": ("percentage", True),
        "3": ("roll", True),
        "4": ("name", True),
    }
    sort_by, asc = sort_map.get(sort_choice, ("percentage", False))
    students = manager.get_sorted(by=sort_by, ascending=asc)

    headers = ["#", "ID", "Name", "Roll", "Div"] + [s[:4] for s in manager.subjects] + ["Total", "Pct%", "Grade", "Result"]
    rows = []
    for rank, s in enumerate(students, 1):
        row = [rank, s.student_id, s.name[:18], s.roll_number, s.division]
        for subj in manager.subjects:
            row.append(f"{s.marks.get(subj, '-')}" if s.marks.get(subj, None) is not None else "-")
        row += [
            f"{s.get_total():.0f}",
            format_percentage(s.get_percentage()),
            s.get_grade(),
            "PASS" if s.is_pass() else "FAIL"
        ]
        rows.append(row)

    print_table(headers, rows, title=f"STUDENT LIST ({len(students)} students)")
    pause()


def search_student():
    banner()
    print(color("  SEARCH STUDENT", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students available.", "yellow"))
        pause()
        return

    student = select_student_prompt("search")
    if not student:
        pause()
        return

    print()
    print(color("  " + "═" * 50, "blue"))
    print(color(f"  STUDENT PROFILE — {student.name}", "bold", "cyan"))
    print(color("  " + "═" * 50, "blue"))
    print(color(f"  ID         : {student.student_id}", "white"))
    print(color(f"  Name       : {student.name}", "white"))
    print(color(f"  Roll No    : {student.roll_number}", "white"))
    print(color(f"  Division   : {student.division}", "white"))
    print(color(f"  DOB        : {student.dob or 'N/A'}", "white"))
    print(color(f"  Acad. Year : {student.academic_year}", "white"))
    print(color("  " + "─" * 50, "blue"))
    print(color("  MARKS BREAKDOWN:", "yellow", "bold"))

    for subj in student.subjects:
        m = student.marks.get(subj)
        if m is not None:
            bar_len = int(m / 5)
            bar = color("█" * bar_len + "░" * (20 - bar_len), "green" if m >= 40 else "red")
            status = color("✓", "green") if m >= 35 else color("✗", "red")
            print(color(f"  {subj:<20}: {m:6.2f}  {bar}  {status}", "white"))
        else:
            print(color(f"  {subj:<20}: NOT ENTERED", "yellow"))

    print(color("  " + "─" * 50, "blue"))
    print(color(f"  Total Marks  : {student.get_total():.2f} / {student.get_max_total()}", "white"))
    print(color(f"  Percentage   : {format_percentage(student.get_percentage())}", "cyan", "bold"))
    print(color(f"  Grade        : {student.get_grade()} — {student.get_grade_description()}", "yellow", "bold"))
    result_c = "green" if student.is_pass() else "red"
    print(color(f"  Result       : {'PASS ✓' if student.is_pass() else 'FAIL ✗'}", result_c, "bold"))

    h_subj, h_mark = student.get_highest_subject()
    l_subj, l_mark = student.get_lowest_subject()
    if h_subj:
        print(color(f"  Best Subject : {h_subj} ({h_mark:.2f})", "green"))
    if l_subj:
        print(color(f"  Weak Subject : {l_subj} ({l_mark:.2f})", "orange"))

    print(color("  " + "═" * 50, "blue"))
    pause()


def display_toppers():
    banner()
    print(color("  TOP STUDENTS", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students available.", "yellow"))
        pause()
        return

    n = get_int_input(f"How many toppers to display? [1–{manager.count()}]: ", min_val=1, max_val=manager.count())
    toppers = manager.get_toppers(n)

    medals = ["🥇", "🥈", "🥉"]
    print()
    print(color(f"  TOP {n} STUDENTS BY PERCENTAGE", "bold", "yellow"))
    print(color("  " + "═" * 55, "blue"))
    for rank, s in enumerate(toppers, 1):
        medal = medals[rank - 1] if rank <= 3 else f"#{rank}"
        result_c = "green" if s.is_pass() else "red"
        print(color(f"  {medal}  {s.name:<22} Roll: {s.roll_number:<5}  {format_percentage(s.get_percentage()):<10}  Grade: {s.get_grade():<4}  {'PASS' if s.is_pass() else 'FAIL'}", result_c if not s.is_pass() else "white"))
    print(color("  " + "═" * 55, "blue"))
    pause()


def class_statistics():
    banner()
    print(color("  CLASS STATISTICS & ANALYTICS", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students available.", "yellow"))
        pause()
        return

    stats = manager.get_statistics()
    subj_avg = manager.get_subject_averages()
    highest = manager.get_highest_scorer()
    lowest = manager.get_lowest_scorer()

    print()
    print(color("  ▶ OVERVIEW", "yellow", "bold"))
    print(color(f"  Total Students     : {stats['total_students']}", "white"))
    print(color(f"  Class Average      : {stats['class_average']:.2f}%", "cyan"))
    print(color(f"  Highest Percentage : {stats['highest_percentage']:.2f}%", "green"))
    print(color(f"  Lowest Percentage  : {stats['lowest_percentage']:.2f}%", "orange"))
    print(color(f"  Pass Count         : {stats['pass_count']} ({stats['pass_percentage']:.2f}%)", "green"))
    print(color(f"  Fail Count         : {stats['fail_count']}", "red"))

    print()
    print(color("  ▶ TOP SCORER", "yellow", "bold"))
    if highest:
        print(color(f"  {highest.name} — {format_percentage(highest.get_percentage())} (Roll: {highest.roll_number})", "green"))

    print()
    print(color("  ▶ LOWEST SCORER", "yellow", "bold"))
    if lowest:
        print(color(f"  {lowest.name} — {format_percentage(lowest.get_percentage())} (Roll: {lowest.roll_number})", "orange"))

    print()
    print(color("  ▶ SUBJECT-WISE AVERAGES", "yellow", "bold"))
    for subj, avg in subj_avg.items():
        bar_len = int(avg / 5)
        bar = color("█" * bar_len + "░" * (20 - bar_len), "cyan")
        print(color(f"  {subj:<22}: {avg:6.2f}  {bar}", "white"))

    print()
    print(color("  ▶ GRADE DISTRIBUTION", "yellow", "bold"))
    dist = stats["grade_distribution"]
    grade_colors = {"O": "green", "A+": "green", "A": "green", "B": "blue",
                    "C": "yellow", "D": "orange", "F": "red"}
    for grade, count in dist.items():
        bar = "█" * count
        print(color(f"  Grade {grade:<3}: {count:3d}  {bar}", grade_colors.get(grade, "white")))

    pause()


def save_to_csv():
    banner()
    print(color("  SAVE DATA TO CSV", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students to save.", "yellow"))
        pause()
        return

    path = csv_report.save(manager.students)
    print(color(f"\n  ✓ Data saved to: {path}", "green", "bold"))
    print(color(f"  Total records saved: {manager.count()}", "cyan"))
    pause()


def export_result_csv():
    banner()
    print(color("  EXPORT RESULT CSV", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if manager.is_empty():
        print(color("  No students to export.", "yellow"))
        pause()
        return

    from datetime import datetime
    fname = f"ResultReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fpath = os.path.join(OUTPUT_DIR, fname)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = csv_report.export_result_csv(manager.students, fpath)
    print(color(f"\n  ✓ Result CSV exported to: {path}", "green", "bold"))
    pause()


def import_csv():
    banner()
    print(color("  IMPORT STUDENTS FROM CSV", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))
    print(color("  CSV must have columns: name, roll_number, and subject names.", "yellow"))
    print()

    fpath = get_str_input("Enter full path to CSV file: ")
    if not os.path.exists(fpath):
        print(color(f"  File not found: {fpath}", "red"))
        pause()
        return

    try:
        students = csv_report.bulk_import(fpath)
    except Exception as e:
        print(color(f"  Error reading CSV: {e}", "red"))
        pause()
        return

    existing_rolls = manager.get_all_rolls()
    added = 0
    skipped = 0
    for s in students:
        if s.roll_number in existing_rolls:
            skipped += 1
        else:
            manager.add_student(s)
            existing_rolls.add(s.roll_number)
            added += 1

    csv_report.save(manager.students)
    print(color(f"\n  ✓ Import complete! Added: {added}, Skipped (duplicate roll): {skipped}", "green", "bold"))
    pause()


def export_pdf_report_card():
    banner()
    print(color("  EXPORT PDF REPORT CARD", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if not pdf_report.is_available():
        print(color("  ⚠  reportlab library is not installed.", "orange", "bold"))
        print(color("  Run: pip install reportlab", "yellow"))
        pause()
        return

    if manager.is_empty():
        print(color("  No students found.", "yellow"))
        pause()
        return

    student = select_student_prompt("export PDF for")
    if not student:
        pause()
        return

    print(color(f"\n  Generating PDF report card for {student.name}...", "cyan"))
    try:
        path = pdf_report.export_student_report_card(student)
        print(color(f"\n  ✓ PDF report card saved to:\n  {path}", "green", "bold"))
    except Exception as e:
        print(color(f"\n  Error generating PDF: {e}", "red"))
    pause()


def export_class_pdf_report():
    banner()
    print(color("  EXPORT FULL CLASS PDF REPORT", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))

    if not pdf_report.is_available():
        print(color("  ⚠  reportlab library is not installed.", "orange", "bold"))
        print(color("  Run: pip install reportlab", "yellow"))
        pause()
        return

    if manager.is_empty():
        print(color("  No students found.", "yellow"))
        pause()
        return

    class_name = get_str_input("Class name (e.g. Class 10-A): ", allow_empty=True) or "Class X"
    print(color(f"\n  Generating PDF class report for {class_name}...", "cyan"))
    try:
        path = pdf_report.export_class_report(manager.students, class_name=class_name)
        print(color(f"\n  ✓ Class PDF report saved to:\n  {path}", "green", "bold"))
    except Exception as e:
        print(color(f"\n  Error generating PDF: {e}", "red"))
    pause()


def grade_scale_reference():
    banner()
    print(color("  GRADE SCALE REFERENCE", "bold", "cyan"))
    print(color("  " + "─" * 40, "blue"))
    headers = ["Grade", "Min%", "Max%", "Description"]
    rows = [(g, f"{lo}%", f"{hi}%", desc) for lo, hi, g, desc in GRADE_SCALE]
    print_table(headers, rows, title="GRADING SYSTEM")
    print(color("  NOTE: Pass condition requires overall ≥ 40% AND each subject ≥ 35 marks.", "yellow"))
    pause()


def load_data_on_start():
    students = csv_report.load()
    if students:
        manager.load_from_list(students)


def main():
    os.system("color") if os.name == "nt" else None
    load_data_on_start()

    handlers = {
        "1": add_student,
        "2": update_marks,
        "3": update_student_info,
        "4": delete_student,
        "5": view_all_students,
        "6": search_student,
        "7": display_toppers,
        "8": class_statistics,
        "9": save_to_csv,
        "10": export_result_csv,
        "11": import_csv,
        "12": export_pdf_report_card,
        "13": export_class_pdf_report,
        "14": grade_scale_reference,
        "0": None,
    }

    while True:
        choice = main_menu()
        if choice == "0":
            banner()
            print(color("\n  Saving data before exit...", "yellow"))
            if not manager.is_empty():
                csv_report.save(manager.students)
            print(color("  Data saved. Goodbye!\n", "green", "bold"))
            sys.exit(0)
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print(color("  Invalid option. Please try again.", "red"))
            pause()


if __name__ == "__main__":
    main()

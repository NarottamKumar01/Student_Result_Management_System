# Student Result Management System

A comprehensive, professional CLI-based Student Result Management System built in Python.

## Features

| Feature | Description |
|---|---|
| Add Student | Add with name, roll, DOB, division, academic year, and subject-wise marks |
| Update Marks | Update one or all subjects for any student |
| Update Info | Change name, division, DOB, academic year |
| Delete Student | Safe delete with confirmation |
| View All Students | Tabular view with sorting options |
| Search Student | By roll number, ID, or name (with progress bars) |
| Display Toppers | Top N students with medals |
| Class Analytics | Average, highest/lowest scorer, subject averages, grade distribution |
| Save CSV | Persist all data automatically to `data/students.csv` |
| Export Result CSV | Ranked result sheet with grades exported to CSV |
| Import CSV | Bulk import students from a CSV file |
| Export PDF Report Card | Individual styled PDF report card per student (reportlab) |
| Export Class PDF Report | Full class result PDF in landscape layout |
| Grade Scale Reference | View grading system table |

## Grade Scale

| Grade | Range | Description |
|---|---|---|
| O | 90–100% | Outstanding |
| A+ | 80–89% | Excellent |
| A | 70–79% | Very Good |
| B | 60–69% | Good |
| C | 50–59% | Average |
| D | 40–49% | Below Average |
| F | 0–39% | Fail |

> Pass condition: Overall ≥ 40% AND each subject ≥ 35 marks

## Project Structure

```
student_result_system/
├── main.py                     # CLI entry point (14 menu options)
├── models/
│   └── student.py              # Student class with grade/percentage/pass logic
├── managers/
│   └── student_manager.py      # CRUD, sorting, analytics
├── reports/
│   ├── csv_report.py           # Save/load/import/export CSV
│   └── pdf_report.py           # Individual & class PDF reports (reportlab)
├── utils/
│   └── helpers.py              # Color printing, validation, table renderer
├── data/
│   └── students.csv            # Auto-saved persistent data
├── reports_output/             # Generated PDFs stored here
├── requirements.txt
└── README.md
```

## Installation & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

## Concepts Covered

- **Classes & Objects** — `Student`, `StudentManager`, `CSVReport`, `PDFReport`
- **CSV Files** — Reading, writing, bulk import, result export
- **Sorting** — By percentage, name, roll number (ascending/descending)
- **Data Processing** — Percentage, grade, pass/fail, statistics
- **File I/O** — Persistent data storage with auto-save on exit
- **PDF Generation** — Professional styled report cards using `reportlab`
- **Input Validation** — Name, roll number, marks all validated
- **OOP Design** — Encapsulation, separation of concerns, modular architecture

## Sample Output

```
Top 5 Students:
  🥇  Priya Singh       Roll: 3     94.33%    Grade: O    PASS
  🥈  Ananya Roy        Roll: 6     88.67%    Grade: A+   PASS
  🥉  Rahul Sharma      Roll: 1     85.50%    Grade: A+   PASS
       Amit Kumar        Roll: 2     81.17%    Grade: A+   PASS
       Vikram Joshi      Roll: 7     71.67%    Grade: A    PASS
```

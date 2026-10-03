import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph,
        Spacer, HRFlowable, KeepTogether
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics import renderPDF
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class PDFReport:
    def __init__(self, output_dir="reports_output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.primary_color = colors.HexColor("#1a237e")
        self.accent_color = colors.HexColor("#0d47a1")
        self.gold_color = colors.HexColor("#f9a825")
        self.green_color = colors.HexColor("#1b5e20")
        self.red_color = colors.HexColor("#b71c1c")
        self.light_blue = colors.HexColor("#e3f2fd")
        self.light_grey = colors.HexColor("#f5f5f5")

    def is_available(self):
        return REPORTLAB_AVAILABLE

    def _get_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name="SchoolTitle",
            fontSize=20,
            fontName="Helvetica-Bold",
            textColor=self.primary_color,
            alignment=TA_CENTER,
            spaceAfter=4,
        ))
        styles.add(ParagraphStyle(
            name="SubTitle",
            fontSize=11,
            fontName="Helvetica",
            textColor=self.accent_color,
            alignment=TA_CENTER,
            spaceAfter=2,
        ))
        styles.add(ParagraphStyle(
            name="SectionHeading",
            fontSize=13,
            fontName="Helvetica-Bold",
            textColor=self.primary_color,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=4,
        ))
        styles.add(ParagraphStyle(
            name="InfoLabel",
            fontSize=10,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#424242"),
        ))
        styles.add(ParagraphStyle(
            name="InfoValue",
            fontSize=10,
            fontName="Helvetica",
            textColor=colors.black,
        ))
        styles.add(ParagraphStyle(
            name="FooterText",
            fontSize=8,
            fontName="Helvetica",
            textColor=colors.grey,
            alignment=TA_CENTER,
        ))
        styles.add(ParagraphStyle(
            name="ResultPass",
            fontSize=18,
            fontName="Helvetica-Bold",
            textColor=self.green_color,
            alignment=TA_CENTER,
        ))
        styles.add(ParagraphStyle(
            name="ResultFail",
            fontSize=18,
            fontName="Helvetica-Bold",
            textColor=self.red_color,
            alignment=TA_CENTER,
        ))
        return styles

    def _grade_color(self, grade):
        grade_colors = {
            "O": colors.HexColor("#1b5e20"),
            "A+": colors.HexColor("#2e7d32"),
            "A": colors.HexColor("#388e3c"),
            "B": colors.HexColor("#0277bd"),
            "C": colors.HexColor("#f57f17"),
            "D": colors.HexColor("#e65100"),
            "F": colors.HexColor("#b71c1c"),
        }
        return grade_colors.get(grade, colors.black)

    def export_student_report_card(self, student):
        filename = f"ReportCard_{student.name.replace(' ', '_')}_{student.roll_number}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )
        styles = self._get_styles()
        story = []

        header_data = [[
            Paragraph("EXCEL ACADEMY", styles["SchoolTitle"]),
        ]]
        header_table = Table(header_data, colWidths=[17.5 * cm])
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.primary_color),
            ("ROUNDEDCORNERS", [8]),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 6))

        story.append(Paragraph("STUDENT REPORT CARD", styles["SubTitle"]))
        story.append(Paragraph(f"Academic Year: {student.academic_year}", styles["SubTitle"]))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=2, color=self.gold_color))
        story.append(Spacer(1, 8))

        info_data = [
            [Paragraph("Student Name:", styles["InfoLabel"]), Paragraph(student.name, styles["InfoValue"]),
             Paragraph("Roll No:", styles["InfoLabel"]), Paragraph(str(student.roll_number), styles["InfoValue"])],
            [Paragraph("Student ID:", styles["InfoLabel"]), Paragraph(student.student_id, styles["InfoValue"]),
             Paragraph("Division:", styles["InfoLabel"]), Paragraph(student.division, styles["InfoValue"])],
            [Paragraph("Date of Birth:", styles["InfoLabel"]), Paragraph(student.dob or "N/A", styles["InfoValue"]),
             Paragraph("Generated:", styles["InfoLabel"]), Paragraph(datetime.now().strftime("%d-%m-%Y"), styles["InfoValue"])],
        ]
        info_table = Table(info_data, colWidths=[3.5 * cm, 5.5 * cm, 3.5 * cm, 5 * cm])
        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.light_blue),
            ("BOX", (0, 0), (-1, -1), 1, self.accent_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bbdefb")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 12))

        story.append(Paragraph("MARKS STATEMENT", styles["SectionHeading"]))
        story.append(HRFlowable(width="100%", thickness=1, color=self.accent_color))
        story.append(Spacer(1, 6))

        marks_header = [
            Paragraph("Subject", ParagraphStyle("th", fontSize=10, fontName="Helvetica-Bold",
                                                  textColor=colors.white, alignment=TA_CENTER)),
            Paragraph("Max Marks", ParagraphStyle("th", fontSize=10, fontName="Helvetica-Bold",
                                                   textColor=colors.white, alignment=TA_CENTER)),
            Paragraph("Marks Obtained", ParagraphStyle("th", fontSize=10, fontName="Helvetica-Bold",
                                                        textColor=colors.white, alignment=TA_CENTER)),
            Paragraph("Grade", ParagraphStyle("th", fontSize=10, fontName="Helvetica-Bold",
                                               textColor=colors.white, alignment=TA_CENTER)),
            Paragraph("Status", ParagraphStyle("th", fontSize=10, fontName="Helvetica-Bold",
                                                textColor=colors.white, alignment=TA_CENTER)),
        ]
        marks_rows = [marks_header]
        for i, subj in enumerate(student.subjects):
            mark = student.marks.get(subj, None)
            if mark is None:
                continue
            sub_grade = ""
            sub_status_color = self.green_color
            if mark >= 90:
                sub_grade = "O"
            elif mark >= 80:
                sub_grade = "A+"
            elif mark >= 70:
                sub_grade = "A"
            elif mark >= 60:
                sub_grade = "B"
            elif mark >= 50:
                sub_grade = "C"
            elif mark >= 40:
                sub_grade = "D"
            else:
                sub_grade = "F"
                sub_status_color = self.red_color
            status = "Pass" if mark >= 35 else "Fail"
            row_bg = self.light_grey if i % 2 == 0 else colors.white
            marks_rows.append([
                Paragraph(subj, ParagraphStyle("cell", fontSize=10, fontName="Helvetica")),
                Paragraph("100", ParagraphStyle("cell", fontSize=10, fontName="Helvetica", alignment=TA_CENTER)),
                Paragraph(f"{mark:.2f}", ParagraphStyle("cell", fontSize=10, fontName="Helvetica-Bold", alignment=TA_CENTER)),
                Paragraph(sub_grade, ParagraphStyle("cell", fontSize=10, fontName="Helvetica-Bold",
                                                     textColor=self._grade_color(sub_grade), alignment=TA_CENTER)),
                Paragraph(status, ParagraphStyle("cell", fontSize=10, fontName="Helvetica-Bold",
                                                  textColor=sub_status_color, alignment=TA_CENTER)),
            ])

        marks_rows.append([
            Paragraph("TOTAL", ParagraphStyle("total", fontSize=11, fontName="Helvetica-Bold",
                                               textColor=self.primary_color)),
            Paragraph(str(int(student.get_max_total())), ParagraphStyle("total", fontSize=11,
                                                                         fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(f"{student.get_total():.2f}", ParagraphStyle("total", fontSize=11,
                                                                     fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph("", ParagraphStyle("total", fontSize=11, fontName="Helvetica-Bold")),
            Paragraph("", ParagraphStyle("total", fontSize=11, fontName="Helvetica-Bold")),
        ])

        marks_table = Table(marks_rows, colWidths=[5.5 * cm, 3 * cm, 4 * cm, 2.5 * cm, 2.5 * cm])
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), self.primary_color),
            ("BACKGROUND", (0, -1), (-1, -1), self.light_blue),
            ("BOX", (0, 0), (-1, -1), 1.5, self.accent_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("LINEABOVE", (0, -1), (-1, -1), 1.5, self.primary_color),
        ]
        for i in range(1, len(marks_rows) - 1):
            if i % 2 == 0:
                style_cmds.append(("BACKGROUND", (0, i), (-1, i), self.light_grey))
        marks_table.setStyle(TableStyle(style_cmds))
        story.append(marks_table)
        story.append(Spacer(1, 14))

        summary_data = [
            ["Percentage", f"{student.get_percentage():.2f}%"],
            ["Overall Grade", student.get_grade()],
            ["Performance", student.get_grade_description()],
            ["Result", "PASS" if student.is_pass() else "FAIL"],
            ["Rank (Class)", "N/A"],
        ]
        result_color = self.green_color if student.is_pass() else self.red_color
        sum_style = [
            ("BACKGROUND", (0, 0), (0, -1), self.primary_color),
            ("BACKGROUND", (1, 0), (1, -1), self.light_blue),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("TEXTCOLOR", (1, 3), (1, 3), result_color),
            ("BOX", (0, 0), (-1, -1), 1.5, self.accent_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bbdefb")),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ]
        summary_table = Table(summary_data, colWidths=[6 * cm, 6 * cm])
        summary_table.setStyle(TableStyle(sum_style))

        sig_data = [
            [
                Paragraph("_____________________", styles["InfoLabel"]),
                Paragraph("_____________________", styles["InfoLabel"]),
                Paragraph("_____________________", styles["InfoLabel"]),
            ],
            [
                Paragraph("Class Teacher", styles["FooterText"]),
                Paragraph("Principal", styles["FooterText"]),
                Paragraph("Parent/Guardian", styles["FooterText"]),
            ]
        ]
        sig_table = Table(sig_data, colWidths=[5.5 * cm, 5.5 * cm, 5.5 * cm])
        sig_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ]))

        combined = Table([[summary_table, Spacer(1, 1), sig_table]], colWidths=[12.5 * cm, 0.5 * cm, 6 * cm])
        combined.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        story.append(combined)
        story.append(Spacer(1, 16))

        story.append(HRFlowable(width="100%", thickness=1, color=self.gold_color))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            f"Generated by Student Result Management System  |  {datetime.now().strftime('%d-%m-%Y %H:%M')}  |  Excel Academy",
            styles["FooterText"]
        ))

        doc.build(story)
        return filepath

    def export_class_report(self, students, class_name="Class X"):
        filename = f"ClassReport_{class_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(
            filepath,
            pagesize=landscape(A4),
            rightMargin=1.2 * cm,
            leftMargin=1.2 * cm,
            topMargin=1.2 * cm,
            bottomMargin=1.2 * cm,
        )
        styles = self._get_styles()
        story = []

        story.append(Paragraph("EXCEL ACADEMY", styles["SchoolTitle"]))
        story.append(Paragraph(f"Class Result Report — {class_name}", styles["SubTitle"]))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y')}", styles["SubTitle"]))
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=2, color=self.gold_color))
        story.append(Spacer(1, 8))

        sorted_students = sorted(students, key=lambda s: s.get_percentage(), reverse=True)
        from models.student import DEFAULT_SUBJECTS
        subjects = DEFAULT_SUBJECTS

        header = ["Rank", "Roll No", "Name", "Division"] + subjects + ["Total", "Percentage", "Grade", "Result"]
        col_w = [1.2 * cm, 1.5 * cm, 3.5 * cm, 1.5 * cm] + [2.8 * cm] * len(subjects) + [1.8 * cm, 2.2 * cm, 1.5 * cm, 1.5 * cm]
        header_row = [Paragraph(h, ParagraphStyle("th", fontSize=8, fontName="Helvetica-Bold",
                                                    textColor=colors.white, alignment=TA_CENTER)) for h in header]
        rows = [header_row]

        for rank, s in enumerate(sorted_students, 1):
            result_c = self.green_color if s.is_pass() else self.red_color
            row = [
                Paragraph(str(rank), ParagraphStyle("td", fontSize=8, fontName="Helvetica-Bold", alignment=TA_CENTER)),
                Paragraph(str(s.roll_number), ParagraphStyle("td", fontSize=8, fontName="Helvetica", alignment=TA_CENTER)),
                Paragraph(s.name, ParagraphStyle("td", fontSize=8, fontName="Helvetica")),
                Paragraph(s.division, ParagraphStyle("td", fontSize=8, fontName="Helvetica", alignment=TA_CENTER)),
            ]
            for subj in subjects:
                m = s.marks.get(subj, "")
                row.append(Paragraph(f"{m:.0f}" if isinstance(m, float) else str(m),
                                     ParagraphStyle("td", fontSize=8, fontName="Helvetica", alignment=TA_CENTER)))
            row += [
                Paragraph(f"{s.get_total():.0f}", ParagraphStyle("td", fontSize=9, fontName="Helvetica-Bold", alignment=TA_CENTER)),
                Paragraph(f"{s.get_percentage():.2f}%", ParagraphStyle("td", fontSize=9, fontName="Helvetica-Bold", alignment=TA_CENTER)),
                Paragraph(s.get_grade(), ParagraphStyle("td", fontSize=9, fontName="Helvetica-Bold",
                                                         textColor=self._grade_color(s.get_grade()), alignment=TA_CENTER)),
                Paragraph("P" if s.is_pass() else "F", ParagraphStyle("td", fontSize=9, fontName="Helvetica-Bold",
                                                                        textColor=result_c, alignment=TA_CENTER)),
            ]
            rows.append(row)

        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), self.primary_color),
            ("BOX", (0, 0), (-1, -1), 1, self.accent_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e0e0e0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ]
        for i in range(1, len(rows)):
            if i % 2 == 0:
                style_cmds.append(("BACKGROUND", (0, i), (-1, i), self.light_grey))

        class_table = Table(rows, colWidths=col_w, repeatRows=1)
        class_table.setStyle(TableStyle(style_cmds))
        story.append(class_table)
        story.append(Spacer(1, 12))

        story.append(HRFlowable(width="100%", thickness=1, color=self.gold_color))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            f"Total Students: {len(students)}  |  Generated by Student Result Management System  |  {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["FooterText"]
        ))

        doc.build(story)
        return filepath

import os
import sys


COLORS = {
    "reset":   "\033[0m",
    "bold":    "\033[1m",
    "red":     "\033[91m",
    "green":   "\033[92m",
    "yellow":  "\033[93m",
    "blue":    "\033[94m",
    "magenta": "\033[95m",
    "cyan":    "\033[96m",
    "white":   "\033[97m",
    "orange":  "\033[38;5;214m",
    "purple":  "\033[38;5;135m",
    "bg_blue": "\033[44m",
    "bg_green":"\033[42m",
    "bg_red":  "\033[41m",
}


def color(text, *attrs):
    if sys.platform == "win32":
        os.system("color")
    parts = "".join(COLORS.get(a, "") for a in attrs)
    return f"{parts}{text}{COLORS['reset']}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(color("\n  Press Enter to continue...", "yellow"))


def center_text(text, width=70):
    return text.center(width)


def format_percentage(pct):
    return f"{pct:.2f}%"


def validate_name(name):
    name = name.strip()
    if not name:
        raise ValueError("Name cannot be empty.")
    if not all(c.isalpha() or c.isspace() for c in name):
        raise ValueError("Name must contain only letters and spaces.")
    if len(name) < 2 or len(name) > 60:
        raise ValueError("Name must be between 2 and 60 characters.")
    return name.title()


def validate_roll(roll_str, existing_rolls=None):
    roll_str = roll_str.strip()
    if not roll_str.isdigit():
        raise ValueError("Roll number must be a positive integer.")
    roll = int(roll_str)
    if roll <= 0:
        raise ValueError("Roll number must be greater than 0.")
    if existing_rolls and roll in existing_rolls:
        raise ValueError(f"Roll number {roll} already exists.")
    return roll


def validate_marks(marks_str, max_marks=100):
    try:
        marks = float(marks_str.strip())
    except ValueError:
        raise ValueError(f"Marks must be a number (0 to {max_marks}).")
    if marks < 0 or marks > max_marks:
        raise ValueError(f"Marks must be between 0 and {max_marks}.")
    return round(marks, 2)


def get_str_input(prompt, allow_empty=False):
    while True:
        val = input(color(f"  {prompt}", "cyan")).strip()
        if val or allow_empty:
            return val
        print(color("  Input cannot be empty. Try again.", "red"))


def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        raw = input(color(f"  {prompt}", "cyan")).strip()
        if not raw.lstrip("-").isdigit():
            print(color("  Please enter a valid integer.", "red"))
            continue
        val = int(raw)
        if min_val is not None and val < min_val:
            print(color(f"  Value must be >= {min_val}.", "red"))
            continue
        if max_val is not None and val > max_val:
            print(color(f"  Value must be <= {max_val}.", "red"))
            continue
        return val


def get_float_input(prompt, min_val=0.0, max_val=100.0):
    while True:
        raw = input(color(f"  {prompt}", "cyan")).strip()
        try:
            val = float(raw)
        except ValueError:
            print(color("  Please enter a valid number.", "red"))
            continue
        if val < min_val or val > max_val:
            print(color(f"  Value must be between {min_val} and {max_val}.", "red"))
            continue
        return round(val, 2)


def print_table(headers, rows, col_widths=None, title=None):
    if not col_widths:
        col_widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) + 2
                      for i, h in enumerate(headers)]
    total_width = sum(col_widths) + len(col_widths) + 1
    border = color("+" + "+".join("-" * w for w in col_widths) + "+", "blue")
    header_row = color("|", "blue") + color("|", "blue").join(
        color(str(h).center(col_widths[i]), "bold", "yellow") for i, h in enumerate(headers)
    ) + color("|", "blue")
    separator = color("+" + "+".join("=" * w for w in col_widths) + "+", "blue")

    print()
    if title:
        print(color(center_text(f"  {title}  ", total_width), "bold", "magenta"))
    print(border)
    print(header_row)
    print(separator)
    for row in rows:
        line = color("|", "blue")
        for i, cell in enumerate(row):
            cell_str = str(cell)
            try:
                float(cell_str.replace("%", ""))
                aligned = cell_str.rjust(col_widths[i] - 1) + " "
            except ValueError:
                aligned = cell_str.ljust(col_widths[i] - 1) + " "
            line += color(" " + aligned.lstrip(" ").rjust(col_widths[i] - 1) + " ", "white") if False else (" " + cell_str.center(col_widths[i] - 2) + " |")
        print(line)
    print(border)
    print()

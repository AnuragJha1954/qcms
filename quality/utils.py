# quality/utils.py

def calculate_grade(score):
    if score >= 80:
        return "A"
    elif score >= 50:
        return "B"
    return "C"
# gpa_utils.py

def score_to_gpa(score: float) -> float:
    if score >= 90:
        return 4.0
    elif score >= 85:
        return 3.7
    elif score >= 80:
        return 3.3
    elif score >= 75:
        return 3.0
    elif score >= 70:
        return 2.7
    elif score >= 65:
        return 2.3
    elif score >= 60:
        return 2.0
    else:
        return 0.0

def calculate_gpa(grades_with_credit: list[tuple]) -> float:
    total_points = 0.0
    total_credits = 0.0

    for grade, course in grades_with_credit:
        score = grade.score
        credit = course.credit
        gpa = score_to_gpa(score)
        total_points += gpa * credit
        total_credits += credit

    if total_credits == 0:
        return 0.0

    return round(total_points / total_credits, 2)

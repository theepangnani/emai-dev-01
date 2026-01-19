def calculate_risk(attendance_pct: float | None, average_grade: float | None, missed_submissions_30d: int | None) -> float:
    risk = 0.15

    if attendance_pct is not None and attendance_pct < 80:
        risk += 0.35
    if average_grade is not None and average_grade < 65:
        risk += 0.35
    if missed_submissions_30d is not None and missed_submissions_30d >= 3:
        risk += 0.25

    return max(0.0, min(1.0, risk))

def recommend_actions(risk: float) -> list[str]:
    if risk >= 0.75:
        return ["Schedule check-in", "Assign remediation pack", "Notify parent/guardian"]
    if risk >= 0.45:
        return ["Assign practice set", "Teacher quick feedback note"]
    return ["Continue current path"]

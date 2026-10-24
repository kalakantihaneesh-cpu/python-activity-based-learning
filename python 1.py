from dataclasses import dataclass

@dataclass
class Applicant:
    applicant_id: str
    name: str
    aggregate_marks: float
    subject_marks: dict[str, float]
    attendance_percent: float
    annual_income: float


# Example scholarship criteria
MIN_AGGREGATE = 75
MIN_SUBJECT_MARK = 60
MIN_ATTENDANCE = 80
MAX_ANNUAL_INCOME = 300_000


def is_eligible(applicant: Applicant) -> bool:
    """Return whether the applicant meets every scholarship requirement."""
    return (
        applicant.aggregate_marks >= MIN_AGGREGATE
        and all(mark >= MIN_SUBJECT_MARK for mark in applicant.subject_marks.values())
        and applicant.attendance_percent >= MIN_ATTENDANCE
        and applicant.annual_income <= MAX_ANNUAL_INCOME
    )


def rank_applicants(applicants: list[Applicant]) -> tuple[list[Applicant], list[Applicant]]:
    """Return eligible applicants in rank order and the ineligible applicants."""
    eligible = [a for a in applicants if is_eligible(a)]
    ineligible = [a for a in applicants if not is_eligible(a)]

    # Higher aggregate, higher attendance, lower income, then ID alphabetically.
    eligible.sort(
        key=lambda a: (
            -a.aggregate_marks,
            -a.attendance_percent,
            a.annual_income,
            a.applicant_id.lower(),
        )
    )

    return eligible, ineligible


if __name__ == "__main__":
    applicants = [
        Applicant("S003", "Asha", 88, {"Math": 91, "Science": 82}, 95, 250_000),
        Applicant("S001", "Ravi", 88, {"Math": 85, "Science": 80}, 90, 200_000),
        Applicant("S002", "Mina", 72, {"Math": 80, "Science": 75}, 92, 150_000),
        Applicant("S004", "Dev", 81, {"Math": 55, "Science": 89}, 96, 180_000),
    ]

    eligible, ineligible = rank_applicants(applicants)

    print("Eligible applicants:")
    for rank, applicant in enumerate(eligible, start=1):
        print(
            f"{rank}. {applicant.name} (ID: {applicant.applicant_id}) — "
            f"marks: {applicant.aggregate_marks}, "
            f"attendance: {applicant.attendance_percent}%, "
            f"income: {applicant.annual_income}"
        )

    print("\nIneligible applicants:")
    for applicant in ineligible:
        print(f"- {applicant.name} (ID: {applicant.applicant_id})")

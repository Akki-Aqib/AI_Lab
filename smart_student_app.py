"""
Smart Student Application — GPA Tracker & Career Path Recommender
Domain: Education / Student Management
Features:
  - GPA calculation and trend analysis
  - Subject performance analysis  
  - Career path recommendation based on strengths
  - Study time optimizer
"""

class StudentApp:
    CAREER_MAP = {
        'Data Science':      ['Mathematics', 'Statistics', 'Python', 'Machine Learning'],
        'Software Engineer': ['Programming', 'Data Structures', 'Algorithms', 'DBMS'],
        'AI/ML Engineer':    ['Machine Learning', 'Mathematics', 'Python', 'Deep Learning'],
        'Web Developer':     ['Programming', 'DBMS', 'Networking', 'Operating Systems'],
        'Cybersecurity':     ['Networking', 'Operating Systems', 'Algorithms', 'DBMS'],
        'Research':          ['Mathematics', 'Statistics', 'Machine Learning', 'Algorithms'],
    }

    GRADE_POINTS = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0}

    def __init__(self, name, branch):
        self.name = name
        self.branch = branch
        self.semesters = {}

    def add_semester(self, sem_num, subjects):
        """subjects: dict of {subject_name: (grade, credits)}"""
        self.semesters[sem_num] = subjects

    def calculate_gpa(self, sem_num):
        subjects = self.semesters.get(sem_num, {})
        if not subjects:
            return 0.0
        total_points = sum(self.GRADE_POINTS.get(g, 0) * c for g, c in subjects.values())
        total_credits = sum(c for _, c in subjects.values())
        return round(total_points / total_credits, 2) if total_credits else 0.0

    def calculate_cgpa(self):
        if not self.semesters:
            return 0.0
        all_gpa = [self.calculate_gpa(s) for s in self.semesters]
        return round(sum(all_gpa) / len(all_gpa), 2)

    def get_strong_subjects(self):
        strong = []
        for subjects in self.semesters.values():
            for name, (grade, _) in subjects.items():
                if self.GRADE_POINTS.get(grade, 0) >= 8:
                    strong.append(name)
        return list(set(strong))

    def recommend_career(self):
        strong = set(self.get_strong_subjects())
        scores = {}
        for career, required in self.CAREER_MAP.items():
            match = len(strong.intersection(set(required)))
            scores[career] = match
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return top[:3]

    def gpa_trend(self):
        trend = []
        for sem in sorted(self.semesters):
            trend.append((sem, self.calculate_gpa(sem)))
        return trend

    def study_optimizer(self):
        weak = []
        for subjects in self.semesters.values():
            for name, (grade, credits) in subjects.items():
                if self.GRADE_POINTS.get(grade, 0) < 7:
                    weak.append((name, self.GRADE_POINTS.get(grade, 0), credits))
        weak.sort(key=lambda x: x[1])
        return weak

    def full_report(self):
        print("=" * 60)
        print(f"  STUDENT REPORT — {self.name}")
        print(f"  Branch: {self.branch}")
        print("=" * 60)

        for sem in sorted(self.semesters):
            print(f"\n  Semester {sem}:")
            print(f"  {'Subject':<25} {'Grade':>6} {'Credits':>8} {'Points':>8}")
            print("  " + "-" * 50)
            for subj, (grade, credits) in self.semesters[sem].items():
                pts = self.GRADE_POINTS.get(grade, 0) * credits
                print(f"  {subj:<25} {grade:>6} {credits:>8} {pts:>8}")
            print(f"  {'GPA':>36}: {self.calculate_gpa(sem)}")

        print(f"\n  CGPA: {self.calculate_cgpa()}")

        print("\n  📈 GPA Trend:")
        for sem, gpa in self.gpa_trend():
            bar = "█" * int(gpa)
            print(f"   Sem {sem}: {gpa:.2f} {bar}")

        print("\n  💼 Career Recommendations:")
        for i, (career, score) in enumerate(self.recommend_career(), 1):
            strength = "★" * score + "☆" * (4 - score)
            print(f"   {i}. {career:<25} {strength}")

        weak = self.study_optimizer()
        if weak:
            print("\n  ⚠️  Focus Areas (weak subjects):")
            for name, pts, credits in weak:
                print(f"   - {name} (Grade Points: {pts}, Credits: {credits})")
        else:
            print("\n  ✅ Excellent! No weak subjects found.")

        print("=" * 60)


if __name__ == "__main__":
    student = StudentApp("Rahul Sharma", "Computer Science & Engineering")
    student.add_semester(1, {
        'Mathematics':       ('A',  4),
        'Programming':       ('O',  4),
        'Physics':           ('B+', 3),
        'English':           ('A+', 2),
        'Engineering Drawing':('B', 2),
    })
    student.add_semester(2, {
        'Data Structures':   ('O',  4),
        'Statistics':        ('A',  3),
        'DBMS':              ('A+', 4),
        'Networking':        ('B+', 3),
        'Operating Systems': ('A',  4),
    })
    student.add_semester(3, {
        'Algorithms':        ('A+', 4),
        'Machine Learning':  ('O',  4),
        'Python':            ('O',  3),
        'Deep Learning':     ('A',  3),
        'Software Engineering':('B',3),
    })
    student.full_report()

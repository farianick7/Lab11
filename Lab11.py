import os
import matplotlib.pyplot as plt

DATA_DIR = "data"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
ASSIGNMENTS_FILE = os.path.join(DATA_DIR, "assignments.txt")
SUBMISSIONS_DIR = os.path.join(DATA_DIR, "submissions")

def load_students():
    students = {}
    with open(STUDENTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            student_id = line[:3]
            student_name = line[3:]
            students[student_id] = student_name
    return students

def load_assignments():
    assignments = {}
    with open(ASSIGNMENTS_FILE, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
        for i in range(0, len(lines), 3):
            assignment_name = lines[i]
            assignment_id = lines[i+1]
            point_value = float(lines[i+2])
            assignments[assignment_id] = (assignment_name, point_value)
    return assignments

def load_submissions():
    submissions = []
    for filename in os.listdir(SUBMISSIONS_DIR):
        if filename.startswith("._"):
            continue
        full_path = os.path.join(SUBMISSIONS_DIR, filename)
        if not os.path.isfile(full_path):
            continue
        with open(full_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                student_id = parts[0]
                assignment_id = parts[1]
                percent = float(parts[2])
                submissions.append((student_id, assignment_id, percent))
    return submissions

def find_student_id_by_name(students, target_name):
    for sid, name in students.items():
        if name == target_name:
            return sid
    return None

def calculate_student_grade(student_name, students, assignments, submissions):
    student_id = find_student_id_by_name(students, student_name)
    if student_id is None:
        print("Student not found")
        return
    total_earned = 0.0
    total_possible = 0.0
    for (_, points) in assignments.values():
        total_possible += points
    for sid, aid, percent in submissions:
        if sid == student_id:
            if aid not in assignments:
                continue
            _, points = assignments[aid]
            earned = (percent / 100.0) * points
            total_earned += earned
    grade_percent = round((total_earned / total_possible) * 100)
    print(f"{grade_percent}%")

def assignment_stats(assignment_name, assignments, submissions):
    assignment_id = None    # must be None so we can detect missing assignment
    for aid, (name, value) in assignments.items():
        if name == assignment_name:
            assignment_id = aid
            break
    if assignment_id is None:
        print("Assignment not found")
        return None
    scores = [percent for (sid, aid, percent) in submissions if aid == assignment_id]
    if not scores:
        print("Assignment not found")
        return None
    min_score = round(min(scores))
    avg_score = round(sum(scores) / len(scores))
    max_score = round(max(scores))
    print(f"Min: {min_score}%")
    print(f"Avg: {avg_score}%")
    print(f"Max: {max_score}%")
    return scores

def assignment_graph(assignment_name, assignments, submissions):
    scores = assignment_stats(assignment_name, assignments, submissions)
    if scores is None:
        return
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(assignment_name)
    plt.xlabel("Score (%)")
    plt.ylabel("Number of students")
    plt.show()

def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    selection = input("Enter your selection: ")
    if selection == "1":
        student_name = input("What is the student's name: ")
        calculate_student_grade(student_name, students, assignments, submissions)
    elif selection == "2":
        assignment_name = input("What is the assignment name: ")
        assignment_stats(assignment_name, assignments, submissions)
    elif selection == "3":
        assignment_name = input("What is the assignment name: ")
        assignment_graph(assignment_name, assignments, submissions)

if __name__ == "__main__":
    main()

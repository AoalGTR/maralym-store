class Student:
    def __init__(self, student_id, name, grade):
        self.id = student_id
        self.name = name
        self.grade = grade


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student_id, name, grade):
        student = Student(student_id, name, grade)
        self.students.append(student)

    def view_students(self):
        if not self.students:
            print("No students found.")
            return

        print("--- Student List ---")
        for student in self.students:
            print(f"ID: {student.id} | Name: {student.name} | Grade: {student.grade}")

    def update_grade(self, student_id, new_grade):
        for student in self.students:
            if student.id == student_id:
                student.grade = new_grade
                print("Grade updated.")
                return

        print("Student not found.")


def main():
    manager = StudentManager()

    while True:
        print("=== Student Management System ===")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Grade")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            student_id = input("Enter ID: ").strip()
            name = input("Enter name: ").strip()
            grade = input("Enter grade: ").strip()
            manager.add_student(student_id, name, grade)
            print("Student added.")

        elif choice == "2":
            manager.view_students()

        elif choice == "3":
            student_id = input("Enter ID: ").strip()
            new_grade = input("Enter new grade: ").strip()
            manager.update_grade(student_id, new_grade)

        elif choice == "4":
            print("Goodbye")
            break

        else:
            print("Invalid option. Please choose 1-4.")

        print()


if __name__ == "__main__":
    main()
 
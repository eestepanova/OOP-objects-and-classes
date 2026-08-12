def get_average_grade(grades_dict):
    """Вспомогательная функция для подсчета средней оценки из словаря."""
    if not grades_dict:
        return 0.0
    all_grades = []
    for grades_list in grades_dict.values():
        all_grades.extend(grades_list)
    if not all_grades:
        return 0.0
    return round(sum(all_grades) / len(all_grades), 1)


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and
                course in self.courses_in_progress and
                course in lecturer.courses_attached and
                1 <= grade <= 10):

            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = get_average_grade(self.grades)
        courses_in_progress_str = ", ".join(self.courses_in_progress)
        finished_courses_str = ", ".join(self.finished_courses)
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade}\n"
                f"Курсы в процессе изучения: {courses_in_progress_str}\n"
                f"Завершенные курсы: {finished_courses_str}")

    # Операторы сравнения для студентов
    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return get_average_grade(self.grades) < get_average_grade(other.grades)

    def __le__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return get_average_grade(self.grades) <= get_average_grade(other.grades)

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return get_average_grade(self.grades) == get_average_grade(other.grades)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = get_average_grade(self.grades)
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg_grade}")

    # Операторы сравнения для лекторов
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return get_average_grade(self.grades) < get_average_grade(other.grades)

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return get_average_grade(self.grades) <= get_average_grade(other.grades)

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return get_average_grade(self.grades) == get_average_grade(other.grades)


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# --- Пример проверки работоспособности ---

# 1. Создаем проверяющего
reviewer = Reviewer('Пётр', 'Петров')
print("--- Проверка Reviewer ---")
print(reviewer)
print()

# 2. Создаем лекторов и студентов для демонстрации сравнения и вывода
lecturer_1 = Lecturer('Иван', 'Иванов')
lecturer_1.courses_attached += ['Python']

lecturer_2 = Lecturer('Сергей', 'Сидоров')
lecturer_2.courses_attached += ['Python']

student_1 = Student('Ольга', 'Алёхина', 'Ж')
student_1.courses_in_progress += ['Python']
student_1.finished_courses += ['Введение в программирование']

student_2 = Student('Алексей', 'Павлов', 'М')
student_2.courses_in_progress += ['Python']

# Выставляем оценки лекторам
student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_2, 'Python', 8)

# Проверяющий выставляет оценки студентам
reviewer.courses_attached += ['Python']
reviewer.rate_hw(student_1, 'Python', 9)
reviewer.rate_hw(student_2, 'Python', 10)

print("--- Проверка Lecturer ---")
print(lecturer_1)
print()

print("--- Проверка Student ---")
print(student_1)
print()

print("--- Проверка сравнения ---")
print(f"Лектор Иванов лучше Сидорова? {lecturer_1 > lecturer_2}")  # True (10.0 > 8.0)
print(f"Студент Алёхина учится хуже Павлова? {student_1 < student_2}")
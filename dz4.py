def get_average_grade(grades_dict):
    """Вспомогательная функция для подсчета средней оценки человека по всем курсам."""
    if not grades_dict:
        return 0.0
    all_grades = []
    for grades_list in grades_dict.values():
        all_grades.extend(grades_list)
    if not all_grades:
        return 0.0
    return round(sum(all_grades) / len(all_grades), 1)


# --- Функции для подсчета средних оценок по курсу ---

def get_avg_hw_grade_by_course(students_list, course_name):
    """Подсчет средней оценки за ДЗ по всем студентам в рамках конкретного курса."""
    all_grades = []
    for student in students_list:
        if isinstance(student, Student) and course_name in student.grades:
            all_grades.extend(student.grades[course_name])
    if not all_grades:
        return 0.0
    return round(sum(all_grades) / len(all_grades), 1)


def get_avg_lecture_grade_by_course(lecturers_list, course_name):
    """Подсчет средней оценки за лекции всех лекторов в рамках конкретного курса."""
    all_grades = []
    for lecturer in lecturers_list:
        if isinstance(lecturer, Lecturer) and course_name in lecturer.grades:
            all_grades.extend(lecturer.grades[course_name])
    if not all_grades:
        return 0.0
    return round(sum(all_grades) / len(all_grades), 1)


# --- Описание классов ---

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


# --- Проверка работы программы (по 2 экземпляра каждого класса) ---

# 1. Создаем Reviewers (Проверяющих)
reviewer_1 = Reviewer('Пётр', 'Петров')
reviewer_1.courses_attached += ['Python', 'Git']

reviewer_2 = Reviewer('Анна', 'Сидорова')
reviewer_2.courses_attached += ['Python']

# 2. Создаем Lecturers (Лекторов)
lecturer_1 = Lecturer('Иван', 'Иванов')
lecturer_1.courses_attached += ['Python', 'Git']

lecturer_2 = Lecturer('Сергей', 'Кузнецов')
lecturer_2.courses_attached += ['Python']

# 3. Создаем Students (Студентов)
student_1 = Student('Ольга', 'Алёхина', 'Ж')
student_1.courses_in_progress += ['Python', 'Git']
student_1.add_courses('Введение в программирование')  # Вызов метода add_courses

student_2 = Student('Алексей', 'Павлов', 'М')
student_2.courses_in_progress += ['Python']

# 4. Вызываем методы выставления оценок
# Студенты оценивают лекторов (метод rate_lecture)
student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Git', 9)
student_1.rate_lecture(lecturer_2, 'Python', 8)

student_2.rate_lecture(lecturer_1, 'Python', 8)
student_2.rate_lecture(lecturer_2, 'Python', 7)

# Проверяющие оценивают студентов (метод rate_hw)
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_1, 'Git', 10)
reviewer_1.rate_hw(student_2, 'Python', 8)

reviewer_2.rate_hw(student_1, 'Python', 8)
reviewer_2.rate_hw(student_2, 'Python', 10)

# 5. Выводим информацию о каждом объекте (__str__)
print("=== СПИСОК ПРОВЕРЯЮЩИХ ===")
print(reviewer_1, "\n")
print(reviewer_2, "\n")

print("=== СПИСОК ЛЕКТОРОВ ===")
print(lecturer_1, "\n")
print(lecturer_2, "\n")

print("=== СПИСОК СТУДЕНТОВ ===")
print(student_1, "\n")
print(student_2, "\n")

# 6. Проверяем операторы сравнения
print("=== СРАВНЕНИЕ ===")
print(f"Летор Иванов лучше Кузнецова? {lecturer_1 > lecturer_2}")
print(f"Студент Алёхина учится хуже Павлова? {student_1 < student_2}")
print()

# 7. Тестируем новые глобальные функции подсчета
students_list = [student_1, student_2]
lecturers_list = [lecturer_1, lecturer_2]

print("=== ПОДСЧЕТ СРЕДНИХ ПО КУРСАМ ===")
avg_hw_python = get_avg_hw_grade_by_course(students_list, 'Python')
print(f"Средняя оценка студентов за ДЗ по курсу 'Python': {avg_hw_python}")

avg_hw_git = get_avg_hw_grade_by_course(students_list, 'Git')
print(f"Средняя оценка студентов за ДЗ по курсу 'Git': {avg_hw_git}")

avg_lec_python = get_avg_lecture_grade_by_course(lecturers_list, 'Python')
print(f"Средняя оценка лекторов за лекции по курсу 'Python': {avg_lec_python}")
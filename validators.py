from db import Teacher, Student


class ValidationError(Exception):
    pass


def validate_student_data(data):
    name = data.get("name")
    age = data.get("age")

    if not (name and age):
        raise ValidationError("name and age are required")

    if not isinstance(age, int):
        raise ValidationError("age must be integer")
    if not isinstance(name, str):
        raise ValidationError("name must be string")

    if age < 0:
        raise ValidationError("age must be positive")
    if name == "":
        raise ValidationError("name must not be empty")


def validate_teacher_data(data):
    required_fields = ["id", "name", "contact_info", "subject_taught"]

    for field in required_fields:
        if field not in data:
            raise ValidationError(f"{field} is required")


def validate_mark_data(data):
    required_fields = ["student_id", "teacher_id", "value"]
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"{field} is required")

    student_id = data.get("student_id")
    teacher_id = data.get("teacher_id")
    value = data.get("value")

    if not isinstance(student_id, int):
        raise ValidationError("student_id must be integer")
    if not isinstance(teacher_id, int):
        raise ValidationError("teacher_id must be integer")
    if not isinstance(value, int) or value <= 0:
        raise ValidationError("value must be integer and positive")

    student = Student.get_or_none(id=student_id)
    if not student:
        raise ValidationError("student with such id not found")

    teacher = Teacher.get_or_none(id=teacher_id)
    if not teacher:
        raise ValidationError("teacher with such id not found")

    data["student"] = student
    data["teacher"] = teacher
    data["value"] = value

    return data

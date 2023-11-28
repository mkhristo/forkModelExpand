from flask import Flask, jsonify, request
from peewee import fn

from db import Student, Mark, Teacher
from deserializators import deserialize_student_data, deserialize_mark_data, deserialize_teacher_data
from serializatiors import serialize_db_student, serialize_db_mark, serialize_db_student_with_marks, serialize_db_teacher
from validators import ValidationError, validate_student_data, validate_teacher_data, validate_mark_data

app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify({"message": "Hello World"})


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify({"message": str(error)})
    response.status_code = 422

    return response


@app.route('/students', methods=["GET", "POST"])
def students_api():
    if request.method == "GET":
        # Get name from query params
        filter_name = request.args.get("name")

        students = Student.select(Student, fn.AVG(Mark.value).alias("avg_mark")).join(Mark).group_by(Student).order_by(
            fn.AVG(Mark.value).desc())

        if filter_name:
            students = students.where(Student.name.contains(filter_name))

        return jsonify([serialize_db_student(student) for student in students])
    elif request.method == "POST":
        data = deserialize_student_data()

        validate_student_data(data)

        student = Student.create(**data)

        return jsonify(serialize_db_student(student)), 201


@app.route('/students/<int:student_id>', methods=["GET"])
def student_api(student_id):
    if request.method == "GET":
        student = Student.get_or_none(id=student_id)

        if not student:
            return jsonify({"message": "student not found"}), 404

        return jsonify(serialize_db_student_with_marks(student))


@app.route('/marks', methods=["GET", "POST"])
def marks_api():
    if request.method == "POST":
        data = deserialize_mark_data()
        validate_mark_data(data)  # This function should validate the mark, teacher_id, and student_id
        teacher = Teacher.get_or_none(Teacher.id == data["teacher_id"])
        student = Student.get_or_none(Student.id == data["student_id"])
        if teacher is None:
            return jsonify({"message": "teacher ID not found"}), 404
        if student is None:
            return jsonify({"message": "student ID not found"}), 404
        mark = Mark.create(value=data["value"], teacher=teacher, student=student)
        return jsonify(serialize_db_mark(mark)), 201
    if request.method == "GET":
        marks = Mark.select(Mark, Student).join(Student)
        return jsonify([serialize_db_mark(mark) for mark in marks])


@app.route('/teachers', methods=["GET", "POST", "PATCH", "DELETE"])
def teachers_api():
    if request.method == "GET":
        return jsonify([serialize_db_teacher(teacher) for teacher in Teacher.select()])
    elif request.method == "POST":
        data = deserialize_teacher_data()
        validate_teacher_data(data)
        teacher = Teacher.create(**data)
        return jsonify(serialize_db_teacher(teacher)), 201
    elif request.method == "PATCH":
        data = deserialize_teacher_data()
        validate_teacher_data(data)
        teacher_id = data.pop("id")
        teacher = Teacher.get_or_none(Teacher.id == teacher_id)
        if not teacher:
            return jsonify({"message": "teacher not found"}), 404
        teacher.update(**data)
        return jsonify(serialize_db_teacher(teacher)), 201
    elif request.method == "DELETE":
        data = deserialize_teacher_data()
        validate_teacher_data(data)
        teacher = Teacher.get_or_none(Teacher.id == data["id"])
        if teacher is None:
            return jsonify({"message": "teacher not found"}), 404
        teacher.delete_instance()
        return jsonify({"message": "teacher deleted"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
from flask import request

def deserialize_student_data():
    data = request.get_json()

    name = data.get("name")
    age = data.get("age")

    return {
        "name": name,
        "age": age
    }


def deserialize_mark_data():
    data = request.get_json()

    student_id = data.get("student_id")
    teacher_id = data.get("teacher_id")
    value = data.get("value")

    return {
        "student_id": student_id,
        "teacher_id": teacher_id,
        "value": value
   }


def deserialize_mark_data_on_change():
    data = request.get_json()
    mark_id = data.get("mark_id")
    new_value = data.get("new_value")

    return {
        "mark_id": mark_id,
        "new_value": new_value
    }


def deserialize_mark_data_on_delete():
    data = request.get_json()
    mark_id = data.get("mark_id")

    return {
        "mark_id": mark_id
   }


def deserialize_teacher_data():
    data = request.get_json()

    id = data.get("id")
    name = data.get("name")
    contact_info = data.get("contact_info")
    subject_taught = data.get("subject_taught")

    return {
        "id": id,
        "name": name,
        "contact_info": contact_info,
        "subject_taught": subject_taught
    }
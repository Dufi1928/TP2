import csv
import json
from .csv_to_json import csv_to_json_string

def find_student(students,student_email ):
    for student in students:
        if str(student_email) == str(student.get('email')):
            return student
    return None

def add_student(csv_file_path,new_student):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        lecteur_csv = csv.DictReader(csvfile)
        students = list(lecteur_csv)
        last_student_id = int(students[-1]['id']) + 1
        print(last_student_id)
        is_exist_student = find_student(students, new_student["email"])
    if not is_exist_student:
        new_student_with_id  = last_student_id
        new_student_with_id = {"id": new_student_with_id}
        new_student_with_id.update(new_student)
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            ecrivain_csv = csv.DictWriter(csvfile, fieldnames=new_student_with_id.keys())
            ecrivain_csv.writerow(new_student_with_id)
            return new_student_with_id
    else:
        return "User already exists"
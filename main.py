import socket
import sys
import signal
import json

running = True

from src.csv_to_json import csv_to_json_string
from src.incert_student import add_student

students_src = "./src/data/students.csv"
classes_src = "./src/data/class.csv"

classes_json_data  = csv_to_json_string(classes_src)
students_json_data  = csv_to_json_string(students_src)

classes_object_data  = json.loads(classes_json_data)
students_object_data  = json.loads(students_json_data)



def find_by_id(data, id_to_find):
    for data_in in data:
        if str(id_to_find) == str(data_in.get('id')):
            return data_in
    return None

def http_response(content):
    return f'HTTP/1.0 200 OK\nContent-Type: application/json\n\n{content}'

def http_error_response(status_code, message):
    return f'HTTP/1.0 {status_code} {message}\n\n{message}'

def handle_request(request, client_socket):
    headers, _ = request.split('\r\n\r\n', 1)
    header_lines = headers.split('\r\n')
    request_line = header_lines[0]
    method, path, _ = request_line.split()
    global classes_json_data
    global students_json_data
    global students_object_data
    global class_object_data

    if method == 'GET':
        if path.startswith('/class'):
            path_class_parts = path.split('/')
            if len(path_class_parts) == 3 and path_class_parts[1] == 'class':
                class_id = path_class_parts[2]
                class_data = find_by_id(classes_object_data, class_id)
                if not class_data:
                    response = 'HTTP/1.0 404 NOT FOUND\n\n404 Page Not Found'
                else:
                    response = http_response(json.dumps(class_data))
            else:
                response = http_response(classes_json_data)
        elif path.startswith('/students'):
            path_students_parts = path.split('/')
            if len(path_students_parts) == 3 and path_students_parts[1] == 'students':
                student_id = path_students_parts[2]
                student_data = find_by_id(students_object_data, student_id)
                if not student_data:
                    response = 'HTTP/1.0 404 NOT FOUND\n\n404 Page Not Found'
                else:
                    response = http_response(json.dumps(student_data))
            else:
                response = http_response(students_object_data)
        else:
            response = 'HTTP/1.0 404 NOT FOUND\n\n404 Page Not Found'
    elif method == 'POST':
        if path == '/add_student':
            _, body = request.split('\r\n\r\n', 1)
            student_data = json.loads(body)
            aded_student = add_student(students_src,student_data)
            if aded_student :
                response = http_response(json.dumps(aded_student))
            elif aded_student == "User already exists":
                response = http_error_response(409, 'Conflict: User already exists')
            else:
                response = http_error_response(400, 'Message: Bad request')

        else:
            response = 'HTTP/1.0 404 NOT FOUND\n\n404 Page Not Found'
    client_socket.sendall(response.encode('utf-8'))


def run_server(host='localhost', port=8000):
    global running

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()

            print(f'Server running on {host}:{port}...')

            while running:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    request = client_socket.recv(1024).decode('utf-8')
                    handle_request(request, client_socket)

    except OSError as e:
        print(f"{e}.")

def signal_handler(sig, frame):
    global running
    print("\nInterruption détectée, arrêt du serveur.")
    running = False

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    run_server()
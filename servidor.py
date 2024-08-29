import socket
from pathlib import Path
from utils import *
from views import *
CUR_DIR = Path(__file__).parent
route = 'img/logo-getit.png'
filepath = CUR_DIR / route
SERVER_HOST = '0.0.0.0'

SERVER_PORT = 8080

RESPONSE_TEMPLATE = '''HTTP/1.1 200 OK'''

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')
while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    route = extract_route(request)
    filepath = CUR_DIR / route.strip()
    if filepath.is_file():
        response = buildResponse() + read_file(filepath)
    elif "POST" in request:
        response = postResponses(request)
    elif route == '':
        response = index()
    else:
        response = buildResponse(code=404, reason='Not Found')
    client_connection.sendall(response)
    client_connection.close()
server_socket.close()
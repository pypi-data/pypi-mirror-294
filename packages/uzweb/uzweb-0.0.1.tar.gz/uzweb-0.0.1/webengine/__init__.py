import socket
import threading
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from random import randint

class UzWebApp:
    def __init__(self, title='UzWebApp'):
        self.title = title
        self.routes = {}
        self.files = {}
        self.websockets = []

    def page(self, path="/"):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def websocket(self, route):
        def decorator(func):
            self.websockets.append({'route': route, 'handler': func})
            return func
        return decorator

    def serve(self, host="127.0.0.1", port=10000):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Serving '{self.title}' on http://{host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def handle_client(self, client_socket, addr):
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            return
        
        method, path, _ = request.split(' ', 2)
        parsed_url = urlparse(path)
        route = self.routes.get(parsed_url.path)

        if route:
            response = route()
            client_socket.sendall(self.create_response(response))
        else:
            client_socket.sendall(self.create_response("<h1>404 Not Found</h1>", status_code=404))

        client_socket.close()

    def create_response(self, content, status_code=200, headers=None):
        response = f"HTTP/1.1 {status_code} OK\r\nContent-Type: text/html\r\n"
        if headers:
            for key, value in headers.items():
                response += f"{key}: {value}\r\n"
        response += f"\r\n{content}"
        return response.encode('utf-8')

    def return_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "<h1>404 File Not Found</h1>"

    def get_file(self, file_path):
        if file_path not in self.files:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                self.files[file_path] = BeautifulSoup(content, 'html.parser')
            except FileNotFoundError:
                return None
        return self.files.get(file_path, None)

    def update_element(self, file_path, element_id, new_text):
        soup = self.get_file(file_path)
        if soup:
            element = soup.find(id=element_id)
            if element:
                element.string = new_text
                return str(soup)
        return "<h1>404 Not Found</h1>"

    def click(self, file_path, element_class):
        html = self.get_file(file_path)
        if html:
            element = html.find(class_=element_class)
            if element and 'onclick' in element.attrs:
                return element.attrs['onclick']
        return None

# Kutubxonaning soddalashtirilgan ishlatilishi

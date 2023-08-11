from http.server import HTTPServer, BaseHTTPRequestHandler
import json

Settings = {"HOST": "192.168.122.118", "PORT": 8080}

ID = {}


class MainServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(Settings), "utf-8"))

    def do_POST(self):
        global ID
        id = int(self.headers['id'])
        ip = str(self.headers['ip'])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(f"Connected by {id} at {ip}")
        ID[id] = ip
        self.wfile.write(bytes(f"Connected by {id} at {ip}", "utf-8"))


def StartServer(numBots):
    server = HTTPServer((Settings['HOST'], Settings['PORT']), MainServer)
    while len(ID) != numBots:
        server.handle_request()
    return ID

print(StartServer(1))

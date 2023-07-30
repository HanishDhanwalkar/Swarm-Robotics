from http.server import HTTPServer, BaseHTTPRequestHandler
import json

Settings = {"HOST": "192.168.231.164", "PORT": 8080}


class MainServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(Settings),"utf-8"))

    def do_POST(self):
        id = int(self.headers['id'])
        ip = str(self.headers['ip'])
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        print(f"Connected by {id} at {ip}")
        self.wfile.write(bytes(f"Connected by {id} at {ip}","utf-8"))

server=HTTPServer((Settings['HOST'],Settings['PORT']),MainServer)
server.serve_forever()
server.server_close()

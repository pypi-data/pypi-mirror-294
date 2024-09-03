import socket
import json

class TempDBClient:
    def __init__(self, addr, db_name, api_key):
        self.addr = addr
        self.db_name = db_name
        self.api_key = api_key
        self.conn = None

    def connect(self):
        if self.conn is None:
            host, port = self.addr.split(':')
            self.conn = socket.create_connection((host, int(port)), timeout=5)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def send_command(self, command):
        self.connect()
        full_command = f"{self.api_key} {command}\r\n"
        self.conn.sendall(full_command.encode())
        response = self.conn.recv(4096).decode().strip()
        return response

    def set(self, key, value):
        return self.send_command(f"SET {key} {value}")

    def get(self, key):
        return self.send_command(f"GET {key}")

    def set_ex(self, key, seconds, value):
        return self.send_command(f"SETEX {key} {seconds} {value}")

    def delete(self, key):
        return self.send_command(f"DELETE {key}")

    def lpush(self, key, value):
        return self.send_command(f"LPUSH {key} {value}")

    def sadd(self, key, value):
        return self.send_command(f"SADD {key} {value}")

    def set_data(self, key, value):
        json_value = json.dumps(value)
        return self.send_command(f"SETJSON {key} {json_value}")

    def get_json(self, key, field):
        return self.send_command(f"GETJSON {key} /{field}")

    def view_data(self):
        return self.send_command("VIEW_DATA")

    def get_db(self):
        return self.send_command("GET_DB")
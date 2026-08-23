"""
mock_api_server.py

A tiny local stand-in for the external Text Processing API. This is used
ONLY to demonstrate, end-to-end, that the refactored script correctly
attaches the Authorization header and parses a successful response --
the sandbox environment's network egress rules block the real
api.text-processing.com host, so this mock reproduces its response shape
on 127.0.0.1 for demonstration purposes.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        auth = self.headers.get("Authorization", "")
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()

        if not auth.startswith("Bearer "):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error": "missing bearer token"}')
            return

        # crude parse of the urlencoded "text=" field
        text = ""
        for part in body.split("&"):
            if part.startswith("text="):
                from urllib.parse import unquote_plus
                text = unquote_plus(part[len("text="):])

        text_lower = text.lower()
        if any(w in text_lower for w in ["love", "great", "happy", "sunny", "good"]):
            label = "pos"
        elif any(w in text_lower for w in ["hate", "terrible", "bad", "sad"]):
            label = "neg"
        else:
            label = "neutral"

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"label": label, "probability": {"pos": 0.87}}).encode())

    def log_message(self, format, *args):
        pass  # silence default request logging


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8899), Handler)
    server.serve_forever()

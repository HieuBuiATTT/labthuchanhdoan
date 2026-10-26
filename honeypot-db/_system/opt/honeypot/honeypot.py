from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

logging.basicConfig(filename='/var/log/honeypot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class HoneypotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        log_msg = f"UNAUTHORIZED_PIVOT: Incoming connection from {client_ip} to path {self.path}"
        logging.info(log_msg)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"FLAG{ssrf_lateral_movement_detected_999}\n")

def run():
    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, HoneypotHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()

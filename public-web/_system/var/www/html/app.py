from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import ipaddress
import socket
import logging

logging.basicConfig(filename='/var/log/syslog', level=logging.INFO, format='%(asctime)s - %(message)s')

class SSRFHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path != '/fetch':
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found\n")
            return

        query = parse_qs(parsed_path.query)
        target_url = query.get('url', [None])[0]
        if not target_url:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing 'url' parameter\n")
            return

        parsed_url = urlparse(target_url)
        hostname = parsed_url.hostname
        if not hostname:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid URL format\n")
            return

        try:
            ip_addr = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip_addr)
            logging.info(f"SSRF_PROBE: Request targeting {hostname} ({ip_addr})")

            if (ip_obj.is_loopback or ip_addr == "169.254.169.254") and ip_addr != "172.30.0.99":
                logging.warning(f"SECURITY_ALERT: Blocked SSRF attempt targeting IP -> {ip_addr}")
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"403 Forbidden - Access to internal loopback/metadata is blocked!\n")
                return
        except Exception as e:
            logging.error(f"DNS Resolution error for {hostname}: {e}")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"DNS Resolution Failed\n")
            return

        try:
            req = urllib.request.Request(target_url)
            with urllib.request.urlopen(req, timeout=3) as response:
                body = response.read()
                self.send_response(response.getcode())
                self.end_headers()
                self.wfile.write(body)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write((str(e) + "\n").encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 80), SSRFHandler)
    server.serve_forever()

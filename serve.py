#!/usr/bin/env python3
"""
HTTPS dev server for mahoraga AR demo.
Generates a self-signed cert on first run.

Usage:
  python3 serve.py

Then open: https://localhost:8443
(Chrome: click Advanced → Proceed to localhost)
"""
import http.server, ssl, os, subprocess, sys

CERT = "cert.pem"
KEY  = "key.pem"
PORT = 8443

if not os.path.exists(CERT) or not os.path.exists(KEY):
    print("Generating self-signed certificate…")
    ret = subprocess.run([
        "openssl", "req", "-x509",
        "-newkey", "rsa:2048",
        "-keyout", KEY,
        "-out", CERT,
        "-days", "365",
        "-nodes",
        "-subj", "/CN=localhost"
    ], capture_output=True)
    if ret.returncode != 0:
        print("openssl failed:", ret.stderr.decode())
        sys.exit(1)
    print("Certificate created.")

server = http.server.HTTPServer(("localhost", PORT), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)
server.socket = ctx.wrap_socket(server.socket, server_side=True)

print(f"\n  Serving HTTPS on https://localhost:{PORT}")
print("  First visit: Chrome → Advanced → Proceed to localhost (unsafe)\n")
server.serve_forever()

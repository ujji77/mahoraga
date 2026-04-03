#!/usr/bin/env python3
"""
HTTPS dev server for Mahoraga AR.
Camera access requires a secure context (https:// or localhost via https).

Usage:
    python3 serve.py

Then open: https://localhost:8443
Accept the self-signed cert warning in your browser.
"""

import http.server
import ssl
import os
import subprocess
import sys

PORT = 8443
CERT = 'cert.pem'
KEY  = 'key.pem'

# Generate a self-signed cert if one doesn't exist yet
if not os.path.exists(CERT) or not os.path.exists(KEY):
    print('Generating self-signed TLS certificate…')
    ret = subprocess.run([
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', KEY, '-out', CERT,
        '-days', '365', '-nodes',
        '-subj', '/CN=localhost'
    ], capture_output=True)
    if ret.returncode != 0:
        print('ERROR: openssl failed. Install openssl and retry.')
        print(ret.stderr.decode())
        sys.exit(1)
    print('Certificate created (cert.pem / key.pem)\n')

handler = http.server.SimpleHTTPRequestHandler

# Silence the per-request log noise a little
handler.log_message = lambda self, fmt, *args: print(f'  {args[0]} {args[1]}')

server = http.server.HTTPServer(('localhost', PORT), handler)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)
server.socket = ctx.wrap_socket(server.socket, server_side=True)

print(f'Serving at  https://localhost:{PORT}')
print('Open that URL in Chrome/Firefox, accept the cert warning, then allow camera.\n')
print('Press Ctrl-C to stop.\n')

try:
    server.serve_forever()
except KeyboardInterrupt:
    print('\nStopped.')

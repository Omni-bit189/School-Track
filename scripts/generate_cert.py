#!/usr/bin/env python3
"""
Generates a self-signed SSL certificate for local HTTPS development.
Run once: python scripts/generate_cert.py
"""
import subprocess
import os

CERT_DIR = os.path.join(os.path.dirname(__file__), "..", "certs")
os.makedirs(CERT_DIR, exist_ok=True)

cert_path = os.path.join(CERT_DIR, "cert.pem")
key_path = os.path.join(CERT_DIR, "key.pem")

cmd = [
    "openssl", "req", "-x509", "-newkey", "rsa:4096",
    "-keyout", key_path,
    "-out", cert_path,
    "-days", "365",
    "-nodes",
    "-subj", "/C=IN/ST=Maharashtra/L=Mumbai/O=SchoolTrack/CN=localhost",
    "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1"
]

print("Generating self-signed SSL certificate...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print(f"✅ Certificate generated:")
    print(f"   cert: {cert_path}")
    print(f"   key:  {key_path}")
    print(f"\nTo start with HTTPS, run:")
    print(f"   uvicorn app.main:app --host 0.0.0.0 --port 8443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem --reload")
else:
    print("❌ Error generating certificate:")
    print(result.stderr)
    print("\nMake sure openssl is installed: sudo apt install openssl  (or brew install openssl on Mac)")

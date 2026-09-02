import sys
import os
from a2wsgi import ASGIMiddleware

# Tambahkan path aplikasi ke environment
sys.path.insert(0, os.path.dirname(__file__))

from main import app as fastapi_app

# Handler WSGI untuk Phusion Passenger (cPanel / CloudLinux)
application = ASGIMiddleware(fastapi_app)

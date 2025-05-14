from waitress import serve
from app import app

if __name__ == "__main__":
    # For local network access, use your computer's IP address
    # For example: serve(app, host='192.168.1.100', port=8080)
    
    # For local access only
    print("Starting Store Management System on http://localhost:8080")
    serve(app, host='127.0.0.1', port=8080)
"""
Production server for the Store Management application.
This script runs the application using a production-ready WSGI server (Waitress).
"""
from waitress import serve
import os
import logging
from app import app  # Import your Flask application

# Configure logging
logging.basicConfig(
    filename='store_server.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('store_server')

# Set the port
PORT = 8080

if __name__ == "__main__":
    # Print information to console
    print(f"\n{'='*50}")
    print(f"Store Management System Server")
    print(f"{'='*50}")
    print(f"Server is running at: http://localhost:{PORT}")
    print(f"To access from other computers on your network, use: http://<your-ip-address>:{PORT}")
    print(f"Press Ctrl+C to stop the server")
    print(f"{'='*50}\n")
    
    # Log startup information
    logger.info(f"Starting Store Management Server on port {PORT}")
    
    # Start the server
    serve(app, host='0.0.0.0', port=PORT)
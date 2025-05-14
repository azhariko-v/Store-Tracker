"""
Windows service installer for the Store Management application.
This script creates a Windows service that runs the application in the background.
"""
import sys
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
from threading import Thread
from waitress import serve

# Add the current directory to the path so we can import our app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app  # Import your Flask application

# Configure logging
logging.basicConfig(
    filename='store_service.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('store_service')

class StoreService(win32serviceutil.ServiceFramework):
    _svc_name_ = "StoreManagementService"
    _svc_display_name_ = "Store Management System"
    _svc_description_ = "Runs the Store Management web application in the background"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False
        self.server_thread = None
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True
        logger.info("Service stop requested")
        
    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        logger.info("Service starting")
        self.main()
        
    def main(self):
        # Port to run the server on
        PORT = 8080
        
        # Create and start the server in a separate thread
        self.server_thread = Thread(
            target=serve,
            kwargs={'app': app, 'host': '0.0.0.0', 'port': PORT}
        )
        self.server_thread.daemon = True
        self.server_thread.start()
        
        logger.info(f"Web server started on port {PORT}")
        
        # Keep the service running until stopped
        while not self.stop_requested:
            time.sleep(1)
            
        logger.info("Service stopped")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(StoreService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(StoreService)
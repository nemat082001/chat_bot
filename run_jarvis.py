# run_jarvis.py
"""
Main launcher for JARVIS system
Starts both backend and frontend
"""

import subprocess
import sys
import os
import time
import threading

def run_backend():
    """Run FastAPI backend"""
    print("🚀 Starting JARVIS Backend...")
    os.chdir("src")
    subprocess.run([sys.executable, "jarvis_backend.py"])

def run_frontend():
    """Run React frontend"""
    print("🎨 Starting JARVIS Frontend...")
    time.sleep(5)  # Wait for backend to start
    os.chdir("frontend")
    subprocess.run(["npm", "start"])

def main():
    print("🎯 JARVIS Complete System Launcher")
    print("=" * 50)
    
    choice = input("""
Choose launch mode:
1. Backend only (API server)
2. Frontend only (React app)
3. Full system (Both backend and frontend)
4. Setup (Install dependencies)

Enter choice (1-4): """).strip()
    
    if choice == "1":
        run_backend()
    
    elif choice == "2":
        run_frontend()
    
    elif choice == "3":
        print("🚀 Starting full JARVIS system...")
        # Start backend in separate thread
        backend_thread = threading.Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # Start frontend in main thread
        run_frontend()
    
    elif choice == "4":
        print("📦 Installing dependencies...")
        
        # Install Python dependencies
        print("Installing Python packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Install Node.js dependencies
        print("Installing Node.js packages...")
        os.chdir("frontend")
        subprocess.run(["npm", "install"])
        
        print("✅ Setup complete!")
    
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
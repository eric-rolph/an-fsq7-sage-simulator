"""
Keep Reflex server alive despite Windows shutdown signals.
This is a workaround for the Windows hot-reload issue.
"""
import subprocess
import sys
import time
import signal

# Ignore Control-C
signal.signal(signal.SIGINT, signal.SIG_IGN)

while True:
    print("Starting Reflex server...")
    process = subprocess.Popen(
        [sys.executable, "-m", "reflex", "run"],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    try:
        # Wait for process to complete
        returncode = process.wait()
        print(f"Server exited with code {returncode}, restarting in 2 seconds...")
        time.sleep(2)
    except KeyboardInterrupt:
        print("\nShutting down...")
        process.terminate()
        break

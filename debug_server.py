import subprocess
import sys
import time

# Start reflex in a subprocess
process = subprocess.Popen(
    [sys.executable, "-m", "reflex", "run"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

print("Started reflex process, monitoring output...")
print("=" * 60)

try:
    # Monitor for 30 seconds
    start_time = time.time()
    while time.time() - start_time < 30:
        line = process.stdout.readline()
        if line:
            print(line.rstrip())
        
        # Check if process has terminated
        if process.poll() is not None:
            print(f"\nProcess terminated with code: {process.returncode}")
            # Read any remaining output
            remaining = process.stdout.read()
            if remaining:
                print(remaining)
            break
        
        time.sleep(0.1)
    else:
        print("\n30 seconds elapsed, server still running!")
        process.terminate()
        
except KeyboardInterrupt:
    print("\nInterrupted by user")
    process.terminate()

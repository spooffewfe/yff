import os
import time
import sys

# Suppress all output
class DevNull:
    def write(self, _): pass
    def flush(self): pass

sys.stdout = DevNull()
sys.stderr = DevNull()

def animated_text(text, color_code):
    # Temporarily restore stdout for animated text
    sys.stdout = sys.__stdout__
    for char in text:
        print(f"\x1b[38;2;{color_code}m{char}", end="", flush=True)
        time.sleep(0.1)
    print("\n")
    # Suppress output again after showing the animation
    sys.stdout = DevNull()

# Show animated text
animated_text("Installing Dependencies...", "0;255;58")

# Automatically install the required packages using 'python -m pip install'
os.system("python -m pip install -q cloudscraper")
os.system("python -m pip install -q socks")
os.system("python -m pip install -q pysocks")
os.system("python -m pip install -q colorama")
os.system("python -m pip install -q undetected_chromedriver")
os.system("python -m pip install -q httpx")
os.system("python -m pip install -q setuptools")

if os.name != "nt":
    os.system("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    os.system("apt-get install -qq ./google-chrome-stable_current_amd64.deb")

# Restore stdout and print completion message
sys.stdout = sys.__stdout__
print("Done.")

import os
import time

def animated_text(text, color_code):
    for char in text:
        print(f"\x1b[38;2;{color_code}m{char}", end="", flush=True)
        time.sleep(0.1)
    print("\n")

# Start the installation process with animated text
animated_text("Installing Dependencies...", "0;255;58")

# Automatically install the required packages using 'python -m pip install'
os.system("python -m pip install cloudscraper")
os.system("python -m pip install socks")
os.system("python -m pip install pysocks")
os.system("python -m pip install colorama")
os.system("python -m pip install undetected_chromedriver")
os.system("python -m pip install httpx")

if os.name != "nt":
    os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    os.system("apt-get install ./google-chrome-stable_current_amd64.deb")

print("Done.")

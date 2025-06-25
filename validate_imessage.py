import subprocess
from pathlib import Path
import time

GOOD_FILE = Path("good.txt")
BAD_FILE = Path("bad.txt")
SCRIPT_PATH = Path("scripts/check_compatibility.applescript")

def is_imessage_user(phone_number: str) -> bool:
    """Checks if number is reachable via iMessage using AppleScript."""
    try:
        output = subprocess.check_output([
            "osascript",
            str(SCRIPT_PATH),
            phone_number
        ])
        return output.strip().lower() == b"true"
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] AppleScript failed for {phone_number}: {e}")
        return False

def validate_numbers(numbers_file="numbers.txt"):
    """Reads numbers from file and checks for iMessage compatibility."""
    with open(numbers_file, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]

    for number in numbers:
        print(f"\n[INFO] Checking {number}...")
        if is_imessage_user(number):
            print("[✓] iMessage supported.")
            with GOOD_FILE.open("a") as good:
                good.write(number + "\n")
        else:
            print("[✗] Not on iMessage.")
            with BAD_FILE.open("a") as bad:
                bad.write(number + "\n")
        time.sleep(0.5)

if __name__ == "__main__":
    validate_numbers()
import subprocess
import time
from pathlib import Path

GOOD_FILE = Path("good.txt")
BAD_FILE = Path("bad.txt")


def send_imessage(phone_number: str, message: str) -> bool:
    """Attempts to send iMessage and confirms success or failure."""
    applescript = f'''
    tell application "Messages"
        set iService to 1st service whose service type = iMessage
        try
            set iBuddy to buddy "{phone_number}" of iService
            send "{message}" to iBuddy
            return "success"
        on error errMsg
            return "error"
        end try
    end tell
    '''
    try:
        result = subprocess.check_output(["osascript", "-e", applescript])
        decoded = result.decode("utf-8").strip()
        return decoded == "success"
    except Exception as e:
        print(f"[ERROR] AppleScript failed: {e}")
        return False


def validate_and_send(numbers_file="numbers.txt", message="Hello from Python iMessage bot!"):
    """Reads numbers, sends iMessages, and logs success/failure."""
    with open(numbers_file, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]

    for number in numbers:
        print(f"\n[INFO] Processing {number}...")

        if send_imessage(number, message):
            print("[✓] Message delivered successfully.")
            with GOOD_FILE.open("a") as good:
                good.write(number + "\n")
        else:
            print("[✗] Failed to send. Logged as bad.")
            with BAD_FILE.open("a") as bad:
                bad.write(number + "\n")

        time.sleep(1)


if __name__ == "__main__":
    validate_and_send()
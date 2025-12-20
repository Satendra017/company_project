import time
import subprocess
from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).parent
ORDERS_FILE = BASE_DIR / "data" / "orders.csv"

print("👀 Watching orders.csv for changes...")

last_modified_time = os.path.getmtime(ORDERS_FILE)

while True:
    try:
        current_modified_time = os.path.getmtime(ORDERS_FILE)

        if current_modified_time != last_modified_time:
            print("📥 New order detected. Running Ops Assistant...")

            # ✅ USE SAME PYTHON AS WATCHER
            subprocess.run(
                [sys.executable, "app.py"],
                check=True
            )

            last_modified_time = current_modified_time

        time.sleep(5)

    except KeyboardInterrupt:
        print("🛑 Watcher stopped.")
        break

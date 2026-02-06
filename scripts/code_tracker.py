import subprocess
import os
from collections import defaultdict
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
START_TIME = f"{today} 00:00"
END_TIME   = f"{today} 23:59"

cmd = [
    "git", "log",
    "--since", START_TIME,
    "--until", END_TIME,
    "--numstat",
    "--pretty=format:"
]

result = subprocess.run(cmd, capture_output=True, text=True)

language_lines = defaultdict(int)

for line in result.stdout.split("\n"):
    parts = line.split("\t")
    if len(parts) == 3:
        added, removed, filename = parts
        if added.isdigit():
            ext = filename.split(".")[-1]
            language_lines[ext] += int(added)

report_content = "\n📊 Code Report\n"
report_content += f"From {START_TIME} → {END_TIME}\n\n"

for lang, lines in language_lines.items():
    report_content += f"{lang.upper():6} : {lines} lines\n"

print(report_content)

log_dir = "daily_code_logs"
os.makedirs(log_dir, exist_ok=True)

with open(os.path.join(log_dir, f"{today}.txt"), "w") as f:
    f.write(report_content)

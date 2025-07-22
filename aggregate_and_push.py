import subprocess
import os
from datetime import datetime

subprocess.run(["python3", "aggregate_statistics"], check=True)

subprocess.run(["git", "add", "."], check=True)
subprocess.run(
    ["git", "commit", "-m", f"Auto update {datetime.now().isoformat()}"], check=True
)
subprocess.run(["git", "push"], check=True)

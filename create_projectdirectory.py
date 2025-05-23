#!/usr/bin/env python3
import os
from pathlib import Path

# Define the directory structure and files
dirs = [
    "config",
    "data",
    "output",
    os.path.join(".github", "workflows"),
]

files = [
    "etl_pipeline.py",
    "scheduler.py",
    "load_to_db.py",
    "requirements.txt",
    "README.md",
    "report.pdf",
    os.path.join("config", "db_config.json"),
    os.path.join("data", "sample_data.csv"),
    os.path.join("data", "sample_weather.json"),
    os.path.join("data", "google_sheet_sample.csv"),
    os.path.join(".github", "workflows", "ci_cd.yml"),
]

def main():
    # Create directories
    for d in dirs:
        path = Path(d)
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {path}")

    # Create empty files
    for f in files:
        path = Path(f)
        if not path.exists():
            path.touch()
            print(f"Created file: {path}")
        else:
            print(f"Already exists: {path}")

if __name__ == "__main__":
    main()

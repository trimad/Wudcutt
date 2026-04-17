import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
existing = os.environ.get("PYTHONPATH", "")
os.environ["PYTHONPATH"] = str(ROOT) if not existing else f"{ROOT}:{existing}"

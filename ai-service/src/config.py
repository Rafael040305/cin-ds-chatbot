import os
from pathlib import Path


AI_SERVICE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = AI_SERVICE_DIR.parent

DATA_DIR = Path(
    os.getenv("SECGRAD_DATA_DIR") or PROJECT_ROOT / "data" / "raw"
)

CHROMA_PATH = Path(
    os.getenv("SECGRAD_CHROMA_PATH") or AI_SERVICE_DIR / "chroma_db"
)

COLLECTION_NAME = os.getenv(
    "SECGRAD_COLLECTION",
    "secgrad_normas",
)
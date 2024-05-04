import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Paths:
    root: Path = Path(__file__).parent
    data: Path = root / "data"
    documents: Path = (
        data
        / "Document_Source/documents.html"
    )
    models: Path = (
        data
        / "Document_Source/models.html"
    )


openai_api_key = os.getenv("OPENAI_API_KEY")

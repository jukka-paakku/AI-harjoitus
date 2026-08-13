from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ImageCandidate:
    source: Path
    similar: Path
    similarity: float
    status: str = "pending"


@dataclass(frozen=True)
class ScanResult:
    scanned_files: int
    candidates: tuple[ImageCandidate, ...]

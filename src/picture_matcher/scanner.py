from collections.abc import Iterable
from hashlib import sha256
from pathlib import Path

from picture_matcher.types import ImageCandidate, ScanResult

IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg"})
SAMPLE_SIZE = 64 * 1024


def list_image_files(folder: Path) -> tuple[Path, ...]:
    """Return supported image files directly inside a folder, sorted by name."""
    return tuple(
        sorted(
            (path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS),
            key=lambda path: path.name.lower(),
        )
    )


def sample_digest(path: Path) -> bytes:
    """Hash the start and end of a file, keeping comparisons cheap for large images."""
    size = path.stat().st_size
    with path.open("rb") as image_file:
        start = image_file.read(SAMPLE_SIZE)
        image_file.seek(max(0, size - SAMPLE_SIZE))
        end = image_file.read(SAMPLE_SIZE)
    return sha256(start + end).digest()


def digest_similarity(first: bytes, second: bytes) -> float:
    """Return the percentage of equal digest bits."""
    equal_bits = sum((~(left ^ right) & 0xFF).bit_count() for left, right in zip(first, second, strict=True))
    return round((equal_bits / (len(first) * 8)) * 100, 2)


def find_similar_images(files: Iterable[Path], threshold: float) -> tuple[ImageCandidate, ...]:
    """Compare image-file samples pairwise and return candidates at the threshold."""
    items = tuple(files)
    digests = {path: sample_digest(path) for path in items}
    candidates: list[ImageCandidate] = []
    for index, source in enumerate(items):
        for similar in items[index + 1 :]:
            similarity = digest_similarity(digests[source], digests[similar])
            if similarity >= threshold:
                candidates.append(ImageCandidate(source=source, similar=similar, similarity=similarity))
    return tuple(candidates)


def scan(folder: Path, threshold: float = 90.0) -> ScanResult:
    if not folder.is_dir():
        raise ValueError(f"Lähdekansiota ei löydy: {folder}")
    files = list_image_files(folder)
    return ScanResult(scanned_files=len(files), candidates=find_similar_images(files, threshold))

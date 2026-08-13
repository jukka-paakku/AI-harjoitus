from os import chmod
from pathlib import Path
from shutil import move

from picture_matcher.database import open_database, replace_candidates
from picture_matcher.scanner import scan
from picture_matcher.types import ScanResult


def run_scan(source: Path, database_path: Path, threshold: float) -> ScanResult:
    result = scan(source, threshold)
    with open_database(database_path) as connection:
        replace_candidates(connection, result.candidates)
    return result


def move_candidates(result: ScanResult, destination: Path) -> int:
    destination.mkdir(mode=0o750, parents=True, exist_ok=True)
    chmod(destination, 0o750)
    files_to_move = {candidate.similar for candidate in result.candidates}
    destinations = {image_file: destination / image_file.name for image_file in files_to_move}
    existing_files = [target for target in destinations.values() if target.exists()]
    if existing_files:
        raise FileExistsError(f"Kohdetiedosto on jo olemassa: {existing_files[0]}")

    moved = 0
    for image_file in sorted(files_to_move, key=lambda path: path.name.lower()):
        move(str(image_file), str(destinations[image_file]))
        moved += 1
    return moved

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from picture_matcher.scanner import digest_similarity, list_image_files
from picture_matcher.service import move_candidates
from picture_matcher.types import ImageCandidate, ScanResult


class ScannerTests(unittest.TestCase):
    def test_digest_similarity_is_100_for_identical_digests(self) -> None:
        digest = bytes(32)
        self.assertEqual(digest_similarity(digest, digest), 100.0)

    def test_list_image_files_filters_extensions(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            temporary_folder = Path(temporary_directory)
            (temporary_folder / "first.jpg").touch()
            (temporary_folder / "second.jpeg").touch()
            (temporary_folder / "third.png").touch()
            (temporary_folder / "notes.txt").touch()
            self.assertEqual(
                [path.name for path in list_image_files(temporary_folder)],
                ["first.jpg", "second.jpeg"],
            )

    def test_move_keeps_first_image_and_moves_duplicate(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "source"
            destination = Path(temporary_directory) / "duplicates"
            source.mkdir()
            original = source / "original.jpg"
            duplicate = source / "duplicate.jpeg"
            original.write_bytes(b"original")
            duplicate.write_bytes(b"original")
            result = ScanResult(
                scanned_files=2,
                candidates=(ImageCandidate(source=original, similar=duplicate, similarity=100.0),),
            )

            moved = move_candidates(result, destination)

            self.assertEqual(moved, 1)
            self.assertTrue(original.exists())
            self.assertFalse(duplicate.exists())
            self.assertTrue((destination / "duplicate.jpeg").exists())

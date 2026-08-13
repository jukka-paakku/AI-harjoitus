import argparse
from pathlib import Path

from picture_matcher.service import move_candidates, run_scan


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Etsi samankaltaisia kuvatiedostoja.")
    parser.add_argument("source", type=Path, help="Skannattava kuvakansio")
    parser.add_argument("--destination", type=Path, help="Kansio, johon ehdokaskuvat siirretään")
    parser.add_argument("--move", action="store_true", help="Siirrä ehdokaskuvat kohdekansioon")
    parser.add_argument("--threshold", type=float, default=90.0, help="Samankaltaisuusraja (0-100)")
    parser.add_argument("--database", type=Path, default=Path("data/images.db"), help="SQLite-tietokannan polku")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if not 0 <= arguments.threshold <= 100:
        raise ValueError("Samankaltaisuusrajan tulee olla välillä 0-100.")
    if arguments.move and arguments.destination is None:
        raise ValueError("--move vaatii --destination-kansion.")

    result = run_scan(arguments.source, arguments.database, arguments.threshold)
    print(f"Skannattu: {result.scanned_files}; ehdokkaita: {len(result.candidates)}")
    for candidate in result.candidates:
        print(f"{candidate.similarity:5.2f}%  {candidate.source.name} <-> {candidate.similar.name}")
    if arguments.move:
        print(f"Siirretty {move_candidates(result, arguments.destination)} kuvaa.")


if __name__ == "__main__":
    main()

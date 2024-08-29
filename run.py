import argparse
import logging
import pathlib

exclude_dirs = [".git", "__pycache__"]


def main():
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_dir", help="Path to the directory to search for text files"
    )
    parser.add_argument(
        "output_file",
        help="Path to the file where the concatenated content will be saved",
    )
    args = parser.parse_args()

    root_dir = pathlib.Path(args.input_dir)
    output_file = pathlib.Path(args.output_file)

    if not (root_dir / ".git").exists():
        raise FileNotFoundError(f".git directory not found in {root_dir}")

    with open(output_file, "w", encoding="utf-8") as out_f:
        for path in root_dir.rglob("*"):
            if (
                any(excluded in path.parts for excluded in exclude_dirs)
                or path.is_dir()
            ):
                continue

            try:
                with open(path, "r", encoding="utf-8") as f:
                    contents = f.read()
            except Exception as e:
                logging.warning(f"Could not read file {path}: {e}")
                continue

            out_f.write("-" * 8 + "\n")
            out_f.write(str(path) + "\n")
            out_f.write(contents + "\n")


if __name__ == "__main__":
    main()

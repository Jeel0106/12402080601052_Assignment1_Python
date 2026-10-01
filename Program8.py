import pickle
import re
import zipfile
from collections import defaultdict
from pathlib import Path


def build_index(folder, zip_name):
    folder = Path(folder)

    if not folder.is_dir():
        raise Exception("Folder not found")

    files = []
    index = defaultdict(list)
    total_lines = 0

    for file in sorted(folder.iterdir()):
        if file.is_file() and file.suffix == ".txt":
            files.append(file)

            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                for line_number, line in enumerate(f, 1):
                    total_lines += 1
                    words = re.findall(r"[A-Za-z0-9_]+", line)
                    words = set(word.lower() for word in words)

                    for word in words:
                        index[word].append((file.name, line_number))

    pickle_file = folder / "log_index.pkl"

    with open(pickle_file, "wb") as f:
        pickle.dump(dict(index), f)

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
        for file in files:
            z.write(file, file.name)
        z.write(pickle_file, pickle_file.name)

    print("FILES", len(files))
    print("LINES", total_lines)
    print("TOKENS", len(index))


def search_index(pickle_file, words):
    with open(pickle_file, "rb") as f:
        index = pickle.load(f)

    for word in words:
        print(word + ":")
        for file, line in index.get(word.lower(), []):
            print(file + ":" + str(line))


def main():
    try:
        first = input().strip()

        if first.upper().startswith("BUILD "):
            parts = first.split()
            build_index(parts[1], parts[2])

        elif first.upper() == "BUILD":
            folder, zip_name = input().split()
            build_index(folder, zip_name)

        elif first.upper().startswith("SEARCH "):
            pickle_file = first.split(maxsplit=1)[1]
            q = int(input())
            words = [input().strip() for i in range(q)]
            search_index(pickle_file, words)

        elif first.upper() == "SEARCH":
            pickle_file = input().strip()
            q = int(input())
            words = [input().strip() for i in range(q)]
            search_index(pickle_file, words)

        else:
            print("ERROR")

    except Exception:
        print("ERROR")


if __name__ == "__main__":
    main()

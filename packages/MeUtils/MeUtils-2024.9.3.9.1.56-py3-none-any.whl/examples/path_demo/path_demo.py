from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIR = Path(__file__).absolute().parent


print(BASE_DIR)
print(DIR)
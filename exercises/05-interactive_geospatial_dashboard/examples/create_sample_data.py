from pathlib import Path
from app.data import create_sample_data

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    paths = create_sample_data(root / "sample_data")
    for name, path in paths.items():
        print(f"{name}: {path}")

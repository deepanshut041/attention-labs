"""Export this source checkout for upload to a Colab runtime."""
import argparse
import json
from pathlib import Path
from utils.colab_export import export_bundle

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "artifacts/colab")
    args = parser.parse_args()
    print(json.dumps(export_bundle(root, args.output), indent=2))

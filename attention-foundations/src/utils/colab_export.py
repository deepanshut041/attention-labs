"""Export only public source needed by the Colab runner."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

PUBLIC_FILES = ("README.md", "COLAB.md", "pyproject.toml", "uv.lock",
                ".python-version", ".gitignore", ".ai-project.toml")
DIRECTORIES = ("src", "tests", "notebooks")
SUFFIXES = (".py", ".toml", ".ipynb")

def export_bundle(root: Path, output: Path) -> dict:
    root, output = root.resolve(), output.resolve()
    if output == root or any(output.is_relative_to(root / name) for name in DIRECTORIES):
        raise ValueError("Export into artifacts/colab or a directory outside public source folders")
    paths = [root / name for name in PUBLIC_FILES]
    for directory in DIRECTORIES:
        paths.extend(p for p in (root / directory).rglob("*")
                     if p.is_file() and p.suffix in SUFFIXES
                     and "__pycache__" not in p.parts and ".ipynb_checkpoints" not in p.parts)
    payloads = {}
    for path in sorted(paths):
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Missing or non-regular public source: {path}")
        raw = path.read_bytes()
        if path.suffix == ".ipynb":
            notebook = json.loads(raw)
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    cell["outputs"], cell["execution_count"] = [], None
            raw = (json.dumps(notebook, indent=2) + "\n").encode()
        payloads[path.relative_to(root).as_posix()] = raw
    try:
        source_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root,
                                                 text=True, stderr=subprocess.DEVNULL).strip()
        dirty = bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", "."],
            cwd=root, text=True, stderr=subprocess.DEVNULL).strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        source_revision, dirty = None, None
    output.mkdir(parents=True, exist_ok=True)
    archive = output / "attention-foundations-source.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, raw in sorted(payloads.items()):
            info = zipfile.ZipInfo("attention-foundations/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, raw)
    manifest = {"schema_version": 1, "project_id": "attention-foundations",
                "source_revision": source_revision, "working_tree": dirty,
                "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                "files": {name: hashlib.sha256(raw).hexdigest() for name, raw in sorted(payloads.items())}}
    (output / "source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (output / "attention_foundations_colab.ipynb").write_bytes(payloads["notebooks/attention_foundations_colab.ipynb"])
    return {"archive": str(archive), "manifest": str(output / "source-manifest.json"),
            "notebook": str(output / "attention_foundations_colab.ipynb"),
            "files": len(payloads), "source_revision": source_revision, "working_tree": dirty}

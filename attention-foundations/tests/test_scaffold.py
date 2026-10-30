"""Boilerplate boundaries and the actual notebook source-transfer contract."""
from pathlib import Path
import hashlib
import io
import json
import shutil
import sys
import types
import zipfile

import pytest
import torch

from core.config import load_config
from data.fixtures import example_inputs
from utils.colab_export import export_bundle, PUBLIC_FILES, DIRECTORIES
from utils.commands import main

ROOT = Path(__file__).resolve().parents[1]

def test_setup_from_another_directory_is_only_setup(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["check"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["setup_checks"]["autograd_probe"] == "passed"
    assert result["implemented_mechanisms"] == []
    assert result["attention_correctness_verified"] is False
    assert result["hosted_colab_verified"] is False
    assert list(tmp_path.iterdir()) == []

@pytest.mark.parametrize("name", load_config()["scope"]["mechanisms"])
def test_pending_mechanisms_do_not_create_results(name, capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["mechanism", "--name", name]) == 2
    result = json.loads(capsys.readouterr().err)
    assert result["status"] == "not_implemented"
    assert result["implemented_mechanisms"] == []
    assert list(tmp_path.iterdir()) == []

def test_multihead_does_not_enter_the_single_head_scope(capsys):
    assert main(["mechanism", "--name", "GQA"]) == 1
    assert "single-head" in json.loads(capsys.readouterr().err)["message"]

@pytest.mark.parametrize("old,new", [
    ('dtype = "float64"', 'dtype = "float16"'),
    ('seed = 17', 'seed = -1'),
    ('absolute_tolerance = 1e-10', 'absolute_tolerance = 0'),
])
def test_invalid_correctness_profile_fails(old, new, tmp_path):
    p = tmp_path / "invalid.toml"
    p.write_text((ROOT / "src/core/project.toml").read_text().replace(old, new))
    with pytest.raises(ValueError):
        load_config(p)

def test_fixture_is_a_fresh_cpu_float64_input():
    first = example_inputs()
    first[0, 0] = 99
    second = example_inputs()
    assert second.tolist() == [[1., 0.], [0., 1.], [1., 1.]]
    assert second.device.type == "cpu" and second.dtype == torch.float64

@pytest.fixture
def public_source(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    for name in PUBLIC_FILES:
        shutil.copyfile(ROOT / name, source / name)
    for directory in DIRECTORIES:
        shutil.copytree(ROOT / directory, source / directory,
                        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    for name in ["docs/private.md", "data/private.txt", ".sources/caption.vtt",
                 "weights/private.pt", "artifacts/old-run.json", ".venv/private.txt"]:
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("not public source")
    return source

def test_source_export_is_complete_repeatable_and_private(public_source, tmp_path):
    first = export_bundle(public_source, tmp_path / "one")
    second = export_bundle(public_source, tmp_path / "two")
    manifest = json.loads(Path(first["manifest"]).read_text())
    assert Path(first["archive"]).read_bytes() == Path(second["archive"]).read_bytes()
    assert manifest["archive_sha256"] == hashlib.sha256(Path(first["archive"]).read_bytes()).hexdigest()
    with zipfile.ZipFile(first["archive"]) as z:
        names = {name.removeprefix("attention-foundations/") for name in z.namelist()}
        assert names == set(manifest["files"])
        assert "uv.lock" in names and "src/data/fixtures.py" in names
        assert not any(name.startswith(("docs/", "data/", ".sources/", "weights/", "artifacts/", ".venv/")) for name in names)
        for name in names:
            assert hashlib.sha256(z.read("attention-foundations/" + name)).hexdigest() == manifest["files"][name]

def test_export_clears_notebook_output_without_editing_the_source(public_source, tmp_path):
    p = public_source / "notebooks/attention_foundations_colab.ipynb"
    n = json.loads(p.read_text())
    cell = next(c for c in n["cells"] if c["cell_type"] == "code")
    cell["outputs"] = [{"output_type": "stream", "name": "stdout", "text": ["old result"]}]
    cell["execution_count"] = 7
    p.write_text(json.dumps(n))
    original = p.read_bytes()
    result = export_bundle(public_source, tmp_path / "export")
    exported = json.loads(Path(result["notebook"]).read_text())
    assert all(not c["outputs"] and c["execution_count"] is None
               for c in exported["cells"] if c["cell_type"] == "code")
    assert p.read_bytes() == original

@pytest.mark.parametrize("corruption", ["none", "archive-hash", "member-hash", "traversal"])
def test_notebook_upload_verifies_before_extracting(public_source, tmp_path, monkeypatch, corruption):
    result = export_bundle(public_source, tmp_path / "export")
    archive = Path(result["archive"]).read_bytes()
    manifest = json.loads(Path(result["manifest"]).read_text())
    if corruption in ("member-hash", "traversal"):
        output = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(archive)) as before, zipfile.ZipFile(output, "w") as after:
            for name in before.namelist():
                payload = before.read(name)
                if corruption == "member-hash" and name.endswith("/README.md"):
                    payload += b"\nchanged"
                after.writestr(name, payload)
            if corruption == "traversal":
                after.writestr("attention-foundations/../outside.py", b"changed")
        archive = output.getvalue()
        manifest["archive_sha256"] = hashlib.sha256(archive).hexdigest()
    elif corruption == "archive-hash":
        archive += b"changed"
    uploaded = {"attention-foundations-source.zip": archive,
                "source-manifest.json": json.dumps(manifest).encode()}
    google, colab = types.ModuleType("google"), types.ModuleType("google.colab")
    colab.files = types.SimpleNamespace(upload=lambda: uploaded)
    google.colab = colab
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.colab", colab)
    notebook = json.loads((ROOT / "notebooks/attention_foundations_colab.ipynb").read_text())
    source = "".join(next(c for c in notebook["cells"] if c["cell_type"] == "code")["source"])
    assert 'dir="/content"' in source
    content = tmp_path / "content"
    content.mkdir()
    source = source.replace('dir="/content"', "dir=" + repr(str(content)))
    namespace = {}
    if corruption == "none":
        exec(compile(source, "<colab-upload-cell>", "exec"), namespace)
        assert (namespace["SOURCE"] / "src/check_setup.py").is_file()
        assert len(list(content.iterdir())) == 1
    else:
        with pytest.raises(ValueError):
            exec(compile(source, "<colab-upload-cell>", "exec"), namespace)
        assert list(content.iterdir()) == []

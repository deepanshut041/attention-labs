"""Read the installed configuration without depending on a working directory."""
from importlib import resources
from pathlib import Path
import math
import tomllib

PROJECT_ID = "attention-foundations"
MECHANISMS = {"additive", "dot-product", "scaled-dot-product", "self-attention", "projected-self-attention", "causal-attention"}

def load_config(path: Path | None = None) -> dict:
    text = path.read_text() if path is not None else resources.files("core").joinpath("project.toml").read_text()
    config = tomllib.loads(text)
    if type(config.get("schema_version")) is not int or config["schema_version"] != 1 or config.get("project_id") != PROJECT_ID:
        raise ValueError("Configuration must identify attention-foundations schema 1")
    scope = config.get("scope", {}).get("mechanisms")
    if not isinstance(scope, list) or not all(isinstance(x, str) for x in scope) or set(scope) != MECHANISMS or len(set(scope)) != len(scope):
        raise ValueError("Declare a nonempty, unique mechanism scope")
    experiment = config["experiment"]
    if experiment.get("device") != "cpu" or experiment.get("dtype") != "float64":
        raise ValueError("This initial correctness profile requires CPU float64")
    if type(experiment.get("seed")) is not int or experiment["seed"] < 0:
        raise ValueError("Seed must be a nonnegative integer")
    for key in ("absolute_tolerance", "relative_tolerance"):
        value = experiment.get(key)
        if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
            raise ValueError("Numerical tolerances must be finite and positive")
    return config

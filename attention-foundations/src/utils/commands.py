"""Runnable setup commands; mechanism execution remains explicitly pending."""
import argparse
import json
from pathlib import Path
import platform
import sys

from core.config import PROJECT_ID, load_config
from core.workflow import pending_result

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build and test basic single-head attention")
    parser.add_argument("action", nargs="?", default="status", choices=["status", "check", "show-config", "mechanism"])
    parser.add_argument("--name", help="Mechanism to build/test after its implementation phase")
    parser.add_argument("--config", type=Path)
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        if args.action == "mechanism":
            if args.name is None:
                raise ValueError("Select a mechanism with --name")
            print(json.dumps(pending_result(args.name, config), indent=2), file=sys.stderr)
            return 2
        result = config if args.action == "show-config" else {
            "project": PROJECT_ID, "status": "boilerplate", "goal": config["goal"],
            "planned_mechanisms": config["scope"]["mechanisms"],
            "implemented_mechanisms": [], "attention_correctness_verified": False,
            "hosted_colab_verified": False}
        if args.action == "check":
            import numpy
            import torch
            from data.fixtures import example_inputs
            if sys.version_info[:2] != (3, 12):
                raise ValueError("Use the project's Python 3.12 environment")
            probe = torch.tensor([1., -2.], dtype=torch.float64, requires_grad=True)
            loss = probe.square().sum()
            loss.backward()
            if loss.item() != 5 or probe.grad.tolist() != [2., -4.]:
                raise ValueError("CPU autograd setup probe failed")
            fixture = example_inputs()
            if list(fixture.shape) != [3, 2] or fixture.dtype != torch.float64 or fixture.device.type != "cpu":
                raise ValueError("Numerical fixture setup is inconsistent")
            result["setup_checks"] = {
                "python": platform.python_version(), "torch": torch.__version__,
                "numpy": numpy.__version__, "device": "cpu", "dtype": "float64",
                "fixture_shape": list(fixture.shape), "autograd_probe": "passed",
                "scope": "dependency/setup check, not an attention implementation"}
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}), file=sys.stderr)
        return 1

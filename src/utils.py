"""Small helpers shared by every pipeline stage."""

import random
import subprocess

import numpy as np
import yaml


def load_params(path: str = "params.yaml") -> dict:
    """Read the single source of truth for hyperparameters, split and seed."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def set_seed(seed: int) -> None:
    """Seed Python and NumPy global RNGs (sklearn objects get random_state explicitly)."""
    random.seed(seed)
    np.random.seed(seed)


def git_info() -> dict:
    """Return the current commit SHA and whether src/ has uncommitted changes."""
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain", "--", "src", "dvc.yaml"], text=True
        ).strip()
        return {"git_commit": sha, "code_uncommitted": bool(dirty)}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"git_commit": "unknown", "code_uncommitted": True}

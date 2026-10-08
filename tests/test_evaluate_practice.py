"""Tests for the TrackEval bootstrap without TrackEval, lab data, or a network."""

import subprocess
import sys
from pathlib import Path

import evaluate_practice


def test_bootstrap_patches_numpy_in_child_process(tmp_path: Path) -> None:
    fake_script = tmp_path / "run_mot_challenge.py"
    fake_script.write_text(
        "import sys\n"
        "import numpy as np\n"
        "print(np.float is float, np.int is int, sys.argv[1:], __name__)\n"
    )

    result = subprocess.run(
        [sys.executable, "-c", evaluate_practice._TRACKEVAL_BOOTSTRAP, str(fake_script), "--A", "1"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.stdout.strip() == "True True ['--A', '1'] __main__"


def test_run_trackeval_uses_bootstrap(monkeypatch, tmp_path: Path) -> None:
    calls = []
    monkeypatch.setattr(evaluate_practice.subprocess, "run", lambda cmd, check: calls.append(cmd))

    evaluate_practice.run_trackeval(tmp_path, "nhom01", "LAB21", "train")

    cmd = calls[0]
    assert cmd[1:3] == ["-c", evaluate_practice._TRACKEVAL_BOOTSTRAP]
    assert cmd[3] == str(tmp_path / "scripts" / "run_mot_challenge.py")

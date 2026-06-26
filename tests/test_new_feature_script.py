import shutil
import subprocess
from pathlib import Path


def test_new_feature_script_creates_feature_and_test_scaffold(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    temp_repo = tmp_path / "repo"

    shutil.copytree(repo_root / "scripts", temp_repo / "scripts")
    shutil.copytree(repo_root / "templates", temp_repo / "templates")
    (temp_repo / "src").mkdir()
    (temp_repo / "tests").mkdir()

    result = subprocess.run(
        ["bash", str(temp_repo / "scripts" / "new_feature.sh"), "users"],
        capture_output=True,
        check=True,
        cwd=temp_repo,
        text=True,
    )

    assert (temp_repo / "src" / "users" / "router.py").exists()
    assert (temp_repo / "tests" / "users" / ".gitkeep").exists()
    assert "Created feature scaffold: src/users" in result.stdout
    assert "Created feature test scaffold: tests/users" in result.stdout

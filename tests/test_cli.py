import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from dotenv_to_json.cli import main


def test_missing_input_file_clean_error(tmp_path, capsys):
    missing = tmp_path / "does-not-exist.env"
    rc = main(["-i", str(missing)])
    assert rc == 1
    captured = capsys.readouterr()
    assert "does-not-exist.env" in captured.err
    assert "Traceback" not in captured.err


def test_valid_input_still_converts(tmp_path, capsys):
    env_file = tmp_path / "a.env"
    env_file.write_text("FOO=bar\n", encoding="utf-8")
    assert main(["-i", str(env_file)]) == 0
    assert json.loads(capsys.readouterr().out) == {"FOO": "bar"}

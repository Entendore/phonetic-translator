"""Tests for CLI."""
import pytest
from typer.testing import CliRunner
from cli import app

runner = CliRunner()


class TestCLITranslate:
    def test_basic_translate(self):
        result = runner.invoke(app, ["translate", "hello", "en", "es"])
        assert result.exit_code == 0

    def test_translate_json_output(self):
        result = runner.invoke(app, ["translate", "hello", "en", "es", "--json"])
        assert result.exit_code == 0
        import json
        data = json.loads(result.output)
        assert 'source' in data

    def test_translate_missing_args(self):
        result = runner.invoke(app, ["translate", "hello"])
        assert result.exit_code != 0


class TestCLITransliterate:
    def test_basic_transliterate(self):
        result = runner.invoke(app, ["transliterate", "hello", "en"])
        assert result.exit_code == 0


class TestCLILanguages:
    def test_list_languages(self):
        result = runner.invoke(app, ["languages"])
        assert result.exit_code == 0
        assert "en" in result.output


class TestCLIBatch:
    def test_batch_with_file(self, tmp_path):
        input_file = tmp_path / "input.txt"
        input_file.write_text("hello\ten\tes\nworld\ten\tfr\n")
        output_file = tmp_path / "output.jsonl"
        result = runner.invoke(app, ["batch", str(input_file), "--output", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        assert len(output_file.read_text().strip().split('\n')) == 2

"""Simple tests for wordcount.py. Run with: python -m pytest"""

from wordcount import count_words, main


def test_count_words():
    assert count_words("hello world") == 2
    assert count_words("  several   spaces\tand\nnew lines  ") == 5
    assert count_words("") == 0


def test_main_prints_count(tmp_path, capsys):
    path = tmp_path / "sample.txt"
    path.write_text("one two three\nfour\n", encoding="utf-8")
    assert main([str(path)]) == 0
    assert capsys.readouterr().out.strip() == "4"


def test_main_missing_file(tmp_path, capsys):
    assert main([str(tmp_path / "nope.txt")]) == 1
    assert "Cannot read" in capsys.readouterr().err


def test_main_needs_exactly_one_argument(capsys):
    assert main([]) == 2
    assert "Usage" in capsys.readouterr().err

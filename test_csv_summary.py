"""Simple tests for csv_summary.py. Run with: python -m pytest"""

import math

from csv_summary import format_summary, main, summarize


def test_row_count_and_averages():
    rows, averages, skipped = summarize(["price,qty", "10,1", "20,2", "30,6"])
    assert rows == 3
    assert averages == {"price": 20.0, "qty": 3.0}
    assert skipped == []


def test_decimals_and_negative_numbers():
    _, averages, _ = summarize(["x", "1.5", "-0.5", "2"])
    assert math.isclose(averages["x"], 1.0)


def test_text_columns_are_skipped():
    rows, averages, skipped = summarize(["name,score", "Ann,8", "Bob,6"])
    assert rows == 2
    assert averages == {"score": 7.0}
    assert skipped == ["name"]


def test_column_with_any_text_value_is_not_numeric():
    _, averages, skipped = summarize(["value", "1", "two", "3"])
    assert averages == {}
    assert skipped == ["value"]


def test_empty_cells_are_ignored():
    rows, averages, _ = summarize(["a,b", "1,", "3,4"])
    assert rows == 2
    assert averages == {"a": 2.0, "b": 4.0}


def test_header_only_file():
    rows, averages, skipped = summarize(["a,b"])
    assert rows == 0
    assert averages == {"a": None, "b": None}
    assert skipped == []


def test_completely_empty_file():
    assert summarize([]) == (0, {}, [])


def test_format_summary():
    text = format_summary(2, {"score": 7.0, "empty": None}, ["name"])
    assert text == (
        "Rows: 2\n"
        "Column averages:\n"
        "  score: 7\n"
        "  empty: n/a (no values)\n"
        "Not numeric: name"
    )


def test_main_prints_summary(tmp_path, capsys):
    path = tmp_path / "data.csv"
    path.write_text("name,price\napple,1.5\npear,2.5\n", encoding="utf-8")
    assert main([str(path)]) == 0
    assert capsys.readouterr().out == "Rows: 2\nColumn averages:\n  price: 2\nNot numeric: name\n"


def test_main_missing_file(tmp_path, capsys):
    assert main([str(tmp_path / "nope.csv")]) == 1
    assert "Cannot read" in capsys.readouterr().err


def test_main_needs_exactly_one_argument(capsys):
    assert main([]) == 2
    assert "Usage" in capsys.readouterr().err

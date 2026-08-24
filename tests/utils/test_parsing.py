# tests/utils/test_parsing.py

"""
tests/utils/test_parsing.py

Unit tests for parsing utilities.

These tests verify that parse_size() correctly converts human-readable
storage sizes into bytes and handles plain numeric values.
"""

import pytest

from app.utils.parsing import parse_size


class TestParseSize:
    """Tests for parse_size()."""

    # ==========================================================
    # Numeric Values
    # ==========================================================

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("0", 0),
            ("1", 1),
            ("1024", 1024),
            ("999999", 999999),
        ],
    )
    def test_parses_numeric_values(
        self,
        value,
        expected,
    ):
        """Parses plain integer values."""

        assert parse_size(value) == expected

    # ==========================================================
    # Kilobytes
    # ==========================================================

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("1KB", 1024),
            ("2KB", 2048),
            ("1.5KB", 1536),
        ],
    )
    def test_parses_kilobytes(
        self,
        value,
        expected,
    ):
        """Parses kilobyte values."""

        assert parse_size(value) == expected

    # ==========================================================
    # Megabytes
    # ==========================================================

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("1MB", 1024 ** 2),
            ("2MB", 2 * 1024 ** 2),
            ("0.5MB", 524288),
        ],
    )
    def test_parses_megabytes(
        self,
        value,
        expected,
    ):
        """Parses megabyte values."""

        assert parse_size(value) == expected

    # ==========================================================
    # Gigabytes
    # ==========================================================

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("1GB", 1024 ** 3),
            ("2GB", 2 * 1024 ** 3),
            ("1.25GB", int(1.25 * 1024 ** 3)),
        ],
    )
    def test_parses_gigabytes(
        self,
        value,
        expected,
    ):
        """Parses gigabyte values."""

        assert parse_size(value) == expected

    # ==========================================================
    # Formatting
    # ==========================================================

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (" 1kb ", 1024),
            ("10mb", 10 * 1024 ** 2),
            ("3Gb", 3 * 1024 ** 3),
        ],
    )
    def test_ignores_case_and_surrounding_whitespace(
        self,
        value,
        expected,
    ):
        """Ignores surrounding whitespace and unit casing."""

        assert parse_size(value) == expected

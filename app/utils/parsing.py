# app/utils/parsing.py

"""
Reusable parsing utilities.

This module contains helper functions that convert human-readable
values into strongly typed Python objects used throughout Custy.

Current helpers
---------------

parse_size()
    Convert storage sizes into bytes.

parse_duration()
    Convert human-readable duration strings into ``timedelta`` objects.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"

DAYS_PER_MONTH = 30

DAYS_PER_YEAR = 365


def parse_size(size: str) -> int:
    """
    Convert a human-readable storage size into bytes.

    Examples
    --------
    >>> parse_size("10MB")
    10485760

    >>> parse_size("1GB")
    1073741824

    Parameters
    ----------
    size:
        Human-readable storage size.

    Returns
    -------
    int
        Size expressed in bytes.

    Raises
    ------
    ValueError
        If the supplied value cannot be parsed.
    """

    size = size.strip().upper()

    units = {
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
    }

    for unit, multiplier in units.items():
        if size.endswith(unit):
            value = float(size.removesuffix(unit))
            return int(value * multiplier)

    return int(size)


def parse_duration(value: str) -> timedelta:
    """
    Convert a human-readable duration into a ``timedelta``.

    Supported units
    ---------------

    ====== ===========================
    Unit   Meaning
    ====== ===========================
    m      Minutes
    h      Hours
    d      Days
    w      Weeks
    mo     Months (30 days)
    y      Years (365 days)
    ====== ===========================

    Examples
    --------

    >>> parse_duration("30m")

    >>> parse_duration("12h")

    >>> parse_duration("30d")

    >>> parse_duration("2w")

    >>> parse_duration("6mo")

    >>> parse_duration("1y")

    Parameters
    ----------
    value:
        Duration string.

    Returns
    -------
    timedelta
        Parsed duration.

    Raises
    ------
    ValueError
        If the duration format is invalid.
    """

    value = value.strip().lower()

    match = re.fullmatch(
        r"(\d+)\s*(m|h|d|w|mo|y)",
        value,
    )

    if match is None:
        raise ValueError(
            "Invalid duration format. "
            "Supported examples: "
            "'30m', '12h', '30d', '2w', '6mo', '1y'."
        )

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "m":
        return timedelta(minutes=amount)

    if unit == "h":
        return timedelta(hours=amount)

    if unit == "d":
        return timedelta(days=amount)

    if unit == "w":
        return timedelta(weeks=amount)

    if unit == "mo":
        return timedelta(days=amount * DAYS_PER_MONTH)

    if unit == "y":
        return timedelta(days=amount * DAYS_PER_YEAR)

    raise ValueError(f"Unsupported duration unit: {unit}")


def parse_date(value: str) -> datetime:
    """
    Convert a date string into a ``datetime`` object.

    The accepted format follows the ISO-8601 calendar date:

    YYYY-MM-DD

    Examples
    --------
    >>> parse_date("2026-07-01")

    >>> parse_date("2025-12-31")

    Parameters
    ----------
    value:
        Date string.

    Returns
    -------
    datetime
        Parsed datetime object.

    Raises
    ------
    ValueError
        If the supplied date does not match the required
        ``YYYY-MM-DD`` format.
    """

    value = value.strip()

    try:
        return datetime.strptime(
            value,
            DATE_FORMAT,
        )
    except ValueError as exc:
        raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.") from exc

"""Test the update_copyright_date module."""

import pytest

from .. import update_copyright_date as ucd


@pytest.mark.parametrize(
    "line, symbol, owner, expected, year_string, final",
    [
        [
            "Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>",
            "(c)",
            "Free Software Foundation, Inc.",
            (["2007"], 14, 18),
            "2007",
            f"Copyright (C) 2007, {ucd.THIS_YEAR} Free Software Foundation, Inc. <http://fsf.org/>",
        ],
        [
            "Copyright 2015 Contrived Example",
            "Copyright",
            "Contrived Example",
            (["2015"], 10, 14),
            "2015",
            f"Copyright 2015, {ucd.THIS_YEAR} Contrived Example",
        ],
        [
            f"Copyright {ucd.LAST_YEAR} Contrived Example",
            "Copyright",
            "Contrived Example",
            ([ucd.LAST_YEAR], 10, 14),
            ucd.LAST_YEAR,
            f"Copyright {ucd.LAST_YEAR}-{ucd.THIS_YEAR} Contrived Example",
        ],
        [
            "# Copyright (C) 1988-2020 Free Software Foundation, Inc.",
            "(c)",
            "Inc.",
            (["1988", "2020"], 16, 25),
            "1988-2020",
            f"# Copyright (C) 1988-2020, {ucd.THIS_YEAR} Free Software Foundation, Inc.",
        ],
        [
            "# Copyright (c) 2006, 2008 Junio C Hamano",
            "Copyright (c)",
            "Junio C Hamano",
            (["2006", "2008"], 16, 26),
            "2006, 2008",
            f"# Copyright (c) 2006, 2008, {ucd.THIS_YEAR} Junio C Hamano",
        ],
        [
            "Copyright (C) 2000, 2001, 2002, 2007, 2008 Free Software Foundation, Inc.",
            "(c)",
            "Free Software Foundation",
            (["2000", "2001", "2002", "2007", "2008"], 14, 42),
            "2000, 2001, 2002, 2007, 2008",
            f"Copyright (C) 2000, 2001, 2002, 2007, 2008, {ucd.THIS_YEAR} Free Software Foundation, Inc.",
        ],
        [
            f"Copyright (c) 1215, 1871, 1973, 1975-1991, {ucd.THIS_YEAR} Some Project Owner",
            "(c)",
            "Some Project Owner",
            (["1215", "1871", "1973", "1975", "1991", ucd.THIS_YEAR], 14, 47),
            f"1215, 1871, 1973, 1975-1991, {ucd.THIS_YEAR}",
            f"Copyright (c) 1215, 1871, 1973, 1975-1991, {ucd.THIS_YEAR} Some Project Owner",
        ],
        [
            f'copyright = "(c) 2014 - {ucd.THIS_YEAR}, Project Copyright Owner"',
            "(c)",
            "Project Copyright Owner",
            (["2014", ucd.THIS_YEAR], 17, 28),
            f"2014 - {ucd.THIS_YEAR}",
            f'copyright = "(c) 2014 - {ucd.THIS_YEAR}, Project Copyright Owner"',
        ],
        [
            f"Copyright (C) 2008-{ucd.LAST_YEAR} NeXus International Advisory Committee (NIAC)",
            "(C)",
            "NeXus International Advisory Committee (NIAC)",
            (["2008", ucd.LAST_YEAR], 14, 23),
            f"2008-{ucd.LAST_YEAR}",
            f"Copyright (C) 2008-{ucd.THIS_YEAR} NeXus International Advisory Committee (NIAC)",
        ],
        [
            f"Copyright (c) 1111, 1234, 2021 - {ucd.LAST_YEAR}, Some Project Owner",
            "(c)",
            "Some Project Owner",
            (["1111", "1234", "2021", ucd.LAST_YEAR], 14, 37),
            f"1111, 1234, 2021 - {ucd.LAST_YEAR}",
            f"Copyright (c) 1111, 1234, 2021 - {ucd.THIS_YEAR}, Some Project Owner",
        ],
        [
            f"Copyright (c) 1111, 1234, 2021, {ucd.LAST_YEAR}, A Project Team",
            "(c)",
            "A Project Team",
            (["1111", "1234", "2021", ucd.LAST_YEAR], 14, 36),
            f"1111, 1234, 2021, {ucd.LAST_YEAR}",
            f"Copyright (c) 1111, 1234, 2021, {ucd.LAST_YEAR}-{ucd.THIS_YEAR}, A Project Team",
        ],
        [
            f"# :copyright: (c) 2014-{ucd.LAST_YEAR}, D. Veloper\n",
            "(c)",
            "D. Veloper",
            (["2014", ucd.LAST_YEAR], 18, 27),
            f"2014-{ucd.LAST_YEAR}",
            f"# :copyright: (c) 2014-{ucd.THIS_YEAR}, D. Veloper\n",
        ],
    ],
)
def test_find_years_indices(line, symbol, owner, expected, year_string, final):
    result = ucd.find_years_indices(line, symbol, owner)
    assert result == expected

    p3, p4 = result[1:]
    assert line[p3:p4] == year_string

    result = ucd.revise_copyright_line(line, symbol, owner, ucd.THIS_YEAR)
    assert result == final

#! /usr/bin/env python3

__copyright__ = "(C) 2017-2024 Guido Draheim, licensed under the Apache License 2.0"""
__version__ = "1.6.3365"

from tabxlsx import tabtotext, print_tabtotext, print_tablist, CellValue, StrToTime, StrToDate
from tabxlsx import tabtoXLSX, tablistfileXLSX, tablistfile, tablistmap, tablistfor
from tabxlsx import TabSheet
from tabtotext import tablistscanGFM, tablistscanJSON
from typing import Optional, Union, Dict, List, Any, Sequence, Callable, Iterable, cast
import unittest
import datetime
import sys
from fnmatch import fnmatchcase as fnmatch
import os
import os.path as path
import shutil
import json
import inspect
from subprocess import getoutput
from datetime import date as Date
from datetime import datetime as Time
from datetime import timezone as TimeZone
from datetime import timedelta as Plus
from zipfile import ZipFile
from dataclasses import dataclass
from io import StringIO

import logging
logg = logging.getLogger("XLSX")
NIX = ""
LIST: List[str] = []
JSONLIST: List[Dict[str, str]] = []
KEEP = 0
TABTO = "./tabxlsx.py"
FIXME = True
BIGFILE = 100000


try:
    from tabtools import currency_default
    def X(line: str) -> str:
        return line.replace("$", chr(currency_default))
except ImportError as e:
    def X(line: str) -> str:
        return line


skipXLSX = False
def loadJSON(text: str) -> List[Dict[str, CellValue]]:
    tablist = tablistfile(StringIO(text), defaultformat="json")
    return tablist[0].data if tablist else []
def loadCSV(text: str) -> List[Dict[str, CellValue]]:
    tablist = tablistfile(StringIO(text), defaultformat="csv")
    return tablist[0].data if tablist else []
def loadGFM(text: str) -> List[Dict[str, CellValue]]:
    tablist = tablistfile(StringIO(text), defaultformat="md")
    return tablist[0].data if tablist else []

# ..............................

def readFromXLSX(filename: str) -> List[Dict[str, CellValue]]:
    tablist = tablistfileXLSX(filename)
    return tablist[0].data if tablist else []

def sh(cmd: str, *args: Any) -> str:
    logg.debug("sh %s", cmd)
    return getoutput(cmd, *args)
def get_caller_name() -> str:
    frame = inspect.currentframe().f_back.f_back  # type: ignore
    return frame.f_code.co_name  # type: ignore
def get_caller_caller_name() -> str:
    frame = inspect.currentframe().f_back.f_back.f_back  # type: ignore
    return frame.f_code.co_name  # type: ignore

JSONDict = Dict[str, CellValue]
JSONList = List[JSONDict]

def rev(data: List[JSONDict]) -> JSONList:
    return list(reversed(data))

class DataItem:
    """ Use this as the base class for dataclass types """
    def __getitem__(self, name: str) -> CellValue:
        return cast(CellValue, getattr(self, name))

DataList = List[DataItem]

@dataclass
class Item1(DataItem):
    b: CellValue

@dataclass
class Item2(DataItem):
    a: str
    b: int
    def foo(self, a: str) -> None:
        pass

#######################################################################

test003: JSONList = []
test004: JSONList = [{}]
# test004: JSONList = [{}, {}]
test005: JSONList = [{"a": "x"}]
test006: JSONList = [{"a": "x", "b": "y"}]
test007: JSONList = [{"b": "y", "a": "x"}, {"b": "v"}]
test007Q: JSONList = [{"b": "y", "a": "x"}, {"b": "v", "a": None}]
test008: JSONList = [{"a": "x"}, {"b": "v"}]
test008Q: JSONList = [{"b": None, "a": "x"}, {"b": "v", "a": None}]
test009: JSONList = [{}, {"b": "v"}]
test009Q: JSONList = [{"b": None}, {"b": "v"}]
test011: JSONList = [{"b": None}]
test011Q: JSONList = []
test012: JSONList = [{"b": False}]
test013: JSONList = [{"b": True}]
test014: JSONList = [{"b": ""}]
test015: JSONList = [{"b": "5678"}]
test015Q: JSONList = [{"b": 5678}]
test016: JSONList = [{"b": 123}]
test017: JSONList = [{"b": 123.4}]
test018: JSONList = [{"b": datetime.date(2021, 12, 31)}]
test018Q: JSONList = [{"b": datetime.datetime(2021, 12, 31, 0, 0)}]
test019Q: JSONList = [{"b": datetime.date(2021, 12, 31)}]
test019q: JSONList = [{"b": datetime.datetime(2021, 12, 31, 23, 34)}]
test019: JSONList = [{"b": datetime.datetime(2021, 12, 31, 23, 34, 45)}]

data011: DataList = [Item1(None)]
data012: DataList = [Item1(False)]
data013: DataList = [Item1(True)]
data014: DataList = [Item1("")]
data015: DataList = [Item1("5678")]
data016: DataList = [Item1(123)]
data017: DataList = [Item1(123.4)]
data018: DataList = [Item1(datetime.date(2021, 12, 31))]
data019: DataList = [Item1(datetime.datetime(2021, 12, 31))]

table01: JSONList = [{"a": "x y"}, {"b": 1}]
table01N: JSONList = [{'a': 'x y', 'b': None}, {'a': None, 'b': 1}]
table02: JSONList = [{"a": "x", "b": 0}, {"b": 2}]
table02N: JSONList = [{'a': 'x', 'b': 0}, {'a': None, 'b': 2}]
table22: JSONList = [{"a": "x", "b": 3}, {"b": 2, "a": "y"}]
table33: JSONList = [{"a": "x", "b": 3, "c": Date(2021, 12, 31)},
                     {"b": 2, "a": "y", "c": Date(2021, 12, 30)},
                     {"a": None, "c": Time(2021, 12, 31, 23, 34)}]
table33N: JSONList = [{"a": "x", "b": 3, "c": Date(2021, 12, 31)},
                      {"b": 2, "a": "y", "c": Date(2021, 12, 30)},
                      {"a": None, "b": None, "c": Time(2021, 12, 31, 23, 34)}]
table33Q: JSONList = [{"a": "x", "b": 3, "c": Date(2021, 12, 31)},
                      {"b": 2, "a": "y", "c": Date(2021, 12, 30)},
                      {"a": None, "b": None, "c": Date(2021, 12, 31)}]
table44: JSONList = [{"a": "x", "b": 3, "c": True, "d": 0.4},
                     {"b": 2, "a": "y", "c": False, "d": 0.3},
                     {"a": None, "b": None, "c": True, "d": 0.2},
                     {"a": "y", "b": 1, "d": 0.1}]
table44N: JSONList = [{"a": "x", "b": 3, "c": True, "d": 0.4},
                      {"b": 2, "a": "y", "c": False, "d": 0.3},
                      {"a": None, "b": None, "c": True, "d": 0.2},
                      {"a": "y", "b": 1, "c": None, "d": 0.1}]

def _none(data: JSONList, none: str = "") -> JSONList:
    rows: JSONList = []
    for datarow in data:
        row: JSONDict = datarow.copy()
        for name, value in row.items():
            if value is None:
                row[name] = none
        rows.append(row)
    return rows
def _date(data: JSONList, none: str = "") -> JSONList:
    rows: JSONList = []
    for datarow in data:
        row: JSONDict = datarow.copy()
        for name, value in row.items():
            if isinstance(value, Time):
                row[name] = value.date()
        rows.append(row)
    return rows

class TabXlsxTest(unittest.TestCase):
    def caller_testname(self) -> str:
        name = get_caller_caller_name()
        x1 = name.find("_")
        if x1 < 0: return name
        x2 = name.find("_", x1 + 1)
        if x2 < 0: return name
        return name[:x2]
    def testname(self, suffix: Optional[str] = None) -> str:
        name = self.caller_testname()
        if suffix:
            return name + "_" + suffix
        return name
    def testdir(self, testname: Optional[str] = None, keep: bool = False) -> str:
        testname = testname or self.caller_testname()
        newdir = "tmp/tmp." + testname
        if path.isdir(newdir) and not keep:
            shutil.rmtree(newdir)
        if not path.isdir(newdir):
            os.makedirs(newdir)
        return newdir
    def rm_testdir(self, testname: Optional[str] = None) -> str:
        testname = testname or self.caller_testname()
        newdir = "tmp/tmp." + testname
        if path.isdir(newdir):
            if not KEEP:
                shutil.rmtree(newdir)
        return newdir
    #
    def test_1100(self) -> None:
        time = StrToTime()
        want = Date(2022, 12, 23)
        have = time("2022-12-23")
        self.assertEqual(have, want)
        have = time("2022-12-23.")
        self.assertEqual(have, want)
    def test_1101(self) -> None:
        time = StrToTime()
        want = "2022-12-23T"
        have = time(want)
        self.assertEqual(have, want)
        want = "2022-12-2"
        have = time(want)
        self.assertEqual(have, want)
    def test_1102(self) -> None:
        time = StrToTime()
        want = Time(2022, 12, 23, 14, 45)
        have = time("2022-12-23T14:45")
        self.assertEqual(have, want)
        have = time("2022-12-23.14:45:00")
        self.assertEqual(have, want)
    def test_1103(self) -> None:
        time = StrToTime()
        want = "2022-12-23T14"
        have = time(want)
        self.assertEqual(have, want)
        want = "2022-12-23.14:"
        have = time(want)
        self.assertEqual(have, want)
        want = "2022-12-23.14:45:"
        have = time(want)
        self.assertEqual(have, want)
    def test_1104(self) -> None:
        time = StrToTime()
        want = Time(2022, 12, 23, 14, 45, tzinfo=TimeZone.utc)
        have = time("2022-12-23T14:45Z")
        self.assertEqual(have, want)
        have = time("2022-12-23.14:45:00 Z")
        self.assertEqual(have, want)
        have = time("2022-12-23.14:45:00 +00")
        self.assertEqual(have, want)
    def test_1105(self) -> None:
        time = StrToTime()
        want = "2022-12-23T14Z"
        have = time(want)
        self.assertEqual(have, want)
        want = "2022-12-23.14:45:Z"
        have = time(want)
        self.assertEqual(have, want)
        want = "2022-12-23.14:45:.Z"
        have = time(want)
        self.assertEqual(have, want)
    def test_1106(self) -> None:
        time = StrToTime()
        want = Time(2022, 12, 23, 14, 45, tzinfo=TimeZone(Plus(hours=1)))
        have = time("2022-12-23T14:45+01")
        self.assertEqual(have, want)
        have = time("2022-12-23.14:45:00 +0100")
        self.assertEqual(have, want)
        have = time("2022-12-23.14:45:00 +01:00")
        self.assertEqual(have, want)
    def test_1107(self) -> None:
        time = StrToTime()
        want = "2022-12-23T14+01"
        have = time(want)
        self.assertEqual(have, want)
        want = "2022-12-23.14:45:+01"
        have = time(want)
        self.assertEqual(have, want)
        want = "2022-12-23.14:45:+01.00"
        have = time(want)
        self.assertEqual(have, want)
    def test_1109(self) -> None:
        BB = 880 * 1000
        time = StrToTime()
        want = Time(2022, 12, 23, 14, 45, 55, BB, tzinfo=TimeZone(Plus(hours=-1)))
        have = time("2022-12-23T14:45:55.88-01")
        self.assertEqual(have, want)
        have = time("2022-12-23.14:45:55.880 -0100")
        self.assertEqual(have, want)
        have = time("2022-12-23.14:45:55.880000 -01:00")
        self.assertEqual(have, want)
    def test_1110(self) -> None:
        time = StrToDate()
        want = Date(2022, 12, 23)
        have = time("2022-12-23")
        self.assertEqual(have, want)
        have = time("2022-12-23.")
        self.assertEqual(have, want)
        have = time("2022-12-23T23:45")
        self.assertEqual(have, want)
        have = time("2022-12-23++++")
        self.assertEqual(have, want)
    def test_1111(self) -> None:
        time = StrToDate()
        want = "2022-12-234"
        have = time(want)
        self.assertEqual(have, want)
        want = "2022-12-2"
        have = time(want)
        self.assertEqual(have, want)
    #
    def test_4103(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test003, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test003, text)
        want = JSONLIST
        cond = ['']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4104(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test004, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        want = JSONLIST
        cond = ['', '', ]
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4105(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test005, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test005, text)
        want = test005
        cond = ['a', 'x', ]
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4106(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test006, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test006, text)
        want = test006
        cond = ['a;b', 'x;y', ]
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4107(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test007, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test007, text)
        want = test007Q
        cond = ['a;b', 'x;y', '~;v']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4108(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test008, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test008, text)
        want = test008Q
        cond = ['a;b', 'x;~', '~;v']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4109(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test009, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test009, text)
        want = test009Q
        cond = ['b', '~', 'v']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4111(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test011, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test011, text)
        want = test011
        cond = ['b', '~']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4112(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test012, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test012, text)
        want = test012
        cond = ['b', '(no)']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4113(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test013, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test013, text)
        want = test013
        cond = ['b', '(yes)']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4114(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test014, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test014, text)
        want = test014
        cond = ['b', '""']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4115(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test015, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test015, text)
        want = test015Q
        cond = ['b', '5678']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4116(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test016, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test016, text)
        want = test016
        cond = ['b', '123']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        if back[0]['b'] == "123":
            back[0]['b'] = 123
        self.assertEqual(want, back)
    def test_4117(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test017, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test017, text)
        want = test017
        cond = ['b', '123.40']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        if back[0]['b'] == "123.40":
            back[0]['b'] = 123.4
        self.assertEqual(want, back)
    def test_4118(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test018, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test018, text)
        want = test018
        cond = ['b', '2021-12-31']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_4119(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test019, defaultformat="csv")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test019, text)
        want = test019q
        cond = ['b', '2021-12-31.2334']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(want, back)
    def test_5103(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test003, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test003, text)
        want = test003
        cond = ['[', '', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5104(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test004, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        want = test004
        cond = ['[', ' {}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5105(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test005, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test005, text)
        want = test005
        cond = ['[', ' {"a": "x"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5106(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test006, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test006, text)
        want = test006
        cond = ['[', ' {"a": "x", "b": "y"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5107(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test007, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test007, text)
        want = test007
        cond = ['[', ' {"a": "x", "b": "y"},', ' {"b": "v"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5108(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test008, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test008, text)
        want = test008
        cond = ['[', ' {"a": "x"},', ' {"b": "v"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5109(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test009, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test009, text)
        want = test009
        cond = ['[', ' {},', ' {"b": "v"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5111(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test011, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test011, text)
        want = test011
        cond = ['[', ' {"b": null}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5112(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test012, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test012, text)
        want = test012
        cond = ['[', ' {"b": false}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5113(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test013, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test013, text)
        want = test013
        cond = ['[', ' {"b": true}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5114(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test014, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test014, text)
        want = test014
        cond = ['[', ' {"b": ""}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5115(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test015, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test015, text)
        want = test015
        cond = ['[', ' {"b": "5678"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5116(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test016, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test016, text)
        want = test016
        cond = ['[', ' {"b": 123}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5117(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test017, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test017, text)
        want = test017
        cond = ['[', ' {"b": 123.4}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5118(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test018, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test018, text)
        want = test018
        cond = ['[', ' {"b": "2021-12-31"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5119(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test019, defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test019, text)
        want = test019
        cond = ['[', ' {"b": "2021-12-31 23:34:45"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        self.assertEqual(want, back)
    def test_5143(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b', 'a'], defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['[', ' {"b": 2, "a": "x"},', ' {"b": 1, "a": "y"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        want = [{'a': 'x', 'b': 2}, {'a': 'y', 'b': 1}, ]
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_5144(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b@1', 'a'], defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['[', ' {"b": 1, "a": "y"},', ' {"b": 2, "a": "x"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        want = [{'a': 'y', 'b': 1}, {'a': 'x', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_5145(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}, {'c': 'h'}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b@1', 'a'], defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['[', ' {"b": 1, "a": "y"},', ' {"b": 2, "a": "x"},', ' {"c": "h"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        want = [{'a': 'y', 'b': 1}, {'a': 'x', 'b': 2}, {'c': "h"}, ]
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_5146(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}, {'c': 'h'}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['a@:2', 'b@:1'], defaultformat="json")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['[', ' {"a": "y", "b": 1},', ' {"a": "x", "b": 2},', ' {"c": "h"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        want = [{'a': 'y', 'b': 1}, {'a': 'x', 'b': 2}, {'c': "h"}, ]
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_5149(self) -> None:
        """ jsn is more compact that json """
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}, {'c': 'h'}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['a@:2', 'b@:1'], defaultformat="jsn")
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        # = ['[', ' {"a": "y", "b": 1},', ' {"a": "x", "b": 2},', ' {"c": "h"}', ']']
        cond = ['[', ' {"a":"y","b":1},', ' {"a":"x","b":2},', ' {"c":"h"}', ']']
        self.assertEqual(cond, text.splitlines())
        back = loadJSON(text)
        want = [{'a': 'y', 'b': 1}, {'a': 'x', 'b': 2}, {'c': "h"}, ]
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_5821(self) -> None:
        tmp = self.testdir()
        tablist = {"table01": table01, "table02": table02}
        filename = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 10)
        self.assertGreater(100, sz)
        want = {"table01": table01, "table02": table02}
        scan = tablistfile(filename)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_5822(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 100)
        self.assertGreater(600, sz)
        want = {"table22": table22, "table33": table33}
        scan = tablistfile(filename)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)

    def test_6103(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test003)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test003, text)
        want = JSONLIST
        cond = ['', '']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6104(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test004)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        want = JSONLIST
        cond = ['', '', '']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6105(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test005)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test005, text)
        want = test005
        cond = ['| a', '| -----', '| x']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6106(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test006)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test006, text)
        want = test006
        cond = ['| a     | b', '| ----- | -----', '| x     | y']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6107(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test007)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test007, text)
        want = test007Q
        cond = ['| a     | b', '| ----- | -----', '| x     | y', '| ~     | v']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6108(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test008)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test008, text)
        want = test008Q
        cond = ['| a     | b', '| ----- | -----', '| x     | ~', '| ~     | v']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6109(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test009)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test009, text)
        want = test009Q
        cond = ['| b', '| -----', '| ~', '| v']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6111(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test011)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test011, text)
        want = test011
        cond = ['| b', '| -----', '| ~']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6112(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test012)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test012, text)
        want = test012
        cond = ['| b', '| -----', '| (no)']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6113(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test013)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test013, text)
        want = test013
        cond = ['| b', '| -----', '| (yes)']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6114(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test014)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test014, text)
        want = test014
        cond = ['| b', '| -----', '|']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6115(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test015)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test015, text)
        want = test015Q
        cond = ['| b', '| -----', '| 5678']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6116(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test016)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test016, text)
        want = test016
        cond = ['| b', '| -----', '| 123']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6117(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test017)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test017, text)
        want = test017
        cond = ['| b', '| ------', '| 123.40']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6118(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test018)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test018, text)
        want = test018
        cond = ['| b', '| ----------', '| 2021-12-31']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6119(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, test019)  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test019, text)
        want = test019q
        cond = ['| b', '| ---------------', '| 2021-12-31.2334']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6144(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b@1', 'a'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['| b     | a', '| ----- | -----', '| 1     | y', '| 2     | x']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': 'y', 'b': 1}, {'a': 'x', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_6171(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b@1', 'a: {:}'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['| b     |     a', '| ----- | ----:', '| 1     |     y', '| 2     |     x']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': 'y', 'b': 1}, {'a': 'x', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_6172(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b@1', 'a: %s'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['| b     |     a', '| ----- | ----:', '| 1     |     y', '| 2     |     x']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': 'y', 'b': 1}, {'a': 'x', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_6173(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b:<.2n@1', 'a:"%s"'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['| b     | a', '| ----- | -----', '| 1     | "y"', '| 2     | "x"']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': '"y"', 'b': 1}, {'a': '"x"', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_6174(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2}, {'a': "y", 'b': 1}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b:{:.2f}@1', 'a:"{:}"'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['|     b | a', '| ----: | -----', '|  1.00 | "y"', '|  2.00 | "x"']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': '"y"', 'b': 1}, {'a': '"x"', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_6175(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2.}, {'a': "y", 'b': 1.}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b:{:<.2f}@1', 'a:"{:}"'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        # text = tabtotext.tabToGFM(itemlist, ['b', 'a'], formats)
        logg.debug("%s => %s", test004, text)
        cond = ['| b     | a', '| ----- | -----', '| 1.00  | "y"', '| 2.00  | "x"']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': '"y"', 'b': 1}, {'a': '"x"', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_6176(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2.}, {'a': "y", 'b': 1.}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b:{:.2f}@1', 'a:"{:}"'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['|     b | a', '| ----: | -----', '|  1.00 | "y"', '|  2.00 | "x"']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': '"y"', 'b': 1}, {'a': '"x"', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    @unittest.expectedFailure
    def test_6177(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2.}, {'a': "y", 'b': 1.}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b:{:$}@1', 'a:"{:}"'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['|     b | a', '| ----: | -----', X('| 1.00$ | "y"'), X('| 2.00$ | "x"')]
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': '"y"', 'b': 1}, {'a': '"x"', 'b': 2}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_6178(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 2.}, {'a': "y", 'b': 1.}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b:{:3f}@1', 'a:"{:5s}"'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['|        b | a', '| -------: | -------', '| 1.000000 | "y    "', '| 2.000000 | "x    "']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': '"y    "', 'b': 1.0}, {'a': '"x    "', 'b': 2.0}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)
    def test_6179(self) -> None:
        itemlist: JSONList = [{'a': "x", 'b': 22.}, {'a': "y", 'b': 1.}]
        out = StringIO()
        res = print_tabtotext(out, itemlist, ['b:{:>3f}@1', 'a:"{:>5s}"'])
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", test004, text)
        cond = ['|         b |       a', '| --------: | ------:', '|  1.000000 | "    y"', '| 22.000000 | "    x"']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        want = [{'a': '"    y"', 'b': 1.0}, {'a': '"    x"', 'b': 22.0}, ]  # order of rows swapped
        logg.info("%s => %s", want, back)
        self.assertEqual(want, back)

    def test_6801(self) -> None:
        data: JSONList = [{"a": "a b", "c": "c d|e"}, {"a": "g\nh", "c": "s\\t"}]
        text = tabtotext(data, defaultformat="md")
        logg.debug("%s => %s", data, text.splitlines())
        cond = ['| a     | c', '| ----- | -----', '| a b   | c d\\|e', '| g\\', 'h  | s\\\\t']
        self.assertEqual(cond, text.splitlines())
        # scan = tabtotext.tablistscanGFM(text)
        # back = dict(tabtotext.tablistmap(scan))
        back = loadGFM(text)
        want = data
        logg.debug("\n>> %s\n<< %s", data, back)
        self.assertEqual(want, back)
    def test_6803(self) -> None:
        data: JSONList = [{"a": "a b", "c": "c d|e"}, {"a": "g\nh", "c": "s\\t"}]
        tabs: Dict[str, JSONList] = {"data": data}
        buff = StringIO()
        done = print_tablist(buff, tablistfor(tabs), defaultformat="md")
        text = buff.getvalue()
        logg.debug("%s => %s", data, text.splitlines())
        cond = ['| a     | c', '| ----- | -----', '| a b   | c d\\|e', '| g\\', 'h  | s\\\\t']
        self.assertEqual(cond, text.splitlines())
        scan = tablistfile(StringIO(text))
        back = dict(tablistmap(scan))
        want = {"-1": data}
        logg.debug("\n>> %s\n<< %s", data, back)
        self.assertEqual(want, back)
    def test_6804(self) -> None:
        test = self.testdir()
        data: JSONList = [{"a": "a b", "c": "c d|e"}, {"a": "g\nh", "c": "s\\t"}]
        tabs: Dict[str, JSONList] = {"data": data}
        filename = F"{test}/tabs.md"
        done = print_tablist(filename, tablistfor(tabs), defaultformat="md")
        text = open(filename).read()
        logg.debug("%s => %s", data, text.splitlines())
        cond = ['| a     | c', '| ----- | -----', '| a b   | c d\\|e', '| g\\', 'h  | s\\\\t']
        self.assertEqual(cond, text.splitlines())
        scan = tablistfile(filename)
        back = dict(tablistmap(scan))
        want = {"-1": data}
        logg.debug("\n>> %s\n<< %s", data, back)
        self.assertEqual(want, back)
        self.rm_testdir()
    date_for_6220: JSONList = [{"a": "x", "b": 0}, {"b": 2}]
    def test_6220(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, self.date_for_6220, ["b", "a"])  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", res, text)
        want = self.date_for_6220
        cond = ['| b     | a', '| ----- | -----', '| 0     | x', '| 2     | ~']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        del back[1]["a"]
        self.assertEqual(want, back)
    date_for_6221: JSONList = [{"a": "x", "b": 3}, {"b": 2}]
    def test_6221(self) -> None:
        out = StringIO()
        res = print_tabtotext(out, self.date_for_6221, ["b@1", "a"])  # defaultformat="markdown"
        logg.info("print_tabtotext %s", res)
        text = out.getvalue()
        logg.debug("%s => %s", res, text)
        want = rev(self.date_for_6221)  # type: ignore[arg-type]
        cond = ['| b     | a', '| ----- | -----', '| 2     | ~', '| 3     | x']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        del back[0]["a"]
        self.assertEqual(want, back)
    def test_6821(self) -> None:
        tmp = self.testdir()
        tablist = {"table01": table01, "table02": table02}
        filename = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 50)
        self.assertGreater(200, sz)
        have = open(filename).read()
        logg.debug("have\n%s", have)
        want = {"table01": table01N, "table02": _date(table02N)}
        scan = tablistfile(filename)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_6822(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 40)
        self.assertGreater(600, sz)
        want = {"table22": table22, "table33": table33N}
        scan = tablistfile(filename)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_6970(self) -> None:
        text = tabtotext(table01, [], ["@wide"])
        logg.debug("%s => %s", table01, text)
        want = table01N
        cond = ['a     b', 'x y   ~', '~     1']
        self.assertEqual(cond, text.splitlines())
    def test_6971(self) -> None:
        text = tabtotext(table02, [], ["@wide"])
        logg.debug("%s => %s", table02, text)
        want = table02N
        cond = ['a     b', 'x     0', '~     2']
        self.assertEqual(cond, text.splitlines())
    def test_6972(self) -> None:
        text = tabtotext(table22, [], ["@wide"])
        logg.debug("%s => %s", table22, text)
        want = table22
        cond = ['a     b', 'x     3', 'y     2']
        self.assertEqual(cond, text.splitlines())
    def test_6973(self) -> None:
        text = tabtotext(table33, [], ["@wide"])
        logg.debug("%s => %s", table33, text)
        want = table33Q
        cond = ['a     b     c',
                'x     3     2021-12-31', 'y     2     2021-12-30',
                '~     ~     2021-12-31.2334']
        self.assertEqual(cond, text.splitlines())
    def test_6974(self) -> None:
        text = tabtotext(table44, [], ["@wide"])
        logg.debug("%s => %s", table44, text)
        want = table44N
        cond = ['a     b     c     d',
                'x     3     (yes) 0.40',
                'y     2     (no)  0.30',
                '~     ~     (yes) 0.20',
                'y     1     ~     0.10']
        self.assertEqual(cond, text.splitlines())
    def test_6975(self) -> None:
        text = tabtotext(table01, [], ["@read"])
        logg.debug("%s => %s", table01, text)
        want = table01N
        cond = [' x\\ y  ~', ' ~     1']
        self.assertEqual(cond, text.splitlines())
    def test_6976(self) -> None:
        data: JSONList = [{"a": "a b", "c": "c d e"}, {"a": "g\nh", "c": "s\\t"}]
        text = tabtotext(data, [], ["@read"])
        logg.debug("%s => %s", data, text)
        cond = [' a\\ b  c\\ d\\ e', ' g\\', 'h  s\\\\t']
        self.assertEqual(cond, text.splitlines())
        real = sh("{ echo ' a\\ b  c\\ d\\ e'; echo ' g\\'; echo 'h  s\\\\t'; } | while read a c e; do echo a=$a; echo c=$c; echo e=$e; done")
        logg.info("real\n%s", real)
        back = real.splitlines()
        want = ["a=a b", 'c=c d e', 'e=', 'a=gh', 'c=s\\t', 'e=']  # NOTE: bash-read swallows \n between gh ?
        self.assertEqual(want, back)
    def test_6980(self) -> None:
        text = tabtotext(table01, [], ["@text"])
        logg.debug("%s => %s", table01, text)
        want = table01N
        cond = ['|x y  |~', '|~    |1']
        self.assertEqual(cond, text.splitlines())
    def test_6981(self) -> None:
        text = tabtotext(table02, [], ["@text"])
        logg.debug("%s => %s", table02, text)
        want = table02N
        cond = ['|x    |0', '|~    |2']
        self.assertEqual(cond, text.splitlines())
    def test_6982(self) -> None:
        text = tabtotext(table22, [], ["@text"])
        logg.debug("%s => %s", table22, text)
        want = table22
        cond = ['|x    |3', '|y    |2']
        self.assertEqual(cond, text.splitlines())
    def test_6983(self) -> None:
        text = tabtotext(table33, [], ["@text"])
        logg.debug("%s => %s", table33, text)
        want = table33Q
        cond = ['|x    |3    |2021-12-31',
                '|y    |2    |2021-12-30',
                '|~    |~    |2021-12-31']
    def test_6984(self) -> None:
        text = tabtotext(table44, [], ["@text"])
        logg.debug("%s => %s", table44, text)
        want = table44N
        cond = ['|x    |3    |(yes)|0.40',
                '|y    |2    |(no) |0.30',
                '|~    |~    |(yes)|0.20',
                '|y    |1    |~    |0.10']
        self.assertEqual(cond, text.splitlines())
    def test_6990(self) -> None:
        text = tabtotext(table01, [], ["@txt"])
        logg.debug("%s => %s", table01, text)
        want = table01N
        cond = ['|a    |b', '|x y  |~', '|~    |1']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6991(self) -> None:
        text = tabtotext(table02, [], ["@txt"])
        logg.debug("%s => %s", table02, text)
        want = table02N
        cond = ['|a    |b', '|x    |0', '|~    |2']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6992(self) -> None:
        text = tabtotext(table22, [], ["@txt"])
        logg.debug("%s => %s", table22, text)
        want = table22
        cond = ['|a    |b', '|x    |3', '|y    |2']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6993(self) -> None:
        text = tabtotext(table33, [], ["@txt"])
        logg.debug("%s => %s", table33, text.splitlines())
        want = table33N
        cond = ['|x    |3    |2021-12-31',
                '|y    |2    |2021-12-30',
                '|~    |~    |2021-12-31']
        back = loadGFM(text)
        self.assertEqual(want, back)
    def test_6994(self) -> None:
        text = tabtotext(table44, [], ["@txt"])
        logg.debug("%s => %s", table44, text.splitlines())
        want = table44N
        cond = ['|a    |b    |c    |d',
                '|x    |3    |(yes)|0.40',
                '|y    |2    |(no) |0.30',
                '|~    |~    |(yes)|0.20',
                '|y    |1    |~    |0.10']
        self.assertEqual(cond, text.splitlines())
        back = loadGFM(text)
        self.assertEqual(want, back)

    def test_8011(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test011)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test011
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), back)
        self.rm_testdir()
    def test_8012(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test012)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test012
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8013(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test013)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test013
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8014(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test014)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test014
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8015(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test015)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test015
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8016(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test016)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test016
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8017(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test017)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test017
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8018(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test018)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test018Q
        back = readFromXLSX(filename)
        self.assertEqual(_date(want), back)
        self.rm_testdir()
    def test_8019(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test019)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = test019
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8023(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = table33Q
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8024(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table44.xlsx")
        tabtoXLSX(filename, table44)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(5000, sz)
        want = table44N
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(back))
        self.rm_testdir()
    def test_8031(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test011)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = test011
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), back)
        # self.rm_testdir()
    def test_8032(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test012)
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = test012
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        logg.info("data = %s", back)
        self.rm_testdir()
    def test_8033(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test013)
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = test013
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8034(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test014)
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = test014
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8035(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test015)
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = test015
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8036(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test016)
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = test016
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8037(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test017)
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = test017
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        self.rm_testdir()
    def test_8038(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test018)
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = test018Q
        back = readFromXLSX(filename)
        self.assertEqual(_date(want), back)
        self.rm_testdir()
    def test_8039(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "output.xlsx")
        tabtoXLSX(filename, test019)
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = test019
        back = readFromXLSX(filename)
        self.assertEqual(want, back)
        # self.rm_testdir()
    def test_8060(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "tabl01.xlsx")
        tabtoXLSX(filename, table01, ["b", "a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = table01N
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), back)
        self.rm_testdir()
    def test_8061(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "tabl02.xlsx")
        tabtoXLSX(filename, table02, ["b", "a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = table02N
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), back)
        self.rm_testdir()
    def test_8062(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "tabl22.xlsx")
        tabtoXLSX(filename, table22, ["b", "a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = table22
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), back)
        self.rm_testdir()
    def test_8063(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "tabl33.xlsx")
        tabtoXLSX(filename, table33, ["b", "a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = table33Q
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8064(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table44.xlsx")
        tabtoXLSX(filename, table44, ["b", "a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = table44N
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(back))
        self.rm_testdir()
    def test_8065(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33, ["c", "a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = table33Q
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8467(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table22.xlsx")
        tabtoXLSX(filename, table22, ["b", "a"], ["b", "a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = rev(table22)
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8468(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33, ["b", "a"], ["b", "a", "c"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = rev(table33Q[:2]) + table33Q[2:]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8469(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33, ["b", "a"], ["c", "a", "b"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = rev(table33Q[:2]) + table33Q[2:]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8470(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table01.xlsx")
        tabtoXLSX(filename, table01, ["b", "a"], ["a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'a': None}, {'a': 'x y'}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8471(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table02.xlsx")
        tabtoXLSX(filename, table02, ["b", "a"], ["a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'a': None}, {'a': 'x'}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8472(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table22.xlsx")
        tabtoXLSX(filename, table22, ["b", "a"], ["a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'a': 'x'}, {'a': 'y'}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8473(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33, ["b", "a"], ["a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'a': None}, {'a': 'x'}, {'a': 'y'}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8474(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33, ["c", "a"], ["a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'a': None}, {'a': 'x'}, {'a': 'y'}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8475(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table02.xlsx")
        tabtoXLSX(filename, table02, ["b", "a"], ["b"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'b': 0}, {'b': 2}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8476(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table22.xlsx")
        tabtoXLSX(filename, table22, ["b", "a"], ["b"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'b': 2}, {'b': 3}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8477(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33, ["b", "a"], ["b"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'b': 2}, {'b': 3}, {'b': None}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8478(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33, ["c", "a"], ["b"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'b': 2}, {'b': 3}, {'b': None}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8479(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33, ["c", "a"], ["c"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want: JSONList
        want = [{'c': Date(2021, 12, 30)}, {'c': Date(2021, 12, 31)}, {'c': Date(2021, 12, 31)}]
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8530(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table01.xlsx")
        tabtoXLSX(filename, table01, ["a|b"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = table01N
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8535(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table01.xlsx")
        tabtoXLSX(filename, table01, ["b|a"])
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        #
        with ZipFile(filename) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
                logg.info("xmldata = %s", xmldata)
        #
        want = table01N
        back = readFromXLSX(filename)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    def test_8821(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        want = {"table22": table22, "table33": _date(_none(table33Q))}
        scan = tablistfile(filename)
        back = dict(tablistmap(scan))
        if FIXME and "table33" in back:
            back["table33"] = _date(back["table33"])  # FIXME: openpyxl returns .999999 sec
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
# sh

    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9018(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table44.xlsx")
        tabtoXLSX(filename, table44)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} a b")
        logg.info("text = %s", text)
        cond = ['| a     | b', '| ----- | -----', '|       |',
                '| x     | 3', '| y     | 1', '| y     | 2']
        self.assertEqual(cond, text.splitlines())
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9019(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table44.xlsx")
        tabtoXLSX(filename, table44)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} a b:.2f")
        logg.info("text = %s", text)
        cond = ['| a     |     b', '| ----- | ----:', '|       |',
                '| x     |  3.00', '| y     |  1.00', '| y     |  2.00']
        self.assertEqual(cond, text.splitlines())
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9020(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table01.xlsx")
        tabtoXLSX(filename, table01)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} @csv")
        cond = ['a;b', 'x y;~', '~;1']
        cond = ['a;b', 'x y;', ';1']
        want = table01N
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(_none(want), back)
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9021(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table02.xlsx")
        tabtoXLSX(filename, table02)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} @csv")
        want = table02N
        cond = ['a;b', 'x;0', '~;2']
        cond = ['a;b', 'x;0', ';2']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(_none(want), back)
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9022(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table22.xlsx")
        tabtoXLSX(filename, table22)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} @csv")
        want = table22
        cond = ['a;b', 'x;3', 'y;2']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(_none(want), back)
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9023(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table33.xlsx")
        tabtoXLSX(filename, table33)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} @csv")
        want = table33Q
        cond = ['a;b;c', 'x;3;2021-12-31', 'y;2;2021-12-30', '~;~;2021-12-31']
        cond = ['a;b;c', 'x;3;2021-12-31', 'y;2;2021-12-30', ';;2021-12-31']
        cond = ['a;b;c', 'x;3;2021-12-31', 'y;2;2021-12-30', ';;2021-12-31.2334']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(_none(want), _none(_date(back)))
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9024(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table44.xlsx")
        tabtoXLSX(filename, table44)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} @csv")
        logg.info("text = %s", text)
        want = table44N
        cond = ['a;b;c;d', 'x;3;(yes);0.40', 'y;2;(no);0.30', ';;(yes);0.20', 'y;1;;0.10']
        self.assertEqual(cond, text.splitlines())
        back = loadCSV(text)
        self.assertEqual(_none(want), _none(back))
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9028(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table44.xlsx")
        tabtoXLSX(filename, table44)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} @csv a b")
        logg.info("text = %s", text)
        cond = ['a;b;c;d', 'x;3;(yes);0.40', 'y;2;(no);0.30', ';;(yes);0.20', 'y;1;;0.10']
        cond = ['a;b', ';', 'x;3', 'y;1', 'y;2']
        self.assertEqual(cond, text.splitlines())
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9029(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table44.xlsx")
        tabtoXLSX(filename, table44)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} @csv a b:.2f")
        logg.info("text = %s", text)
        cond = ['a;b;c;d', 'x;3;(yes);0.40', 'y;2;(no);0.30', ';;(yes);0.20', 'y;1;;0.10']
        cond = ['a;b', ';', 'x;3', 'y;1', 'y;2']
        cond = ['a;b', ';', 'x;3.00', 'y;1.00', 'y;2.00']
        self.assertEqual(cond, text.splitlines())
        self.rm_testdir()
    @unittest.skipIf(skipXLSX, "no openpyxl")
    def test_9039(self) -> None:
        tmp = self.testdir()
        filename = path.join(tmp, "table44.xlsx")
        tabtoXLSX(filename, table44)
        sz = path.getsize(filename)
        logg.info("generated [%s] %s", sz, filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} @csv a 'b:{{:.1f}}in@wide'")
        logg.info("text = %s", text)
        cond = ['a;b;c;d', 'x;3;(yes);0.40', 'y;2;(no);0.30', ';;(yes);0.20', 'y;1;;0.10']
        cond = ['a;b', ';', 'x;3', 'y;1', 'y;2']
        cond = ['a;b', ';', 'x;3.00', 'y;1.00', 'y;2.00']
        cond = ['a;wide', ';', 'x;3.0in', 'y;1.0in', 'y;2.0in']
        self.assertEqual(cond, text.splitlines())
        self.rm_testdir()
    def test_9810(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output}")
        have = sh(F"{TABTO} -^ {output} --onlypages")
        logg.info("pages => %s", have.splitlines())
        want = ['table22', 'table33']
        self.assertEqual(want, have.splitlines())
    def test_9811(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output}")
        with ZipFile(output) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
        logg.info("xmldata=>\n%s", xmldata)
        self.assertIn(b"</worksheet>", xmldata)
        want = {"table22": table22, "table33": _none(table33N)}
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9812(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -: table22")
        with ZipFile(output) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
        logg.info("xmldata=>\n%s", xmldata)
        self.assertIn(b"</worksheet>", xmldata)
        want = {"table22": table22, }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9813(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -: table33")
        with ZipFile(output) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
        logg.info("xmldata=>\n%s", xmldata)
        self.assertIn(b"</worksheet>", xmldata)
        want = {"table33": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9814(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2")
        with ZipFile(output) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
        logg.info("xmldata=>\n%s", xmldata)
        self.assertIn(b"</worksheet>", xmldata)
        want = {"data": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9815(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2 -: newdata")
        with ZipFile(output) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
        logg.info("xmldata=>\n%s", xmldata)
        self.assertIn(b"</worksheet>", xmldata)
        want = {"newdata": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9816(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2 -:newdata")
        with ZipFile(output) as zipped:
            with zipped.open("xl/worksheets/sheet1.xml") as zipdata:
                xmldata = zipdata.read()
        logg.info("xmldata=>\n%s", xmldata)
        self.assertIn(b"</worksheet>", xmldata)
        want = {"newdata": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9821(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename}")
        logg.info("=>\n%s", text)
        want = {"table22": table22, "table33": _none(table33N)}
        scan = cast(List[TabSheet], tablistscanGFM(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9822(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -: table22")
        logg.info("=>\n%s", text)
        want = {"table22": table22, }
        scan = cast(List[TabSheet], tablistscanGFM(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9823(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -: table33")
        logg.info("=>\n%s", text)
        want = {"table33": _none(table33N), }
        scan = cast(List[TabSheet], tablistscanGFM(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9824(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -2")
        logg.info("=>\n%s", text)
        want = {"-1": _none(table33N), }
        scan = cast(List[TabSheet], tablistscanGFM(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9825(self) -> None:
        tmp = self.testdir()
        tablist1 = {"table22": table22, "table33": table33}
        filename1 = path.join(tmp, "input1.xlsx")
        tablist2 = {"table01": table01, "table02": table02}
        filename2 = path.join(tmp, "input2.xlsx")
        inp1 = print_tablist(filename1, tablistfor(tablist1))
        inp2 = print_tablist(filename2, tablistfor(tablist2))
        text = sh(F"{TABTO} -^ -f {filename1} -f {filename2} -2")
        logg.info("=>\n%s", text)
        want = {"-1": _none(table33N), }
        scan = cast(List[TabSheet], tablistscanGFM(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        text = sh(F"{TABTO} -^ -f {filename1} -f {filename2} -3")
        logg.info("=>\n%s", text)
        want = {"-1": _none(table01N), }
        scan = cast(List[TabSheet], tablistscanGFM(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9830(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output}")
        have = sh(F"{TABTO} -^ {output} --onlypages")
        logg.info("pages => %s", have.splitlines())
        want = ['table22', 'table33']
        self.assertEqual(want, have.splitlines())
    def test_9831(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output}")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanGFM(text)
        want = {"table22": table22, "table33": _none(table33N)}
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9832(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -: table22")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanGFM(text)
        want = {"table22": table22, }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9833(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -: table33")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanGFM(text)
        want = {"table33": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9834(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanGFM(text)
        want = {"-1": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9835(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2 -: newdata")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanGFM(text)
        want = {"newdata": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9836(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.md")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2 :newdata")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanGFM(text)
        want = {"newdata": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9851(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename}  @json")
        logg.info("=>\n%s", text)
        want = {"table22": table22, "table33": _none(table33N)}
        scan = cast(List[TabSheet], tablistscanJSON(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9852(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -: table22  @json")
        logg.info("=>\n%s", text)
        want = {"table22": table22, }
        scan = cast(List[TabSheet], tablistscanJSON(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9853(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -: table33  @json")
        logg.info("=>\n%s", text)
        want = {"table33": _none(table33N), }
        scan = cast(List[TabSheet], tablistscanJSON(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9854(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "output.xlsx")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -2 @json")
        logg.info("=>\n%s", text)
        want = {"data": _none(table33N), }
        scan = cast(List[TabSheet], tablistscanJSON(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9855(self) -> None:
        tmp = self.testdir()
        tablist1 = {"table22": table22, "table33": table33}
        filename1 = path.join(tmp, "input1.xlsx")
        tablist2 = {"table01": table01, "table02": table02}
        filename2 = path.join(tmp, "input2.xlsx")
        inp1 = print_tablist(filename1, tablistfor(tablist1))
        inp2 = print_tablist(filename2, tablistfor(tablist2))
        text = sh(F"{TABTO} -^ -f {filename1} -f {filename2} -2 @json")
        logg.info("=>\n%s", text)
        want = {"data": _none(table33N), }
        scan = cast(List[TabSheet], tablistscanJSON(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        text = sh(F"{TABTO} -^ -f {filename1} -f {filename2} -3 @json")
        logg.info("=>\n%s", text)
        want = {"data": _none(table01N), }
        scan = cast(List[TabSheet], tablistscanJSON(text))
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
    def test_9860(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output}")
        have = sh(F"{TABTO} -^ {output} --onlypages")
        logg.info("pages => %s", have.splitlines())
        want = ['table22', 'table33']
        self.assertEqual(want, have.splitlines())
    def test_9861(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output}")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanJSON(text)
        want = {"table22": table22, "table33": _none(table33N)}
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9862(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename}  -o {output} -: table22")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanJSON(text)
        want = {"table22": table22, }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9863(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename}  -o {output} -: table33")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanJSON(text)
        want = {"table33": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9864(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanJSON(text)
        want = {"data": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9865(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2 -: newdata")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanJSON(text)
        want = {"newdata": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9866(self) -> None:
        tmp = self.testdir()
        tablist = {"table22": table22, "table33": table33}
        filename = path.join(tmp, "input.xlsx")
        output = path.join(tmp, "output.json")
        text = print_tablist(filename, tablistfor(tablist))
        sz = path.getsize(filename)
        self.assertGreater(sz, 3000)
        self.assertGreater(6000, sz)
        text = sh(F"{TABTO} -^ {filename} -o {output} -2 :newdata")
        text = open(output).read()
        logg.info("=>\n%s", text)
        test = tablistscanJSON(text)
        want = {"newdata": _none(table33N), }
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(want, back)
        self.assertEqual(test, scan)
    def test_9888(self) -> None:
        tmp = self.testdir()
        tabs: List[TabSheet] = []
        for sheet in range(5):
            rows: JSONList = []
            for row in range(BIGFILE // 10):
                num = sheet * BIGFILE + row
                vals: JSONDict = {"a": num, "b": BIGFILE + num}
                rows.append(vals)
            title = "data%i" % sheet
            tabs.append(TabSheet(rows, [], title))
        filename = path.join(tmp, "bigfile.xlsx")
        output = path.join(tmp, "bigfile.json")
        starting = Time.now()
        text = print_tablist(filename, tabs)
        generated = Time.now()
        text = sh(F"{TABTO} -^ {filename} -o {output}")
        converted = Time.now()
        logg.info("| %i numbers tabxlsx write xlsx time | %s", BIGFILE, generated - starting)
        logg.info("| %i numbers read xls and write json | %s", BIGFILE, converted - generated)
        text = open(output).read()
        # logg.debug("=>\n%s", text)
        test = tablistscanJSON(text)
        scan = tablistfile(output)
        back = dict(tablistmap(scan))
        # logg.debug("\n>> %s\n<< %s", want, back)
        self.assertEqual(test, scan)

if __name__ == "__main__":
    # unittest.main()
    from optparse import OptionParser
    cmdline = OptionParser("%s test...")
    cmdline.add_option("-v", "--verbose", action="count", default=0, help="more verbose logging")
    cmdline.add_option("-^", "--quiet", action="count", default=0, help="less verbose logging")
    cmdline.add_option("-k", "--keep", action="count", default=0, help="keep testdir")
    cmdline.add_option("--bigfile", metavar=str(BIGFILE), default=BIGFILE)
    cmdline.add_option("--failfast", action="store_true", default=False,
                       help="Stop the test run on the first error or failure. [%default]")
    cmdline.add_option("--xmlresults", metavar="FILE", default=None,
                       help="capture results as a junit xml file [%default]")
    opt, args = cmdline.parse_args()
    logging.basicConfig(level=max(0, logging.WARNING - 10 * opt.verbose + 10 * opt.quiet))
    BIGFILE = int(opt.bigfile)
    KEEP = opt.keep
    if not args:
        args = ["test_*"]
    suite = unittest.TestSuite()
    for arg in args:
        if len(arg) > 2 and arg[0].isalpha() and arg[1] == "_":
            arg = "test_" + arg[2:]
        for classname in sorted(globals()):
            if not classname.endswith("Test"):
                continue
            testclass = globals()[classname]
            for method in sorted(dir(testclass)):
                if "*" not in arg: arg += "*"
                if arg.startswith("_"): arg = arg[1:]
                if fnmatch(method, arg):
                    suite.addTest(testclass(method))
    # running
    xmlresults = None
    if opt.xmlresults:
        if os.path.exists(opt.xmlresults):
            os.remove(opt.xmlresults)
        xmlresults = open(opt.xmlresults, "wb")
    if xmlresults:
        import xmlrunner  # type: ignore[import]
        Runner = xmlrunner.XMLTestRunner
        result = Runner(xmlresults).run(suite)
        logg.info(" XML reports written to %s", opt.xmlresults)
    else:
        Runner = unittest.TextTestRunner
        result = Runner(verbosity=opt.verbose, failfast=opt.failfast).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

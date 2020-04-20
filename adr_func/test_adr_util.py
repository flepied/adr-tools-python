from datetime import date
from io import StringIO
import unittest
import sys

import adr_func.adr_util

_LAST = None


def input(fname, inplace):
    global _LAST
    _LAST = MockedInput(fname, inplace)
    return _LAST


def filelineno():
    return _LAST.filelineno()


def close():
    return _LAST.close()


class MockedInput:
    def __init__(self, fname, inplace):
        self.lines = [line + "\n" for line in FNAME2STR[fname].split("\n")]
        self.save_stdout = sys.stdout
        self.output = StringIO()
        sys.stdout = self.output

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        self.idx += 1
        if self.idx == len(self.lines):
            raise StopIteration
        return self.lines[self.idx - 1]

    def filelineno(self):
        return self.idx

    def close(self):
        sys.stdout = self.save_stdout


adr_func.adr_util.fileinput.input = input
adr_func.adr_util.fileinput.filelineno = filelineno
adr_func.adr_util.fileinput.close = close


class TestAdrUtils(unittest.TestCase):
    def test_adr_write_number_and_header(self):
        adr_func.adr_util.adr_write_number_and_header("0001-adr.md", 1, "ADR Choice")
        lines = _LAST.output.getvalue().split("\n")
        self.assertEqual(lines[0], "# 1. ADR Choice")
        self.assertEqual(lines[2], "* " + date.today().strftime("%Y-%m-%d"))


#     def test_adr_add_link(self):
#         adr_func.adr_util._adr_add_link('accepted', '0002-adr.md')
#         lines = _LAST.output.getvalue().split('\n')
#         self.assertEqual(lines[2], '* Status: ')


FNAME2STR = {
    "0001-adr.md": """# NUMBER. TITLE

* DATE
""",
    "0002-adr.md": """# NUMBER. TITLE

* Status: accepted
""",
}

if __name__ == "__main__":
    unittest.main()

# test_adr_utils.py ends here

# SPDX-License-Identifier: MIT
#
# Regression tests for tools/new_experiment.py, standard library only:
#
#   python -m unittest discover -s tests
#
# Each test builds a small research document set in a temporary directory from the
# unmodified templates, drives the tool the way a user would, and holds the result to
# the linter — the tool is only correct if lint_docs.py agrees with what it wrote.

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "tools", "new_experiment.py")
LINT = os.path.join(REPO, "tools", "lint_docs.py")
TEMPLATE = os.path.join(REPO, "templates", "experiments.md")

META = """# About these documents

Standard: https://github.com/Fast-and-Pythonic/ai-docs-method v2.2.0
"""

BACKLOG = """# Backlog

**Status legend:** `open`, `in progress`, `done`, `obsolete`, `dropped`

## Index

| id | status | task | phase |
|----|--------|------|-------|
| T-1 | open | First task | pilot |
| T-2 | open | Second task | pilot |

---

## T-1. First task

**Acceptance criterion:** p50 under 20 ms.

## T-2. Second task

**Acceptance criterion:** p50 under 10 ms.
"""


def comment_block(text):
    m = re.search(r"<!--.*?-->", text, re.DOTALL)
    return m.group(0) if m else None


class OpenExperiments(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.docs = os.path.join(self.tmp, "ai_docs")
        os.makedirs(os.path.join(self.docs, "plan"))
        shutil.copy(TEMPLATE, os.path.join(self.docs, "experiments.md"))
        for rel, body in (("_meta.md", META), ("plan/backlog.md", BACKLOG)):
            with open(os.path.join(self.docs, rel), "w", encoding="utf-8") as f:
                f.write(body)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def open_entry(self, task, title):
        r = subprocess.run(
            [sys.executable, TOOL, "--docs", self.docs, "--task", task,
             "--title", title, "--hypothesis", "h", "--predict", "p",
             "--date", "2026-01-01"],
            capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def experiments(self):
        with open(os.path.join(self.docs, "experiments.md"), encoding="utf-8") as f:
            return f.read()

    def test_second_index_line_lands_under_index_not_in_comment(self):
        # The template keeps example index lines in a comment below the real index. The
        # second entry used to be indexed after the last of those — inside the comment.
        self.open_entry("T-1", "A")
        self.open_entry("T-2", "B")
        text = self.experiments()

        index = text.split("## Index", 1)[1].split("<!--", 1)[0]
        self.assertEqual(re.findall(r"^- \*\*(E\d+)\*\*", index, re.MULTILINE),
                         ["E01", "E02"], text)
        with open(TEMPLATE, encoding="utf-8") as f:
            self.assertEqual(comment_block(text), comment_block(f.read()))
        outside = text.replace(comment_block(text), "")
        self.assertEqual(re.findall(r"^## (E\d+)\.", outside, re.MULTILINE),
                         ["E01", "E02"])

        r = subprocess.run(
            [sys.executable, LINT, "--docs", self.docs, "--profile", "research"],
            capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("\n0 error(s)", r.stdout)


if __name__ == "__main__":
    unittest.main()

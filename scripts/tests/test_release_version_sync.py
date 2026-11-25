"""Check that every pin Release Please bumps is marked and matches STANDARDS_VERSION."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
MARKER = "x-release-please-version"
SEMVER = re.compile(r"\d+\.\d+\.\d+")
# A missing marker leaves a pin behind on the next release, so the expected count is fixed.
EXPECTED = {
    "README.md": 1,
    "docs/migration-guide.md": 2,
    "docs/reusable-workflows.md": 3,
    "template/.github/workflows/{% if reusable_lint %}lint.yml{% endif %}.jinja": 1,
}


class VersionSyncTests(unittest.TestCase):
    def test_marked_pins_match_standards_version(self):
        version = (ROOT / "STANDARDS_VERSION").read_text().strip()
        self.assertRegex(version, rf"^{SEMVER.pattern}$")
        for path, count in EXPECTED.items():
            marked = [line for line in (ROOT / path).read_text().splitlines() if MARKER in line]
            self.assertEqual(len(marked), count, path)
            for line in marked:
                # The Generic updater rewrites the first SemVer of a marked line.
                self.assertEqual(SEMVER.search(line).group(), version, f"{path}: {line}")

    def test_current_version_lines_are_all_marked(self):
        version = (ROOT / "STANDARDS_VERSION").read_text().strip()
        for path in EXPECTED:
            for line in (ROOT / path).read_text().splitlines():
                if f"v{version}" in line:
                    self.assertIn(MARKER, line, f"{path}: {line}")


if __name__ == "__main__":
    unittest.main()

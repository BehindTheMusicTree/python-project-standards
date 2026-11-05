"""Exercise release preparation in disposable Git repositories without publishing."""

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[2]


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        for name in (
            "standards_release_bump.sh",
            "finalize_standards_changelog.py",
            "publish_github_release.py",
        ):
            shutil.copyfile(SOURCE / "scripts" / name, self.root / "scripts" / name)
        (self.root / "STANDARDS_VERSION").write_text("1.0.0\n")
        (self.root / ".bumpversion.toml").write_text(
            '[tool.bumpversion]\ncurrent_version = "1.0.0"\n'
        )
        self.notes = "# Changelog\n\n## [Unreleased]\n\n### Changed\n\n- Useful change.\n\n## [1.0.0]\n\n- Previous.\n"
        (self.root / "CHANGELOG.md").write_text(self.notes)
        self.git("init", "-q", "-b", "feature/release-test")
        self.git("config", "user.email", "fixture@example.test")
        self.git("config", "user.name", "Fixture")
        self.commit()
        binary = self.root / ".git" / "bin"
        binary.mkdir()
        uv = binary / "uv"
        uv.write_text("""#!/usr/bin/env python3
import pathlib, sys
pathlib.Path('.git/bump-called').touch()
if '--dry-run' not in sys.argv:
    pathlib.Path('STANDARDS_VERSION').write_text('1.0.1\\n')
    pathlib.Path('.bumpversion.toml').write_text('[tool.bumpversion]\\ncurrent_version = "1.0.1"\\n')
""")
        uv.chmod(0o755)
        self.env = dict(os.environ, PATH=str(binary) + os.pathsep + os.environ["PATH"])

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def run_script(self, *args, success=True):
        result = subprocess.run(
            ["bash", "scripts/standards_release_bump.sh", "patch", *args],
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_dry_run_does_not_change_files_or_commit(self):
        before = self.git("rev-parse", "HEAD")
        self.run_script("--dry-run", "--commit")
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(self.git("rev-parse", "HEAD"), before)
        self.assertEqual((self.root / "CHANGELOG.md").read_text(), self.notes)

    def test_preparation_updates_notes_without_creating_tag(self):
        self.run_script("--commit")
        self.assertEqual((self.root / "STANDARDS_VERSION").read_text(), "1.0.1\n")
        self.assertIn("## [1.0.1]", (self.root / "CHANGELOG.md").read_text())
        self.assertEqual(self.git("tag"), "")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_preparation_updates_changelog_navigation(self):
        notes = self.notes.replace(
            "## [Unreleased]",
            "## Table of Contents\n\n- [Unreleased](#unreleased)\n\n## [Unreleased]",
            1,
        )
        (self.root / "CHANGELOG.md").write_text(notes)
        self.commit()
        self.run_script()
        output = (self.root / "CHANGELOG.md").read_text()
        self.assertRegex(output, r"- \[1\.0\.1 - [0-9-]+\]\(#101---[0-9-]+\)")

    def test_protected_branch_and_detached_head_fail_before_bump(self):
        for branch in ("main", "develop"):
            self.git("checkout", "-qb", branch)
            self.run_script(success=False)
        self.git("checkout", "--detach", "-q")
        self.run_script(success=False)
        self.assertFalse((self.root / ".git/bump-called").exists())

    def test_empty_notes_fail_before_bump(self):
        (self.root / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n### Changed\n\n<!-- draft -->\n\n## [1.0.0]\n"
        )
        self.commit()
        self.run_script(success=False)
        self.assertFalse((self.root / ".git/bump-called").exists())

    def test_dirty_tree_and_overrides_fail_before_bump(self):
        for option in ("--tag", "--config-file=other.toml", "--allow-dirty"):
            self.run_script(option, success=False)
        (self.root / "untracked").touch()
        self.run_script(success=False)
        self.assertFalse((self.root / ".git/bump-called").exists())

    def test_local_publication_refuses_policy_before_credentials(self):
        (self.root / ".github").mkdir()
        (self.root / ".github/release-policy.json").write_text("{}")
        result = subprocess.run(
            ["python3", "scripts/publish_github_release.py"],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Publication is owned by CI", result.stderr)


if __name__ == "__main__":
    unittest.main()

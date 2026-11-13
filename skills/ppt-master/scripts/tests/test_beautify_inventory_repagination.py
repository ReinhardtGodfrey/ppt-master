#!/usr/bin/env python3
"""Verify Beautify text fidelity when an explicit overview-slide-zoom request re-paginated the deck.

Usage:
    python3 -m unittest tests.test_beautify_inventory_repagination

Dependencies:
    python-pptx and the script runtime dependencies.
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

from pptx import Presentation
from pptx.util import Inches

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import beautify_inventory  # noqa: E402
import pptx_intake  # noqa: E402


def _add_text_slide(presentation: Presentation, text: str) -> None:
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(2))
    box.text_frame.text = text


class BeautifyInventoryRepaginationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "source.pptx"
        presentation = Presentation()
        _add_text_slide(presentation, "ALPHA_ON_SLIDE_ONE")
        _add_text_slide(presentation, "BETA_ON_SLIDE_TWO")
        presentation.save(self.source)

    def _inventory(self) -> Path:
        analysis = self.root / "analysis"
        inventory = analysis / "beautify_inventory.json"
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(pptx_intake.main([str(self.source), "-o", str(analysis)]), 0)
            self.assertEqual(beautify_inventory.main([
                str(analysis / "source.slide_library.json"), "-o", str(inventory),
            ]), 0)
        return inventory

    def _deck(self, pages: list[str]) -> Path:
        presentation = Presentation()
        for text in pages:
            _add_text_slide(presentation, text)
        path = self.root / "export.pptx"
        presentation.save(path)
        return path

    def _verify(self, inventory: Path, deck: Path, *extra: str) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = beautify_inventory.main([str(inventory), "--verify", str(deck), *extra])
        return code, output.getvalue()

    def test_strict_mode_still_fails_after_repagination(self) -> None:
        inventory = self._inventory()
        deck = self._deck(["OVERVIEW_HUB", "ALPHA_ON_SLIDE_ONE", "BETA_ON_SLIDE_TWO"])
        code, output = self._verify(inventory, deck)
        self.assertEqual(code, 1)
        self.assertIn("pages do not match", output)

    def test_frozen_strings_may_move_pages_with_repagination_allowed(self) -> None:
        inventory = self._inventory()
        deck = self._deck(["OVERVIEW_HUB", "ALPHA_ON_SLIDE_ONE", "BETA_ON_SLIDE_TWO"])
        code, output = self._verify(inventory, deck, "--allow-repagination")
        self.assertEqual(code, 0)
        self.assertIn("repagination allowed", output)
        self.assertIn("placed on page(s) 2", output)
        self.assertIn("authored page(s) with no frozen string: [1]", output)
        self.assertIn("hub/card text is expected", output)

    def test_repagination_mode_fails_when_a_frozen_string_is_gone(self) -> None:
        inventory = self._inventory()
        deck = self._deck(["OVERVIEW_HUB", "ALPHA_ON_SLIDE_ONE"])
        code, output = self._verify(inventory, deck, "--allow-repagination")
        self.assertEqual(code, 1)
        self.assertIn("BETA_ON_SLIDE_TWO", output)
        self.assertIn("FAILED: frozen strings are missing from the export", output)

    def test_allow_repagination_requires_verify(self) -> None:
        inventory = self._inventory()
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            beautify_inventory.main([str(inventory), "--summary", "--allow-repagination"])


if __name__ == "__main__":
    unittest.main()

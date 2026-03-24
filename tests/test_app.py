import os
import unittest

from streamlit.testing.v1 import AppTest


class RoyalHumanizeAppTests(unittest.TestCase):
    def setUp(self):
        self._original_gemini = os.environ.pop("GEMINI_API_KEY", None)
        self._original_sapling = os.environ.pop("SAPLING_API_KEY", None)

    def tearDown(self):
        if self._original_gemini is not None:
            os.environ["GEMINI_API_KEY"] = self._original_gemini
        if self._original_sapling is not None:
            os.environ["SAPLING_API_KEY"] = self._original_sapling

    def test_app_renders_without_secrets_file(self):
        app = AppTest.from_file("main.py")
        app.run()

        self.assertFalse(app.exception)
        self.assertEqual(app.radio[0].value, "Humanizer")
        self.assertEqual(len(app.text_input), 2)
        self.assertGreaterEqual(len(app.text_area), 1)
        self.assertFalse(any(block.value.strip() == '<div class="glass-card">' for block in app.markdown))

    def test_quick_clean_generates_refined_output(self):
        app = AppTest.from_file("main.py")
        app.run()

        app.text_area[0].input("It is important to note that teams utilize AI in order to move faster.")
        app.button[1].click()
        app.run()

        self.assertTrue(any("teams use AI to move faster." in block.value for block in app.markdown))

    def test_detector_reports_missing_api_key_cleanly(self):
        app = AppTest.from_file("main.py")
        app.run()

        app.radio[0].set_value("AI Detector")
        app.run()
        app.text_area[0].input("This is a test passage for detection.")
        app.button[0].click()
        app.run()

        self.assertEqual(app.subheader[0].value, "API key needed")
        self.assertTrue(any("Sapling API key" in cap.value for cap in app.caption))


if __name__ == "__main__":
    unittest.main()

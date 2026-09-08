import unittest
from summary import summarize
class SummaryTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(summarize([" Beta ", "ALPHA", "beta", "", "  "]), {"names": ["beta", "alpha"], "counts": {"beta": 2, "alpha": 1}})
    def test_empty(self):
        self.assertEqual(summarize([]), {"names": [], "counts": {}})
    def test_input_preserved(self):
        items = [" B ", "a", "b"]
        original = items[:]
        summarize(items)
        self.assertEqual(items, original)
if __name__ == "__main__": unittest.main()

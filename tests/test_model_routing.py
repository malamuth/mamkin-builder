import unittest

from scripts.select_model_profile import load_config, select_profile, DEFAULT_CONFIG


class ModelRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(DEFAULT_CONFIG)

    def test_economy_requires_bounded_mechanical_read_only_work(self):
        result = select_profile(
            self.config,
            "read-only",
            ["bounded", "mechanical", "deterministic-validation"],
        )
        self.assertEqual(result["selectedProfile"], "economy")
        self.assertEqual(result["agentPreset"], "mamkin-economy-read")
        self.assertEqual(result["model"], "gpt-5.6-terra")
        self.assertEqual(result["reasoningEffort"], "medium")

    def test_workspace_write_defaults_to_balanced(self):
        result = select_profile(
            self.config,
            "workspace-write",
            ["bounded", "mechanical", "deterministic-validation"],
        )
        self.assertEqual(result["selectedProfile"], "balanced")
        self.assertEqual(result["agentPreset"], "mamkin-balanced-write")

    def test_deep_signal_establishes_floor(self):
        result = select_profile(self.config, "read-only", ["unknown-root-cause"])
        self.assertEqual(result["riskFloor"], "deep")
        self.assertEqual(result["reasoningEffort"], "high")

    def test_critical_signal_outranks_deep_signal(self):
        result = select_profile(
            self.config,
            "workspace-write",
            ["cross-component", "destructive-migration"],
        )
        self.assertEqual(result["riskFloor"], "critical")
        self.assertEqual(result["agentPreset"], "mamkin-critical-write")

    def test_requested_profile_may_raise_floor(self):
        result = select_profile(
            self.config,
            "read-only",
            ["bounded", "mechanical", "deterministic-validation"],
            "deep",
        )
        self.assertEqual(result["riskFloor"], "economy")
        self.assertEqual(result["selectedProfile"], "deep")

    def test_requested_profile_cannot_lower_floor(self):
        with self.assertRaisesRegex(ValueError, "below risk floor critical"):
            select_profile(
                self.config,
                "read-only",
                ["security-boundary"],
                "balanced",
            )

    def test_unknown_signal_is_blocked(self):
        with self.assertRaisesRegex(ValueError, "unknown signals"):
            select_profile(self.config, "read-only", ["looks-hard"])


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

from src.cli import parse_arguments


class TestCLI(unittest.TestCase):
    @patch("sys.argv", ["script.py", "user_prompt"])
    def test_parse_arguments_no_model(self):
        args = parse_arguments()
        self.assertEqual(args.user_prompt, "user_prompt")
        self.assertIsNone(args.model)

    @patch("sys.argv", ["script.py", "user_prompt", "-m", "model_name"])
    def test_parse_arguments_with_model(self):
        args = parse_arguments()
        self.assertEqual(args.user_prompt, "user_prompt")
        self.assertEqual(args.model, "model_name")


if __name__ == "__main__":
    unittest.main()

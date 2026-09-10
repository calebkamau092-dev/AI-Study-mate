import unittest

from utilities.validators import validate_subject


class ValidateSubjectTests(unittest.TestCase):
    def test_accepts_python(self):
        self.assertEqual(validate_subject("Python"), (True, "Python"))

    def test_normalizes_case_and_whitespace(self):
        self.assertEqual(validate_subject("  pYtHoN  "), (True, "Python"))

    def test_rejects_other_subjects(self):
        valid, message = validate_subject("Java")

        self.assertFalse(valid)
        self.assertEqual(message, "Only Python is supported as a study subject.")

    def test_rejects_empty_subject(self):
        valid, message = validate_subject("   ")

        self.assertFalse(valid)
        self.assertEqual(message, "Only Python is supported as a study subject.")


if __name__ == "__main__":
    unittest.main()
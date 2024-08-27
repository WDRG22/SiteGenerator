import unittest
from generate_page import *

class TestTextNode(unittest.TestCase):
    def test_extract_title(self):
        markdown = (
                "# This is an h1 title\n\n"
                "## This is an h2 heading\n\n"
                "* This is a list item\n"
                "* This is a second list item"
                )

        test_result = extract_title(markdown)
        expected_result = "This is an h1 title"
        self.assertEqual(test_result, expected_result)
    
    def test_extract_title_no_heading(self):
        markdown_no_heading = (
                "* This is a list item\n"
                "* This is a second list item"
                )
        with self.assertRaises(ValueError):
            extract_title(markdown_no_heading)



if __name__ == "__main__":
    unittest.main()

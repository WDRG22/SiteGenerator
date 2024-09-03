import unittest
import tempfile
import shutil
from generate_page import *

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_generate_page_recursive(self):
        # Create test directory structure
        markdown_dir = os.path.join(self.test_dir, "markdown")
        os.makedirs(markdown_dir)
        
        # Create markdown files
        markdown_file1 = os.path.join(markdown_dir, "file1.md")
        markdown_file2 = os.path.join(markdown_dir, "file2.md")
        with open(markdown_file1, 'w') as f:
            f.write("# Title 1\n\nContent 1")
        with open(markdown_file2, 'w') as f:
            f.write("# Title 2\n\nContent 2")

        # Create a subdirectory
        subdirectory = os.path.join(markdown_dir, "subdir")
        os.makedirs(subdirectory)

        # Create a markdown file in the subdirectory
        markdown_file3 = os.path.join(subdirectory, "file3.md")
        with open(markdown_file3, 'w') as f:
            f.write("# Title 3\n\nContent 3")

        # Generate HTML pages
        template_path = os.path.join(project_root, "template.html")
        output_dir = os.path.join(self.test_dir, "output")
        generate_page_recursive(markdown_dir, template_path, output_dir)

        # Check if HTML files were generated
        html_file1 = os.path.join(output_dir, "file1.html")
        html_file2 = os.path.join(output_dir, "file2.html")
        html_file3 = os.path.join(output_dir, "subdir", "file3.html")
        self.assertTrue(os.path.exists(html_file1))
        self.assertTrue(os.path.exists(html_file2))
        self.assertTrue(os.path.exists(html_file3))

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

import unittest
from textnode import TextNode
from inline_markdownparser import *
from block_markdownparser import *

class TestBlockMarkdownParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = (
                "# This is a heading\n\n"
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
                "* This is the first list item in a list block\n"
                "* This is a list item\n"
                "* This is another list item"
                )

        test_result = markdown_to_blocks(markdown)
        expected_result = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                ]
        self.assertEqual(test_result, expected_result)

    def test_block_to_block_type(self):
        block_paragraph = (
                "This is a simple paragraph. "
                "It contains multiple sentences and can span multiple lines. "
                "There's no special formatting at the start of the lines."
                )
        block_heading = "## This is a Level 2 Heading"
        block_code = (
                "```\n"
                "def hello_world():\n"
                "    print(\"Hello, World!\")\n"
                "    hello_world()\n"
                "```"
            )
        block_quote = (
                "> This is a quote block.\n"
                "> It can span multiple lines.\n"
                "> Each line starts with a '>' character."
                )
        block_unordered_list = (
                "* First item in an unordered list\n"
                "* Second item\n"
                "- Third item (using a dash instead of asterisk)\n"
                "* Fourth item"
                )
        block_ordered_list = (
                "1. First item in an ordered list\n"
                "2. Second item\n"
                "3. Third item\n"
                "4. Fourth item")


                # Test paragraph block
        test_result_paragraph = block_to_block_type(block_paragraph)
        expected_result_paragraph = "paragraph"
        self.assertEqual(test_result_paragraph, expected_result_paragraph)

        # Test heading block
        test_result_heading = block_to_block_type(block_heading)
        expected_result_heading = "heading"
        self.assertEqual(test_result_heading, expected_result_heading)

        # Test code block
        test_result_code = block_to_block_type(block_code)
        expected_result_code = "code"
        self.assertEqual(test_result_code, expected_result_code)

        # Test quote block
        test_result_quote = block_to_block_type(block_quote)
        expected_result_quote = "quote"
        self.assertEqual(test_result_quote, expected_result_quote)

        # Test unordered list block
        test_result_unordered_list = block_to_block_type(block_unordered_list)
        expected_result_unordered_list = "unordered_list"
        self.assertEqual(test_result_unordered_list, expected_result_unordered_list)

        # Test ordered list block
        test_result_ordered_list = block_to_block_type(block_ordered_list)
        expected_result_ordered_list = "ordered_list"
        self.assertEqual(test_result_ordered_list, expected_result_ordered_list)

    def test_markdown_to_html_node(self):
        markdown = (
				"# Welcome to My Page\n\n"
		        "This is a paragraph with some **bold** and *italic* text.\n\n"
				"## A List of Items\n\n"
				"* First item\n"
				"* Second item\n"
				"* Third item\n\n"
				"Here's some code:\n\n"
				"```python\n"
				"def hello_world():\n"
				"    print(\"Hello, World!\")```\n\n"
				">This is a blockquote.\n"
				">It can span multiple lines.\n\n\n"
				"1. First ordered item\n"
				"2. Second ordered item\n"
				"3. Third ordered item\n"
				)

        expected_result = (
			ParentNode(tag="div",
				children=[
		 			'<h1> Welcome to My Page</h1>',
					'<p>This is a paragraph with some <b>bold</b> and <i>italic</i> text.</p>',
					'<h2> A List of Items</h2>',
				ParentNode(tag="ul",
					children=[
						'<li>First item</li>',
						'<li>Second item</li>',
						'<li>Third item</li>',
					],
				),
					"<p>Here's some code:</p>",
					ParentNode(tag="pre",
						children=[
							'<code>python</code>',
							'<code>def hello_world():</code>',
							'<code>    print("Hello, World!")</code>',
						],
					),
					ParentNode(tag="blockquote",
						children=[
							'<p>This is a blockquote.</p>',
							'<p>It can span multiple lines.</p>',
						],
					),
					ParentNode(tag="ol",
						children=[
							'<li>First ordered item</li>',
							'<li>Second ordered item</li>',
							'<li>Third ordered item</li>',
						],
					),
				],
			)
		)
        test_result = markdown_to_html_node(markdown)
        self.assertEqual(test_result, expected_result)

import unittest
from textnode import *
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_node_to_html_node(self):
        # Test for bold
        boldNode = TextNode("This is a text node", "bold")
        boldHtmlNode = LeafNode(tag="b", value="This is a text node")
        self.assertEqual(text_node_to_html_node(boldNode), boldHtmlNode)

        # Test for italic
        italicNode = TextNode("This is italic", "italic")
        italicHtmlNode = LeafNode(tag="i", value="This is italic")
        self.assertEqual(text_node_to_html_node(italicNode), italicHtmlNode)

        # Test for code
        codeNode = TextNode("print('Hello')", "code")
        codeHtmlNode = LeafNode(tag="i", value="print('Hello')")
        self.assertEqual(text_node_to_html_node(codeNode), codeHtmlNode)

        # Test for link
        linkNode = TextNode("Click here", "link", "https://example.com")
        linkHtmlNode = LeafNode(tag="a", value="Click here", props={"href": "https://example.com"})
        self.assertEqual(text_node_to_html_node(linkNode), linkHtmlNode)

        # Test for image
        imageNode = TextNode("An example image", "image", "https://example.com/image.jpg")
        imageHtmlNode = LeafNode(tag="img", value="", props={"src": "https://example.com/image.jpg", "alt": "An example image"})
        self.assertEqual(text_node_to_html_node(imageNode), imageHtmlNode)

        # Test for plain text
        textNode = TextNode("Just plain text", "text")
        textHtmlNode = LeafNode(value="Just plain text")
        self.assertEqual(text_node_to_html_node(textNode), textHtmlNode)

        # Test for invalid text type
        invalidNode = TextNode("Invalid", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(invalidNode)


if __name__ == "__main__":
    unittest.main()

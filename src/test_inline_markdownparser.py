import unittest
from textnode import TextNode
from inline_markdownparser import *

class TestInlineMarkdownParser(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is an *example*", text_type="text")
        node2 = TextNode("Let's see if it *works* correctly", text_type="text")
        
        test_result = split_nodes_delimiter([node, node2], '*', "bold")
        expected_result = [
                            TextNode("This is an ", text_type="text"),
                            TextNode("example", text_type="bold"),
                            TextNode("Let's see if it ", text_type="text"),
                            TextNode("works", text_type="bold"),
                            TextNode(" correctly", text_type="text")
        ]
        self.assertEqual(test_result, expected_result)



    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        test_result = extract_markdown_images(text)
        self.assertEqual(test_result, expected_result)


    def test_extract_markdown_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        test_result = extract_markdown_links(text)
        self.assertEqual(test_result, expected_result)

    def test_split_nodes_image(self):
        node1 = TextNode("Here is an image ![alt text](http://image.url) with text.", "text")
        node2 = TextNode("Here is another image ![alt text 2](http://image2.url)", "text")
        nodes = [node1, node2]

        test_result = split_nodes_image(nodes)
        expected_result = [ 
                # For node1
                TextNode("Here is an image ", "text"),
                TextNode("alt text", "image", "http://image.url"),
                TextNode(" with text.", "text"),
                # For node2
                TextNode("Here is another image ", "text"),
                TextNode("alt text 2", "image", "http://image2.url"),
        ]
        self.assertEqual(test_result, expected_result)

    def test_split_nodes_link(self):
        node1 = TextNode("Here is a link [to something](http://link.url) with text.", "text")
        node2 = TextNode("Here is another link [to something else](http://link2.url)", "text")
        nodes = [node1, node2]

        test_result = split_nodes_link(nodes)
        expected_result = [ 
                # For node1
                TextNode("Here is a link ", "text"),
                TextNode("to something", "link", "http://link.url"),
                TextNode(" with text.", "text"),
                # For node2
                TextNode("Here is another link ", "text"),
                TextNode("to something else", "link", "http://link2.url"),
        ]
        self.assertEqual(test_result, expected_result)


    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        test_result = text_to_textnodes(text)
        expected_result = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(test_result, expected_result)


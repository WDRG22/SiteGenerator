import unittest
from textnode import TextNode
import markdownparser

class TestMarkdownParser(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is an *example*", text_type="text")
        node2 = TextNode("Let's see if it *works* correctly", text_type="text")
        
        test_result = markdownparser.split_nodes_delimiter([node, node2], '*', "bold")
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
        test_result = markdownparser.extract_markdown_images(text)
        self.assertEqual(test_result, expected_result)


    def test_extract_markdown_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        test_result = markdownparser.extract_markdown_links(text)
        self.assertEqual(test_result, expected_result)

    def test_split_nodes_image(self):
        node1 = TextNode("Here is an image ![alt text](http://image.url) with text.", "text")
        node2 = TextNode("Here is another image ![alt text 2](http://image2.url)", "text")
        nodes = [node1, node2]

        test_result = markdownparser.split_nodes_image(nodes)
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

        test_result = markdownparser.split_nodes_link(nodes)
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

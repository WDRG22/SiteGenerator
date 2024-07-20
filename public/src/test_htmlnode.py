import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        hNode = HTMLNode("<p>", "test value", children=[7,8,9], props=[1,2,3])
        hNode2 = HTMLNode("<p>", "test value", children=[7,8,9], props=[1,2,3])
        self.assertEqual(hNode, hNode2)

    def test_props(self):        
        props = {
                    "href": "www.google.com",
                    "target": "_blank"
                }
        html = " href=\"www.google.com\" target=\"_blank\""
        hNode = HTMLNode(props=props)
        self.assertEqual(hNode.props_to_html(), html)

if __name__ == "__main__":
    unittest.main()

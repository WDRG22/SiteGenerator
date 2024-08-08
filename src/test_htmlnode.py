import unittest

from htmlnode import *

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

    def test_leaf_node_eq(self):
        leafNode = LeafNode("p", value="Example paragraph", props={"href":"www.google.com", "alt":"alternative"})
        leafNode2 = LeafNode("p", value="Example paragraph", props={"href":"www.google.com", "alt":"alternative"})
        self.assertEqual(leafNode, leafNode2)

    def test_leaf_node_to_html(self):
        leafNode = LeafNode("p", value="Example paragraph", props={"href":"www.google.com", "alt":"alternative"})
        html = "<p href=\"www.google.com\" alt=\"alternative\">Example paragraph</p>"
        self.assertEqual(leafNode.to_html(), html)

    def test_parent_node_to_html(self):
        children = []
        for i in range(3):
            sub_children = []

            for j in range(3):
                sub_children.append(LeafNode("p", f"leaf node {i*j}", props={"loop":f"{i, j}"}))
                
            children.append(ParentNode("p", children=sub_children, props={"loop":f"{i, j}"}))
            children.append(LeafNode("p", f"leaf node {i}", props={"loop":f"{i, j}"}))

        parentNode = ParentNode("h1", children=children, props={"href":"www.google.com", "alt":"alternative"})
        test_result = parentNode.to_html()
        expected_result = (
			'<h1 href="www.google.com" alt="alternative">'
	        '<p loop="(0, 2)">'
    	    '<p loop="(0, 0)">leaf node 0</p>'
        	'<p loop="(0, 1)">leaf node 0</p>'
	        '<p loop="(0, 2)">leaf node 0</p>'
	        '</p>'
	        '<p loop="(0, 2)">leaf node 0</p>'
	        '<p loop="(1, 2)">'
	        '<p loop="(1, 0)">leaf node 0</p>'
	        '<p loop="(1, 1)">leaf node 1</p>'
	        '<p loop="(1, 2)">leaf node 2</p>'
	        '</p>'
	        '<p loop="(1, 2)">leaf node 1</p>'
	        '<p loop="(2, 2)">'
	        '<p loop="(2, 0)">leaf node 0</p>'
	        '<p loop="(2, 1)">leaf node 2</p>'
	        '<p loop="(2, 2)">leaf node 4</p>'
	        '</p>'
	        '<p loop="(2, 2)">leaf node 2</p>'
	        '</h1>'
		)
        self.assertEqual(test_result, expected_result)

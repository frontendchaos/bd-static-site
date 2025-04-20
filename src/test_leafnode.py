import unittest

from leafnode import LeafNode
from htmlnode import HTMLNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b","Bold text!",{"prop1":"some-property"})
        self.assertEqual(node.to_html(),'<b prop1="some-property">Bold text!</b>')
        
    def test_children_are_bad(self):
        node = LeafNode("b","Bold text!",{"prop1":"some-property"})
        self.assertIsNone(node.children)

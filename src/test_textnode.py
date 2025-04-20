import unittest
from enum import Enum

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextnode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://boot.dev")
        self.assertEqual(node, node2)
    
    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is different text", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_text_type_neq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image_text(self):
        node = TextNode("cat image",TextType.IMAGE,"https://images.unsplash.com/photo-1568152950566-c1bf43f4ab28?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTkxNzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE2NjE3NTY3NTc&ixlib=rb-1.2.1&q=80&w=400")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://images.unsplash.com/photo-1568152950566-c1bf43f4ab28?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTkxNzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE2NjE3NTY3NTc&ixlib=rb-1.2.1&q=80&w=400")

if __name__ == "__main__":
    unittest.main()
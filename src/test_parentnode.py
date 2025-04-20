import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParseMarkdown(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_apply_props(self):
        child = LeafNode("b","child")
        parent_node = ParentNode("div",[child],{"prop":"prop-val"})
        self.assertEqual(
            parent_node.to_html(),
            '<div prop="prop-val"><b>child</b></div>'
        )
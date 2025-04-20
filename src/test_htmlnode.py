import unittest

from htmlnode import HTMLNode

node1 = HTMLNode()
node2 = HTMLNode("p")
node3 = HTMLNode("p","Internal text")
node4 = HTMLNode(value="Internal text")
node5 = HTMLNode("p","internal text",[node1,node2,node3])
node6 = HTMLNode("p","internal text",[node1,node2,node3],{"href":"https://www.google.com","target":"_blank"})
node7 = HTMLNode("p")

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node1, node2)

    def test_neq(self):
        node_x = HTMLNode()
        node_y = HTMLNode("p")
        node_z = HTMLNode("p","Internal text")
        node1 = HTMLNode("p","internal text",[node_x,node_y,node_z])
        node2 = HTMLNode("p","internal text",[node_x,node_y,node_z],{"href":"https://www.google.com","target":"_blank"})
        self.assertNotEqual(node1, node2)
    
    def test_props_to_html(self):
        node_x = HTMLNode()
        node_y = HTMLNode("p")
        node_z = HTMLNode("p","Internal text")
        node1 = HTMLNode("p","internal text",[node_x,node_y,node_z],{"href":"https://www.google.com","target":"_blank"})
        text1 = ' href="https://www.google.com" target="_blank"'
        text2 = node1.props_to_html()
        self.assertEqual(text1,text2)
    

if __name__ == "__main__":
    unittest.main()
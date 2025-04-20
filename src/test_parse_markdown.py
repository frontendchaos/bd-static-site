import unittest

from textnode import TextNode, TextType
from parse_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, markdown_to_blocks, markdown_to_html_node, extract_title

class TestParseMarkdown(unittest.TestCase):
    def test_template(self):
        self.assertEqual(True,True)

    def test_no_delim(self):
        test_node = TextNode("no delimiters",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([test_node],"**",TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes),1)
        self.assertEqual(test_node, new_nodes[0])
    
    def test_bold_delim(self):
        test_node = TextNode("text **bold** more text",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([test_node],"**",TextType.BOLD_TEXT)
        expected_node_1 = TextNode("text ", TextType.NORMAL_TEXT)
        expected_node_2 = TextNode("bold", TextType.BOLD_TEXT)
        expected_node_3 = TextNode(" more text", TextType.NORMAL_TEXT)
        self.assertEqual(len(new_nodes),3)
        self.assertEqual(new_nodes[0], expected_node_1)
        self.assertEqual(new_nodes[1], expected_node_2)
        self.assertEqual(new_nodes[2], expected_node_3)
    
    def test_italic_delim(self):
        test_node = TextNode("text _italic_ more text",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([test_node],"_",TextType.ITALIC_TEXT)
        expected_node_1 = TextNode("text ", TextType.NORMAL_TEXT)
        expected_node_2 = TextNode("italic", TextType.ITALIC_TEXT)
        expected_node_3 = TextNode(" more text", TextType.NORMAL_TEXT)
        self.assertEqual(len(new_nodes),3)
        self.assertEqual(new_nodes[0], expected_node_1)
        self.assertEqual(new_nodes[1], expected_node_2)
        self.assertEqual(new_nodes[2], expected_node_3)
    
    def test_code_delim(self):
        test_node = TextNode("text `code` more text",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([test_node],"`",TextType.CODE_TEXT)
        expected_node_1 = TextNode("text ", TextType.NORMAL_TEXT)
        expected_node_2 = TextNode("code", TextType.CODE_TEXT)
        expected_node_3 = TextNode(" more text", TextType.NORMAL_TEXT)
        self.assertEqual(len(new_nodes),3)
        self.assertEqual(new_nodes[0], expected_node_1)
        self.assertEqual(new_nodes[1], expected_node_2)
        self.assertEqual(new_nodes[2], expected_node_3)
    
    def test_mismatched_delim(self):
        #print("test_mismatched_delim")
        test_node = TextNode("text **is missing a delimiter",TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([test_node],"**",TextType.BOLD_TEXT)
    
    def test_multiple_bolds_in_one_node(self):
        test_node = TextNode("text **bold** more **bold2** text",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([test_node],"**",TextType.BOLD_TEXT)
        expected_node_1 = TextNode("text ", TextType.NORMAL_TEXT)
        expected_node_2 = TextNode("bold", TextType.BOLD_TEXT)
        expected_node_3 = TextNode(" more ", TextType.NORMAL_TEXT)
        expected_node_4 = TextNode("bold2", TextType.BOLD_TEXT)
        expected_node_5 = TextNode(" text", TextType.NORMAL_TEXT)
        self.assertEqual(len(new_nodes),5)
        self.assertEqual(new_nodes[0], expected_node_1)
        self.assertEqual(new_nodes[1], expected_node_2)
        self.assertEqual(new_nodes[2], expected_node_3)
        self.assertEqual(new_nodes[3], expected_node_4)
        self.assertEqual(new_nodes[4], expected_node_5)

    def test_multiple_bolds_in_one_node_with_nothing_after_last_bold(self):
        test_node = TextNode("text **bold** more **bold2**",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([test_node],"**",TextType.BOLD_TEXT)
        expected_node_1 = TextNode("text ", TextType.NORMAL_TEXT)
        expected_node_2 = TextNode("bold", TextType.BOLD_TEXT)
        expected_node_3 = TextNode(" more ", TextType.NORMAL_TEXT)
        expected_node_4 = TextNode("bold2", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes),4)
        self.assertEqual(new_nodes[0], expected_node_1)
        self.assertEqual(new_nodes[1], expected_node_2)
        self.assertEqual(new_nodes[2], expected_node_3)
        self.assertEqual(new_nodes[3], expected_node_4)

    def test_process_multiple_nodes(self):
        test_node = TextNode("text `code` more text",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([test_node],"`",TextType.CODE_TEXT)
        expected_node_1 = TextNode("text ", TextType.NORMAL_TEXT)
        expected_node_2 = TextNode("code", TextType.CODE_TEXT)
        expected_node_3 = TextNode(" more text", TextType.NORMAL_TEXT)
        self.assertEqual(len(new_nodes),3)
        self.assertEqual(new_nodes[0], expected_node_1)
        self.assertEqual(new_nodes[1], expected_node_2)
        self.assertEqual(new_nodes[2], expected_node_3)
        
    def test_find_images_in_text(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res0 = ("rick roll","https://i.imgur.com/aKaOqIh.gif")
        res1 = ("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")
        res = extract_markdown_images(text)
        self.assertEqual(len(res),2)
        self.assertEqual(res[0],res0)
        self.assertEqual(res[1],res1)

    def test_find_links_in_text(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        res0 = ("to boot dev","https://www.boot.dev")
        res1 = ("to youtube","https://www.youtube.com/@bootdotdev")
        res = extract_markdown_links(text)
        self.assertEqual(len(res),2)
        self.assertEqual(res[0],res0)
        self.assertEqual(res[1],res1)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here This is the same paragraph on a new line",
                "- This is a list - with items",
            ],
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain the **same** even with inline stuff</code></pre></div>",
        )
    
    def test_extract_title(self):
        md = """
    # This is a title
    """
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_extract_title_no_title(self):
        md = """
    This is text with no title
    """
        with self.assertRaises(Exception):
            extract_title(md)

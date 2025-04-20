from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
	NORMAL_TEXT = "normal_text"
	BOLD_TEXT = "bold_text"
	ITALIC_TEXT = "italic_text"
	CODE_TEXT = "code_text"
	LINK = "link_text"
	IMAGE = "image_text"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, node):
        if self.text == node.text and self.text_type == node.text_type and self.url == node.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(tag=None,value=text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i",text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("unknown text type")


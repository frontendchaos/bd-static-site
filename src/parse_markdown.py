from textnode import TextNode, TextType, text_node_to_html_node
import re
from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from htmlnode import HTMLNode

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	U_LIST = "unordered_list"
	O_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        else:
            delim_count = node.text.count(delimiter)
            if delim_count % 2 != 0:
                raise Exception(f"unmatched {delimiter}")
            else:
                strs = node.text.split(delimiter)
                for i in range(len(strs)):
                    if len(strs[i]) == 0:
                        pass
                    elif i % 2 == 0:
                        new_nodes.append(TextNode(strs[i],TextType.NORMAL_TEXT))
                    else:
                        new_nodes.append(TextNode(strs[i],text_type))
    return new_nodes

def extract_markdown_images(text):
    #print(text)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    #print(text)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                imgstring = f"![{images[0][0]}]({images[0][1]})"
                strs = node.text.split(imgstring,1)
                if len(strs[0]) > 0:
                    new_nodes.append(TextNode(strs[0],TextType.NORMAL_TEXT))
                new_nodes.append(TextNode(images[0][0],TextType.IMAGE, images[0][1]))
                if len(strs) > 1 and len(strs[1]) > 0:
                    test_nodes = split_nodes_image([TextNode( strs[1], TextType.NORMAL_TEXT )])
                    new_nodes.extend( test_nodes )
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                linkstr = f"[{links[0][0]}]({links[0][1]})"
                strs = node.text.split(linkstr,1)
                if len(strs[0]) > 0:
                    new_nodes.append(TextNode(strs[0],TextType.NORMAL_TEXT))
                new_nodes.append(TextNode(links[0][0],TextType.LINK, links[0][1]))
                if len(strs) > 1 and len(strs[1]) > 0:
                    test_nodes = split_nodes_link([TextNode( strs[1], TextType.NORMAL_TEXT )])
                    new_nodes.extend( test_nodes )
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes,"_",TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    #print(">>> MARKDOWN_TO_BLOCKS")
    markdown = markdown.strip()
    blocks = []
 
    #get each block by looking for double crs
    split_lines = markdown.split("\n\n")
 
    #remove empty lines
    blocks = list(filter(lambda line: len(line) != 0, split_lines))
    #print(">>>>>> found " + str(len(blocks)) + " blocks")
 
    #clean carriage returns and white space
    for i in range(len(blocks)):
        split_lines_again = blocks[i].splitlines()
        split_lines_again = map(str.strip, split_lines_again)
        blocks[i] = " ".join(split_lines_again)
    #print(*blocks)
    #print(">>> END")
    return blocks

def block_to_block_type(md_block):
    #print("block_to_block_type: " + md_block)
    res = re.search(r"^\s*[-+*]\s+(.+)$", md_block)
    #print(str(res))
    
    # help from https://gist.github.com/elfefe/ef08e583e276e7617cd316ba2382fc40
    if len(md_block) == 0:
        return None
    elif re.search(r"^(#{1,6})\s+(.+)$", md_block) != None:
        #DONE
        return BlockType.HEADING
    elif md_block.startswith("```") and md_block.endswith("```"):
        #DONE
        return BlockType.CODE
    elif md_block.startswith(">"):
        lines = md_block.split('\n')
        for line in lines:
            if line.startswith(">") == False:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif md_block.startswith("- "):
        lines = md_block.split('\n')
        for line in lines:
            if line.startswith("- ") == False:
                return BlockType.PARAGRAPH
        return BlockType.U_LIST
    elif re.search(r"\d+\.\s+(.+)", md_block) != None:
        lines = md_block.split('\n')
        for line in lines:
            if re.search(r"^\s*\d+\.\s+(.+)$", line) == None:
                return BlockType.PARAGRAPH
        return BlockType.O_LIST
    else:
        return BlockType.PARAGRAPH

def paragraph_block_to_html_node(md_block):
    text_nodes = text_to_textnodes(md_block)
    new_nodes = []
    for tn in text_nodes:
        #print(f"{tn}: {tn.text}")
        hn = text_node_to_html_node(tn)
        if hn != None:
            #print(f"  hn: {hn.to_html()}")
            new_nodes.append(hn)
        else:
            #print("   hn: NONE WTFBBQ")
            pass
    hn = ParentNode("p",new_nodes)
    return hn

def code_block_to_html_node(md_block):
    #trim our quote characters
    md_block = md_block.strip()
    codetext = md_block[4:]
    codetext = codetext[:-4]
    lines = codetext.splitlines()
    lines = map(str.strip, lines)
    codetext = " ".join(lines)
    codenode = LeafNode("code",codetext)
    prenode = ParentNode("pre",[codenode])
    return prenode

def list_block_to_html_node(md_block, blocktype):
    # Split each line for processing
    if blocktype == BlockType.O_LIST:
        # Match ordered list items (e.g., "1. Item")
        list_items = re.split(r"\d+\.\s+", md_block)
    else:
        # Match unordered list items (e.g., "- Item")
        list_items = md_block.split("- ")
        
    #remove empty lines
    list_items = list(filter(lambda line: len(line) != 0, list_items))
    list_items = list(map(str.strip, list_items))
    list_elems = []
    #for each line
    for i in range(len(list_items)):
        #trim off the markdown at the beginning
        #get the nodes - we need to support bold/italic/etc in each list item
        text_nodes = text_to_textnodes(list_items[i])
        new_nodes = []
        #for each node in the parsed text nodes, assemble the contents into child nodes for the li
        # TODO: this needs to be a helper function, we're copy pastaing all over.
        for tn in text_nodes:
            ln = text_node_to_html_node(tn)
            if ln != None:
                new_nodes.append(ln)
            else:
                pass
        li_node = ParentNode("li",new_nodes)
        list_elems.append(li_node)
    html_type = "ul"
    if blocktype == BlockType.O_LIST:
        html_type = "ol"
    ln = ParentNode(html_type,list_elems)
    return ln

def heading_block_to_html_node(md_block):
    heading_level = 1
    htext = md_block
    if md_block.startswith("######"):
        heading_level = 6
        htext = md_block[7:]
    elif md_block.startswith("#####"):
        heading_level = 5
        htext = md_block[6:]
    elif md_block.startswith("####"):
        heading_level = 4
        htext = md_block[5:]
    elif md_block.startswith("###"):
        heading_level = 3
        htext = md_block[4:]
    elif md_block.startswith("##"):
        heading_level = 2
        htext = md_block[3:]
    elif md_block.startswith("#"):
        heading_level = 1
        htext = md_block[2:]
    h_node = LeafNode(f"h{heading_level}",htext)
    return h_node

def quote_block_to_html_node(md_block):
    #split each line for processing
    list_items = md_block.split("\n")
    new_nodes = []

    #for each line
    for item in list_items:
        #trim off the markdown at the beginning
        item = item.lstrip()
        item = item[2:]
        #get the nodes - we need to support bold/italic/etc in each list item
        text_nodes = text_to_textnodes(item)
        #for each node in the parsed text nodes, assemble the contents into child nodes for the li
        # TODO: this needs to be a helper function, we're copy pastaing all over.
        for tn in text_nodes:
            qn = text_node_to_html_node(tn)
            if qn != None:
                new_nodes.append(qn)
            else:
                pass
    quotenode = ParentNode("blockquote",new_nodes)
    return quotenode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        #print("BLOCK " + str(blocktype) + ": " + str(block))
        match blocktype:
            case BlockType.PARAGRAPH:
                hn = paragraph_block_to_html_node(block)
                nodes.append(hn)
            case BlockType.CODE:
                cn = code_block_to_html_node(block)
                nodes.append(cn)
            case BlockType.U_LIST:
                ul = list_block_to_html_node(block, blocktype)
                nodes.append(ul)
            case BlockType.O_LIST:
                ol = list_block_to_html_node(block, blocktype)
                nodes.append(ol)
            case BlockType.HEADING:
                headnode = heading_block_to_html_node(block)
                nodes.append(headnode)
            case BlockType.QUOTE:
                #print("BLOCKTYPE QUOTE")
                quotenode = quote_block_to_html_node(block)
                nodes.append(quotenode)
            case _:
                raise Exception("could not determine block type")
    parent_node = ParentNode("div",nodes)
    return parent_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.HEADING:
            if block.startswith("#") == True and block.startswith("##") == False:
                return block[2:]
    raise Exception("could not find h1 header")

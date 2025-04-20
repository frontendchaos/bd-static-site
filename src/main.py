from textnode import TextType, TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from parse_markdown import * #split_nodes_delimiter,extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type
from fileio import *
from generate_site import generate_page, generate_content

#get first arg to main.py
import sys
import os

print("=-=-=- main.py -=-=-=")

def main():
    #tn = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    #print(tn)
    #hn = HTMLNode(tag="p",value="my paragraph text",children=[],props={})
    #print(hn)
    #ln = LeafNode("h1","some header text",{"href": "https://www.google.com"})
    #print(ln.to_html())
    #pn = ParentNode("p",[LeafNode("b","Bold Text"),LeafNode("i","italic text")],{"someprop":"the-prop"})
    #print(pn.to_html())
    #markdown_text = TextNode("This is text with two `code blocks` in it - `here is the second one`", TextType.NORMAL_TEXT)
    #split_nodes = split_nodes_delimiter([markdown_text],"`",TextType.CODE_TEXT)
    #for node in split_nodes:
    #    print(node)
    #bad_markdown_text = TextNode("this has **bad delimiters", TextType.NORMAL_TEXT)
    #try:
    #    split_nodes_bad = split_nodes_delimiter([bad_markdown_text],"**",TextType.BOLD_TEXT)
    #except Exception as e:
    #    print(e)
    #text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    #text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    #print("EXTRACT LINK RESULT: " + str(extract_markdown_links(text)))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    #node = TextNode(
    #    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #    TextType.NORMAL_TEXT,
    #)
    #new_nodes = split_nodes_link([node])
    #print("ORIGINAL TEXT: " + node.text)
    #print("NEW NODES: " + str(new_nodes))
    #node = TextNode(
    #    "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
    #    TextType.NORMAL_TEXT,
    #)
    #new_nodes = split_nodes_image([node])
    #print("ORIGINAL TEXT: " + node.text)
    #print("NEW NODES: " + str(new_nodes))
    
    #text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    #nodes = text_to_textnodes(text)
    #for node in nodes:
    #    print(str(node))
    #md = """
#This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a good list
# - with items

# - This is a bad list
# with items


# h1

## h2

### h3

#### h4

##### h5

###### h6

####### paragraph (7)

# ```code
# block```

# > bad quote
# quote2

# > good quote
# > quote2

# 1. good olist 1
# 2. good olist 2

# 1. bad olist 1
# bad olist 2

# """
#     blocks = markdown_to_blocks(md)
#     print(*blocks, sep='<\n')
#     print()
#     for block in blocks:
#         print(str(block_to_block_type(block)))
#     md = """
# ### H3 Text

# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# - list item 1
# - list item 2
# - list item 3

# 1. olist **item 1**
# 2. olist item 2
# 3. olist item 3

# ```code
# block```

# >
# > quote text
# > quote line 2
# """
    #PASS
    # md = """
    # This is **bolded** paragraph
    # text in a p
    # tag here

    # This is another paragraph with _italic_ text and `code` here

    # """
    # #expecting: <div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>
    # retval = markdown_to_html_node(md)
    # # expecting: <div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>
    # print(retval.to_html())
    # PASS
    #     md = """
    # This is **bolded** paragraph

    # This is another paragraph with _italic_ text and `code` here
    # This is the same paragraph on a new line

    # - This is a list
    # - with items
    # """
    #     retval = markdown_to_html_node(md)
    #expecting: <div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>
    #print(retval.to_html())
    
    #quote blocks
#     md = """
#     ```
# This is text that _should_ remain
# the **same** even with inline stuff
#     ```
#     """
#     retval = markdown_to_html_node(md)
#     print(retval.to_html())
#     md = """
# - list item A
# - list item B
# - list item C
#     """
#     blocks = markdown_to_blocks(md)
#     print(*blocks, sep='<\n')
#     ln = list_block_to_html_node(blocks[0],BlockType.U_LIST)
#     print(ln.to_html())
    #retval = markdown_to_html_node(md)
    #print(retval.to_html())

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f"Basepath: {basepath}")
    cur_path = get_root_path()
    try:
        copy_to_dir(f"{cur_path}/static/",f"{cur_path}/docs/")
    except Exception as e:
        print(e)
    generate_content(basepath)
    pass

main()
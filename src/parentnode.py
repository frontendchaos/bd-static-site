from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None,children,props)
    
    def to_html(self):
        retval = ""
        if self.tag == None:
            raise ValueError("no tag")
        if self.value != None:
            raise ValueError("parent node can't have a value")
        if self.children == None:
            retval += f"<{self.tag}{self.props_to_html()}/>"
        else:
            retval += f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                retval += child.to_html()
            retval += f"</{self.tag}>"
        return retval
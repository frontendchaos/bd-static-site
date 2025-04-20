
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, node):
        if node != None and self.tag == node.tag and self.value == node.value and self.children == node.children and self.props == node.props:
            return True
        return False
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props_to_html()})"
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        retval = ""
        for prop in self.props:
            retval += f' {prop}="{self.props[prop]}"'
        #retval = retval.rstrip()
        return retval
        
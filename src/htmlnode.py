class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise ValueError("Not implemented")

    def props_to_html(self):
        return "".join(f" {key}=\"{value}\"" for key, value in self.props.items())

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return f"{self.value}"
            
        html_props = self.props_to_html() if self.props else ""
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag = tag, value=None, children=children, props=props)

    def __repr__(self):

        def format_children(children, indent=2):
            indent_str = ' ' * (indent)
            return '\n'.join(f"{indent_str}{child.__repr__()}" for child in children)

        html_children = format_children(self.children) if self.children else "None"
        html_props = self.props_to_html() if self.props else "" 

        return (f"ParentNode(tag={self.tag}, \n"
                f"  children=[\n{html_children}\n],"
                f"{html_props})")

    def __eq__(self, other):
        return self.tag == other.tag and self.children == other.children and self.props == other.props

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")
        html_props = self.props_to_html() if self.props else ""
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{html_props}>{children_html}</{self.tag}>"
            












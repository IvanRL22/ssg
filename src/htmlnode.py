
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props = {self.props}"

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        result = ""
        for attr,val in self.props.items():
            result += f"{attr}=\"{val}\" "

        return result[:-1]


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")

        if not self.tag:
            return self.value

        if self.props:
            props = f" {self.props_to_html()}"
        else:
            props = ""

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children:list[HTMLNode], props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")

        if not self.children:
            raise ValueError("All parent nodes must have at least one child")

        if self.props:
            props = f" {self.props_to_html()}"
        else:
            props = ""

        return f"<{self.tag}{props}>{"".join(map(lambda node: node.to_html(), self.children))}</{self.tag}>"
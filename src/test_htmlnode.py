import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # HTMLNode tests
    def test_empty_props(self):
        html_node = HTMLNode()
        self.assertEqual(html_node.props_to_html(), "")

    def test_one_prop(self):
        html_node = HTMLNode(props={"id":"node_id"})
        self.assertEqual(html_node.props_to_html(), "id=\"node_id\"")

    def test_multiple_props(self):
        html_node = HTMLNode(props={"id": "node_id", "target":"_blank", "href":"https://www.google.com"})
        self.assertEqual(html_node.props_to_html(), "id=\"node_id\" target=\"_blank\" href=\"https://www.google.com\"")

    # LeafNode tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is some text")
        self.assertEqual(node.to_html(), "This is some text")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    # ParentNode tests
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

    def test_course_example(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_without_tag(self):
        parent_node = ParentNode("", []) # There is also no children but tag is checked first
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_without_children(self):
        parent_node = ParentNode("p", [])
        self.assertRaises(ValueError, parent_node.to_html)
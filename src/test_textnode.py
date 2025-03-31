import unittest

from src.htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_equal_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "localhost:8080")
        node2 = TextNode("This is a text node", TextType.BOLD, "localhost:8080")
        self.assertEqual(node, node2)

    def test_not_eq_by_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "localhost:8080")
        self.assertNotEqual(node, node2)

    def test_not_eq_with_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "localhost:8080")
        self.assertNotEqual(node, node2)

    def test_not_eq_by_text(self):
        node = TextNode("This is a text node", TextType.BOLD, "localhost:8080")
        node2 = TextNode("This is a different text node", TextType.BOLD, "localhost:8080")
        self.assertNotEqual(node, node2)

    # TODO Add text_node_to_html_node tests



if __name__ == "__main__":
    unittest.main()
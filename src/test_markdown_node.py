import unittest

from src.markdown_node import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestMarkdownNode(unittest.TestCase):

    def test_no_text_node(self):
        nodes = [
            TextNode("This text should be bold", TextType.BOLD),
            TextNode("This text should be italic", TextType.ITALIC),
            TextNode("public static void main(String[] args)", TextType.CODE)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(nodes, result)

    def test_text_nodes(self):
        nodes = [
            TextNode("This is some normal text", TextType.TEXT),
            TextNode("This is some more normal text", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(nodes, result)

    def test_boot_dev_example(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(result,
                             [
                                 TextNode("This is text with a ", TextType.TEXT),
                                 TextNode("code block", TextType.CODE),
                                 TextNode(" word", TextType.TEXT),
                             ])

    def test_multiple(self):
        node = TextNode("This is a **text** node with **several** bolded **words**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(result,
                             [
                                 TextNode("This is a ", TextType.TEXT),
                                 TextNode("text", TextType.BOLD),
                                 TextNode(" node with ", TextType.TEXT),
                                 TextNode("several", TextType.BOLD),
                                 TextNode(" bolded ", TextType.TEXT),
                                 TextNode("words", TextType.BOLD),
                             ])

    def test_with_other_delimiter(self):
        node = TextNode("This _is a_ **text node** with _several_ different **markdown** styles", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(result,
                             [
                                 TextNode("This _is a_ ", TextType.TEXT),
                                 TextNode("text node", TextType.BOLD),
                                 TextNode(" with _several_ different ", TextType.TEXT),
                                 TextNode("markdown", TextType.BOLD),
                                 TextNode(" styles", TextType.TEXT)
                             ])

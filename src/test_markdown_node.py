import unittest

from src.markdown_node import split_nodes_delimiter, extract_markdown_images, extract_markdown_link, split_nodes_image, \
    split_nodes_link, text_to_textnodes
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

    # --- Image extraction tests ---
    def test_no_image(self):
        matches = extract_markdown_images("This is some text without any kind of markdown image")
        self.assertListEqual([], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_boot_dev_image_markdown(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual(matches,
                             [
                                 ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                                 ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
                             ])

    def test_does_not_match_link(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([], matches)

    # --- Image extraction tests ---
    def test_no_link(self):
        matches = extract_markdown_link("This is some text without any kind of markdown link")
        self.assertListEqual([], matches)

    def test_boot_dev_link_markdown(self):
        matches = extract_markdown_link("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual(matches,
                             [
                                 ("to boot dev", "https://www.boot.dev"),
                                 ("to youtube", "https://www.youtube.com/@bootdotdev")
                             ])

    def test_does_not_match_images(self):
        matches = extract_markdown_link(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_node_starting_with_link(self):
        matches = extract_markdown_link("[Click here](boot.dev) to learn backend!")
        self.assertListEqual(matches, [('Click here', 'boot.dev')])

    # --- Test splitting text node with images
    def test_no_images(self):
        node = TextNode("This is just a text node, no images, no links", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_starting_with_image(self):
        node = TextNode(
            "![Awesome image init?](https://www.boot.dev/img/bootdev-logo-full-small.webp)Enjoy the logo!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Awesome image init?", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
                TextNode("Enjoy the logo!", TextType.TEXT)
            ],
            new_nodes
        )

    # --- Test splitting test node with links
    def test_no_links(self):
        node = TextNode("This is just a text node, no images, no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://en.wikipedia.org/wiki/Hyperlink) and another [link](https://en.wikipedia.org/wiki/Link)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://en.wikipedia.org/wiki/Hyperlink"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://en.wikipedia.org/wiki/Link"
                ),
            ],
            new_nodes
        )

    def test_split_links_starting_with_link(self):
        node = TextNode(
            "[Click here](https://www.google.com) to go to google.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click here", TextType.LINK, "https://www.google.com"),
                TextNode(" to go to google.", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_links_starting_and_ending_with_links(self):
        node = TextNode(
            "[Click here](https://www.google.com) to go to google. Or you prefer to go to boot.dev, [click here](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click here", TextType.LINK, "https://www.google.com"),
                TextNode(" to go to google. Or you prefer to go to boot.dev, ", TextType.TEXT),
                TextNode("click here", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )

    # --- Test text to text nodes
    def test_text_to_text_nodes_simple_text(self):
        text = "This is some simple text, no markdown, no nothing. Simple stuff."
        result = text_to_textnodes(text)
        self.assertListEqual(result,
                             [
                                 TextNode("This is some simple text, no markdown, no nothing. Simple stuff.", TextType.TEXT)
                             ])

    def test_text_to_text_nodes_boot_dev_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(result,
                             [
                                 TextNode("This is ", TextType.TEXT),
                                 TextNode("text", TextType.BOLD),
                                 TextNode(" with an ", TextType.TEXT),
                                 TextNode("italic", TextType.ITALIC),
                                 TextNode(" word and a ", TextType.TEXT),
                                 TextNode("code block", TextType.CODE),
                                 TextNode(" and an ", TextType.TEXT),
                                 TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                 TextNode(" and a ", TextType.TEXT),
                                 TextNode("link", TextType.LINK, "https://boot.dev"),
                             ])


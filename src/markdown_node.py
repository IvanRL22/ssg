from src.textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if TextType.TEXT != node.text_type:
            new_nodes.append(node)
            continue

        split = node.text.split(delimiter)
        if len(split) == 1: # No splits, delimiter is not present
            new_nodes.append(node)
            continue

        if len(split) % 2 == 0:
            raise ValueError("Invalid Markdown syntax: no closing delimiter was found")

        initial_node = TextNode(split[0], TextType.TEXT)
        # Node could have started with delimiter, avoid adding extra empty text node
        if initial_node.text != "":
            new_nodes.append(initial_node)

        for n in range(1, len(split) - 1, 2):
            new_nodes.append(TextNode(split[n], text_type))
            after_markdown = TextNode(split[n+1], TextType.TEXT)
            # Node could end with delimiter, avoid adding extra empty node
            if after_markdown.text != "":
                new_nodes.append(after_markdown)


    return new_nodes

def extract_markdown_images(text):
    """
        ! ->            markdown starting character for an image
        \[ ->           opening bracket
            (.+?) ->    capture 1 or more characters lazily
        \] ->           closing bracket
        \( ->           opening parenthesis
            (.+?) ->    capture any 1 or more characters lazily
        \) ->           closing parenthesis
    """
    return re.findall(
        "!\[(.+?)\]\((.+?)\)",
        text)

def extract_markdown_link(text):
    """
    (?: ->          start non-capturing group
        ^ ->        beginning of the line
        | ->        or
        [^!] ->     a character that is not '!', this is to avoid matching markdown images
     ) ->           close non-capturing group
     \[ ->          opening bracket
        (.+?) ->    capture any amount of characters lazily
    \] ->           closing bracket
    \( ->           opening parenthesis
        (.+?) ->    capture any amount of characters lazily
    \) ->           closing parenthesis
    """
    return re.findall(
        "(?:^|[^!])\[(.+?)\]\((.+?)\)",
        text)

def split_nodes_image(old_nodes:list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        if text.index(images[0][0]) == 2:  # Deal with nodes starting with an image
            starting_link = images[0][0]
            new_nodes.append(
                TextNode(starting_link, TextType.IMAGE, url=images[0][1])
            )
            text = text[text.index(images[0][1]) + len(images[0][1]) + 1:]
            images = images[1:]

        for match in images:
            new_nodes.append(
                TextNode(
                    text[0:text.index(match[0]) - 2],
                    TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, url=match[1]))
            text = text[text.index(match[1]) + len(match[1]) + 1:]

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes:list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_link(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        if text.index(links[0][0]) == 1: # Deal with nodes starting with a link
            starting_link = links[0][0]
            new_nodes.append(
                TextNode(starting_link, TextType.LINK, url=links[0][1])
            )
            text = text[text.index(links[0][1]) + len(links[0][1]) + 1:]
            links = links[1:]

        for match in links: # Inside the loop we expect to always start with text
            new_nodes.append(
                TextNode(
                    text[0:text.index(match[0]) - 1],
                    TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, url=match[1]))
            text = text[text.index(match[1]) + len(match[1]) + 1:]

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    with_images = split_nodes_image([TextNode(text, TextType.TEXT)])
    with_links = split_nodes_link(with_images)
    with_bold = split_nodes_delimiter(with_links, "**", TextType.BOLD)
    with_italic = split_nodes_delimiter(with_bold, "_", TextType.ITALIC)
    with_code = split_nodes_delimiter(with_italic, "`", TextType.CODE)
    return with_code

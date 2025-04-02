from src.textnode import TextNode, TextType


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


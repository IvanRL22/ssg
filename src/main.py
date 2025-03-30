from textnode import TextNode, TextType


def main():
    dummy = TextNode("This is dome dummy text", TextType.NORMAL_TEXT, "localhost:8080")

    print(dummy)

if __name__ == '__main__':
    main()
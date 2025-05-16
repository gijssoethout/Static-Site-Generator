from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode 

def main():
    textnode = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(textnode)

def text_node_to_html_node(text_node):
    match TextType:
        case TextType.TEXT:
            return LeafNode(None, f"{text_node.text}")
        case TextType.BOLD:
            return LeafNode("b", f"{text_node.text}")
        case TextType.ITALIC:
            return LeafNode("i", f"{text_node.text}")
        case TextType.CODE:
            return LeafNode("code", f"{text_node.text}")
        case TextType.LINK:
            return LeafNode("a", f"{text_node.text}", {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid TextType")

if __name__ == "__main__":
    main()
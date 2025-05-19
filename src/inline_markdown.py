import re
from textnode import TextType, TextNode 


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception(f"Invalid Markdown: No closing delimiter")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 1:
                split_nodes.append(TextNode(sections[i], text_type))
            else:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        images = extract_markdown_images(original_text)

        if images == []:
            new_nodes.append(node)
            continue

        for i in range(len(images)):
            image_alt, image_link = images[i]
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
        
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        links = extract_markdown_links(original_text)

        if links == []:
            new_nodes.append(node)
            continue

        for link_text, link_url in links:
            sections = original_text.split(f"[{link_text}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    textnodes = [TextNode(text, TextType.TEXT)]
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_images(textnodes)
    textnodes = split_nodes_links(textnodes)
    return textnodes
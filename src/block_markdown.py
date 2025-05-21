from enum import Enum
from blocktype import (
    BlockType,
    is_heading_block,
    is_code_block,
    is_quote_block,
    is_unordered_list_block,
    is_ordered_list_block,
)

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def block_to_block_type(markdown_block):
    if is_heading_block(markdown_block):
        return BlockType.HEADING
    elif is_code_block(markdown_block):
        return BlockType.CODE
    elif is_quote_block(markdown_block):
        return BlockType.QUOTE
    elif is_unordered_list_block(markdown_block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list_block(markdown_block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for block in split_markdown:
        if len(block) != 0:
            block = block.strip()
            blocks.append(block)
            
        
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    match block_to_block_type(block):
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.splitlines()
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not is_code_block(block):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.splitlines()
    new_lines = []
    for line in lines:
        if not is_quote_block(line):
            raise ValueError(f"Invalid quote block: {line}")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    list_items = block.splitlines()
    html_list_items = []
    for list_item in list_items:
        text = list_item[2:]
        children = text_to_children(text)
        html_list_items.append(ParentNode("li", children))
    return ParentNode("ul", html_list_items)

def ordered_list_to_html_node(block):
    list_items = block.splitlines()
    html_list_items = []
    for list_item in list_items:
        text = list_item[3:]
        children = text_to_children(text)
        html_list_items.append(ParentNode("li", children))
    return ParentNode("ol", html_list_items)
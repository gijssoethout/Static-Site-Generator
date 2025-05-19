from enum import Enum
from blocktype import (
    BlockType,
    is_heading_block,
    is_code_block,
    is_quote_block,
    is_unordered_list_block,
    is_ordered_list_block,
)

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
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                pass
            case BlockType.CODE:
                pass
            case BlockType.QUOTE:
                pass
            case BlockType.UNORDERED_LIST:
                pass
            case BlockType.ORDERED_LIST:
                pass
            case BlockType.PARAGRAPH:
                pass
            case _:
                raise Exception("Invalid BlockType")
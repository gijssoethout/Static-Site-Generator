import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def is_heading_block(markdown_block):
    pattern = r"^#{1,6} "
    return re.search(pattern, markdown_block) != None

def is_code_block(markdown_block):
    pattern = r"^```[\s\S]*?```$"
    return re.search(pattern, markdown_block) != None

def is_quote_block(markdown_block):
    lines = markdown_block.splitlines()
    pattern = r"^>"
    for line in lines:
        if re.search(pattern, line) == None:
            return False
    return True

def is_unordered_list_block(markdown_block):
    lines = markdown_block.splitlines()
    pattern = r"^- "
    for line in lines:
        if re.search(pattern, line) == None:
            return False
    return True

def is_ordered_list_block(markdown_block):
    lines = markdown_block.splitlines()
    expected = 1
    for line in lines:
        if not line.startswith(f"{expected}. "):
            return False
        expected += 1
    return True
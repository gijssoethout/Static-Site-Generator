import unittest
from block_markdown import (
     markdown_to_blocks,
     block_to_block_type,
)

from blocktype import BlockType


class TestBlockMarkdown(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_newlines(self):
            md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_block_to_block_heading(self):
            headings = [
                  "# heading1",
                  "## heading2",
                  "### heading3",
                  "#### heading4",
                  "##### heading5",
                  "###### heading6",
                  ]
            result = []
            for heading in headings:
                result.append(block_to_block_type(heading))
            self.assertListEqual(
                [
                    BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.HEADING,   
                ],
                result,
            )

        def test_block_to_block(self):
            headings = [
                  "# heading block",
                  "``` code block ```",
                  "> quote block\n>2nd line",
                  "- list item1\n- list item2",
                  "1. ordered list item\n2. ordered list item 2",
                  "this is a paragraph block",
                  ]
            result = []
            for heading in headings:
                result.append(block_to_block_type(heading))
            self.assertListEqual(
                [
                    BlockType.HEADING,
                    BlockType.CODE,
                    BlockType.QUOTE,
                    BlockType.UNORDERED_LIST,
                    BlockType.ORDERED_LIST,
                    BlockType.PARAGRAPH,   
                ],
                result,
            )

        def test_block_to_block_types(self):
            block = "# heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
            block = "```\ncode\n```"
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
            block = "> quote\n> more quote"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
            block = "- list\n- items"
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
            block = "1. list\n2. items"
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
            block = "paragraph"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()

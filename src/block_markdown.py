from textnode import *
from htmlnode import *
from inline_markdown import *
import re

# Base function to convert markdown into HtmlNodes to be later converted to html.
# Uses markdown_to_blocks(), block_to_block_type() and text_to_children()
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = convert_block_to_html_node(block, block_type)
        if isinstance(block_node, list):
            block_nodes.extend(block_node)
        else:
            block_nodes.append(block_node)
    return ParentNode("div", block_nodes)

def convert_block_to_html_node(block, block_type):
    if block_type == "unordered_list":
        return ParentNode("ul", convert_list_block(block, is_ordered=False))
    elif block_type == "ordered_list":
        return ParentNode("ol", convert_list_block(block, is_ordered=True))
    elif block_type == "code":
        return convert_code_block(block)
    elif block_type == "quote":
        return convert_quote_block(block) 
    elif block_type == "heading":
        return convert_heading_block(block)
    else:
        return convert_paragraph_block(block)

def convert_list_block(block, is_ordered):
    lines = block.split("\n")
    items = []
    for line in lines:
        if is_ordered:
            content = line.split(". ", 1)[1]
        else:
            content = re.sub(r"[*-]\s", "", line)
        items.append(ParentNode("li", text_to_children(content)))
    return items

def convert_code_block(block):
    content = block.strip("```").lstrip("\n")
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, content, None)])])

def convert_quote_block(block):
    lines = block.split("\n")
    content = " ".join(line.lstrip("> ") for line in lines)
    return ParentNode("blockquote", text_to_children(content))

def convert_heading_block(block):
    level = len(block.split()[0]) # Count number of '#'
    content = block.lstrip("#").strip()
    return ParentNode(f"h{level}", text_to_children(content))

def convert_paragraph_block(block):
    return ParentNode("p", text_to_children(block))

def text_to_children(text):
    inner_text_children = text_to_textnodes(text)
    return [text_node_to_html_node(child) for child in inner_text_children]

# Split markdown into blocks by double newlines
def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    processed_blocks = []

    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            processed_blocks.append(stripped_block)
    return processed_blocks

# Get the type of block, default is paragraph
def block_to_block_type(block):
    if re.match(r'^#{1,6}', block):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return "quote"
    if all(re.match(r'^[*-] ', line) for line in lines):
        return "unordered_list"

    if all(re.match(r'^\d+\. ', line) for line in lines):
        numbers = [int(line.split(".")[0]) for line in lines]
        if numbers == list(range(1,len(numbers) + 1)):
                return "ordered_list"

    return "paragraph"     

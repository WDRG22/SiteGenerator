from textnode import *
from htmlnode import *
from inline_markdownparser import *
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    processed_blocks = []

    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            processed_blocks.append(stripped_block)
    return processed_blocks

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "quote":
            block_node = ParentNode("blockquote", text_to_children(block, block_type))
            block_nodes.append(block_node)
        elif block_type == "unordered_list":
            block_node = ParentNode("ul", text_to_children(block, block_type))
            block_nodes.append(block_node)
        elif block_type == "ordered_list":
            block_node = ParentNode("ol", text_to_children(block, block_type))
            block_nodes.append(block_node)
        elif block_type == "code":
            block_node = ParentNode("pre", text_to_children(block, block_type))
            block_nodes.append(block_node)
        else:
            children = text_to_children(block, block_type)
            for child in children:
                block_nodes.append(child)

    return ParentNode("div", block_nodes)
        
def text_to_children(text, text_type):
    lines = text.split("\n")
    children = []

    def process_line(line, tag):
            inner_text_children = text_to_textnodes(line)
            inner_html_children = [text_node_to_html_node(child) for child in inner_text_children]
            return ParentNode(tag, inner_html_children).to_html()

    for line in lines:
        if text_type == "quote":
            tag = "p"
            line = line.lstrip(">")
        elif text_type == "unordered_list":
            tag = "li"
            line = line.lstrip("*- ")
        elif text_type == "ordered_list":
            tag = "li"
            line = line.split(". ", 1)[1]
        elif text_type == "code":
            tag = "code"
            line = line.strip("```")
        elif text_type == "heading":
            stripped_line = line.strip("#")
            h_tag_num = len(line) - len(stripped_line)
            tag = f"h{h_tag_num}"
            line = stripped_line
        else:            
            tag = "p"
            
        children.append(process_line(line, tag))
    return children

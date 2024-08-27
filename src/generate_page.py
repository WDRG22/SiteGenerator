from block_markdown import *
from inline_markdown import *
from textnode import *
from htmlnode import *


def extract_title(markdown):
    html_node = markdown_to_html_node(markdown)
    for child in html_node.children:
        if child.tag == 'h1':
            title_node = child
            title = ""
            for child in title_node.children:
                title += child.value
            return title.strip()

    raise ValueError("No heading found") 


def generate_page(src_path, template_path, dst_path):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")

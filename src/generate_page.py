import os
import re
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
    # Open and store the src and template files
    src_file = ''
    with open(src_path, 'r') as file:
        src_file = file.read()

    template = ''
    with open(template_path, 'r') as file:
        template = file.read()
    
    # Convert the src file from markdown to html and retrieve its title
    content = markdown_to_html_node(src_file).to_html()
    title = extract_title(src_file)

    # Modify the template with the new title and html content
    html = modify_template(template, title, content)

    # Write the new html file to the dst folder (create folder if it doesn't exist
    os.makedirs(dst_path, exist_ok=True)
    with open(os.path.join(dst_path, "index.html"), 'w') as file:
        file.write(html)


# Replace the Title and Content placeholders with actual title and content
def modify_template(template, title, content):
    modified_template = re.sub(r'\{\{ Title \}\}', title, template)
    modified_template = re.sub(r'\{\{ Content \}\}', content, modified_template)
    return modified_template

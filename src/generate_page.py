import os
import re
from block_markdown import *
from inline_markdown import *
from textnode import *
from htmlnode import *

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# generate_page() helper function. Gets title from markdown file
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

# generate_page() helper function. Replaces te Title and Content placeholders in the
# template with actual title and content from markdown file
def modify_template(template, title, content):
    modified_template = re.sub(r'\{\{ Title \}\}', title, template)
    modified_template = re.sub(r'\{\{ Content \}\}', content, modified_template)
    return modified_template

# Generate html page from markdown file using a template
def generate_page(src_path, template_path, dst_path):
    # Open and store the src and template files
    with open(src_path, 'r') as file:
        src_file = file.read()

    with open(template_path, 'r') as file:
        template = file.read()
    
    # Convert the src file from markdown to html and retrieve its title
    content = markdown_to_html_node(src_file).to_html()
    title = extract_title(src_file)

    # Modify the template with the new title and html content
    html = modify_template(template, title, content)

    # Write the new html file to the dst folder 
    with open(dst_path, 'w') as file:
        file.write(html)
        print(f">> Wrote file '{file.name}'")

def generate_page_recursive(src_path, template_path, dst_path):
    for item in os.listdir(src_path):
        item_src_path = os.path.join(src_path, item)
        item_dst_path = os.path.join(dst_path, item)
        # If markdown file, generate html file from template and place in dst_path folder
        if os.path.isfile(item_src_path):
            if item.endswith(".md"):
                os.makedirs(os.path.dirname(item_dst_path), exist_ok=True)
                # Generate HTML file
                html_filename = os.path.splitext(item)[0] + ".html"
                html_dst_path = os.path.join(os.path.dirname(item_dst_path), html_filename)
                generate_page(item_src_path, template_path, html_dst_path)
        # Else recurse on any subdirectories, updating dst_path to match src folder structure
        else:
            generate_page_recursive(item_src_path, template_path, item_dst_path)

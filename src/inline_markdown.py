import re
from textnode import TextNode

# Split text nodes on some delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):

    ret = []
    for node in old_nodes:
        if node.text_type != "text":
            ret.append(node)
            continue
        
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"\nUnmatched delimiter '{delimiter}' found in node: {node}\n")

        for i in range(len(parts)):
            if parts[i] == "":
                continue

            if i % 2 == 0:
                ret.append(TextNode(text=parts[i], text_type="text"))
            else:
                ret.append(TextNode(text=parts[i], text_type=text_type))

    return ret

# Get any images in markdown text
def extract_markdown_images(text):
    ret = []
    pattern = r"!\[(.*?)\]\((.*?)\)"    
    return  re.findall(pattern, text)

# Get any links in markdown text
def extract_markdown_links(text):
    ret = []
    pattern = r"\[(.*?)\]\((.*?)\)"    
    return re.findall(pattern, text)

# Split markdown text where images occur
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for alt, url in images:
            split_text = original_text.split(f"![{alt}]({url})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], "text"))

            new_nodes.append(TextNode(alt, "image", url))
            original_text = split_text[1]
        
        if original_text:
            new_nodes.append(TextNode(original_text, "text"))
    return new_nodes

# Split markdown text where links occur
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in links:
            split_text = remaining_text.split(f"[{alt}]({url})", 1)
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], "text"))
            new_nodes.append(TextNode(alt, "link", url))
            remaining_text = split_text[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, "text"))

    return new_nodes

# Convert text into TextNode objects split on any delimiters
def text_to_textnodes(text):
    text_nodes = [TextNode(text, "text")]
    text_nodes = split_nodes_delimiter(text_nodes, "**", "bold")
    text_nodes = split_nodes_delimiter(text_nodes, "*", "italic")
    text_nodes = split_nodes_delimiter(text_nodes, "`", "code")
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes


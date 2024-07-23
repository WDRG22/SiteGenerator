from src.textnode import TextNode
from src.htmlnode import HTMLNode

def main():
    textNode = TextNode("Example text for testing", "bold", "www.google.com")
    print(textNode)
    
    htmlNode = HTMLNode("<p>", "Test value", ["child1", "child2", "child3"], [1,2,3])
    print(htmlNode)

main()

from textnode import TextNode
from htmlnode import HTMLNode
import os
import shutil

def copy_directory(src, dst):
    # ensure destination directory exists
    if not os.path.exists(dst):
        os.makedirs(dst)
    # clear exisiting content in destination
#    for item in os.listdir(dst):
#       itempath = os.path.join(dst, item)
#      if os.path.isfile(itempath):
#            os.remove(itempath)
#        else:
#            shutil.rmtree(itempath)

    # Loop thru items in src directory
    for item in os.listdir(src):
        itempath_src = os.path.join(src, item)
        itempath_dst = os.path.join(dst, item)

        # copy files or create subdirectories recursively
        if os.path.isfile(itempath_src):
            shutil.copy2(itempath_src, itempath_dst)
            print(f"Copied file: {itempath_src} -> {itempath_dst}")
        else:
            copy_directory(itempath_src, itempath_dst)



def main():
    
    copy_directory("static", "public")

    
if __name__ == "__main__":
    main()

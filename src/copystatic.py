import os
import shutil

def copy_files_r(src, dst):
    # Ensure dst directory exists
    if not os.path.exists(dst):
        os.makedirs(dst)
      
    # Copy src items to dst
    for item in os.listdir(src):
        itempath_src = os.path.join(src, item)
        itempath_dst = os.path.join(dst, item)

        # If src item is a file copy it to dst
        if os.path.isfile(itempath_src):
            shutil.copy2(itempath_src, itempath_dst)
            print(f"Copied file: {itempath_src} -> {itempath_dst}")

        # Else it is a directory -> recurse on it
        else:
            copy_files_r(itempath_src, itempath_dst)

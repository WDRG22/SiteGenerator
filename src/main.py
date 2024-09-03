import os
import shutil
from copy_static import *
from generate_page import *

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir_path_static = os.path.join(project_root, 'static')
dir_path_public = os.path.join(project_root, 'public')


def main():

    print("Deleting public directory")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_files_r(dir_path_static, dir_path_public)
    
    src_path = os.path.join(project_root, 'content')
    template_path = os.path.join(project_root, 'template.html')
    dst_path = os.path.join(project_root, 'public')
    generate_page_recursive(src_path, template_path, dst_path)

if __name__ == "__main__":
    main()

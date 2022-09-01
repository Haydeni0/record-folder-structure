from logging import root
import os
from typing import Generator, Iterable
from anytree import Node, RenderTree
import sys


def os_walk(root_folder, max_depth = 4):
    # Test os.walk based directory tree traversal

    # for (root,dirs,files) in walk:
    #     print(root)
    #     print(dirs)
    #     print(files)
    #     print('--------------------------------')
    root = Node(root_folder)
    if max_depth > 0:
        getChild(root, max_depth)

    sys.stdout.reconfigure(encoding="utf-8")
    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")
    # print(RenderTree(root))

    pass


def getChild(node: Node, max_depth: int):
    path = "/".join([_.name for _ in node.path])
    walk = os.walk(path)
    try:
        # This will throw a StopIteration exception when reaching the end of a branch
        dirpath, dirnames, filenames = next(walk)
    except StopIteration:
        return

    for child_dir in dirnames:
        c = Node(child_dir, parent = node)
        if c.depth < max_depth:
            getChild(c, max_depth)
            
    for child_file in filenames:
        Node(child_file, parent = node)
    


if __name__ == "__main__":
    root_folder = "./1"
    root_folder = "C:\\Users\\Hayden\\Documents\\GitRepositories"
    os_walk(root_folder, max_depth=4)

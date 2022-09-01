from logging import root
import os
from anytree import Node, RenderTree
import sys


def main(root_folder: str, max_depth: int = 4) -> Node:
    # Test os.walk based directory tree traversal
    dir_tree = Node(root_folder)
    if max_depth > 0:
        getChild(dir_tree, max_depth)

    # My default stdout is encoded in cp1252, ensure it changes to utf-8 for special characters
    sys.stdout.reconfigure(encoding="utf-8")
    for pre, fill, node in RenderTree(dir_tree):
        print(f"{pre}{node.name}")
    # print(RenderTree(root))

    return dir_tree


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
    dir_tree = main(root_folder, max_depth=10)
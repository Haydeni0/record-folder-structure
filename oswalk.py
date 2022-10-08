#!/usr/bin/env python3

import os
from time import time
from anytree import Node, RenderTree
import sys
from enum import Enum
from typing import Tuple


class Status(Enum):
    OK = 0
    MAX_DEPTH_REACHED = 1
    MAX_TIME_EXCEEDED = -1


def crawlFolderPy(root_folder: str, max_depth: int = 3, max_time: float = 1e9) -> Tuple[Node, Status]:
    """
    Python serial os.walk based folder crawler
    
    Conducts a recursive depth first search (up to a maximum depth) of folder.

    Args:
        root_folder (str): Path to the folder to use as the root of the search
        max_depth (int, optional): Maximum folder depth to search to. Defaults to 3.
        max_time (float, optional): Maximum time to spend searching. Defaults to 1e9.

    Returns:
        Tuple[anytree.Node, Status]: A tuple containing the tree representing the folder 
            structure, and the exit status of the search.
    """

    start_time = time()
    end_time = time() + max_time

    dir_tree = Node(root_folder)
    if max_depth > 0:
        status = getChildren(dir_tree, max_depth, end_time)
    else:
        status = Status.MAX_DEPTH_REACHED
    
    duration = time() - start_time

    # My default stdout is encoded in cp1252, ensure it changes to utf-8 for special characters
    sys.stdout.reconfigure(encoding="utf-8")

    # Output the tree in console
    # print(RenderTree(root)) # Don't use this one, as it doesn't look as nice
    for pre, fill, node in RenderTree(dir_tree):
        print(f"{pre}{node.name}")
    
    print(status)
    if status == Status.MAX_TIME_EXCEEDED:
        print(f"Search stopped after reaching the time limit")
    if status == Status.MAX_DEPTH_REACHED:
        print(f"Search completed down to a tree depth of {max_depth}")


    # Size of a graph is the number of edges (tree order would be the size + 1)
    print(f"Tree size (# of edges): {len(dir_tree.descendants)}")

    print(f"Duration: {duration: .2f} seconds")
        
    return dir_tree, status


def getChildren(node: Node, max_depth: int, end_time: float) -> int:
    path = "/".join([_.name for _ in node.path])
    walk = os.walk(path)
    try:
        # This will throw a StopIteration exception when reaching the end of a branch
        dirpath, dirnames, filenames = next(walk)
    except StopIteration:
        return Status.OK

    status = Status.OK
    for child_dir in dirnames:
        c = Node(child_dir, parent = node)
        if c.depth >= max_depth:
            status = Status.MAX_DEPTH_REACHED
        elif time() > end_time:
            status = Status.MAX_TIME_EXCEEDED
        else:
            temp_status = getChildren(c, max_depth, end_time)
            if status is not Status.MAX_DEPTH_REACHED:
                # Don't overwrite a max depth reached status with an OK status
                status = temp_status

    for child_file in filenames:
        Node(child_file, parent = node)
    
    return status
    


if __name__ == "__main__":
    root_folder = "./test_dir"
    root_folder = "/mnt/c/Users/Hayden/"
    dir_tree = crawlFolderPy(root_folder, max_depth=3, max_time=1)
    pass

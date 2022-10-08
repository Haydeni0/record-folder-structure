#!/usr/bin/env python3

import os
from time import time
from anytree import Node, RenderTree
import sys
from enum import Enum
from typing import Tuple
import argparse


class Status(Enum):
    OK = 0
    MAX_DEPTH_REACHED = 1
    MAX_TIME_EXCEEDED = -1


def crawlFolder(
    root_folder: str, max_depth: int = 3, max_time: float = 1e9, print_tree: bool = False
) -> Tuple[Node, Status]:
    """
    Python serial os.walk based folder crawler.
    Conducts a recursive depth first search (up to a maximum depth) of a folder, returning the folder and filenames in a tree.

    Args:
        root_folder (str): Path to the folder to use as the root of the search
        max_depth (int, optional): Maximum folder depth to search to. Defaults to 3.
        max_time (float, optional): Maximum time in seconds to spend searching. Defaults to 1e9.

    Returns:
        Tuple[anytree.Node, Status]: A tuple containing the tree representing the folder
            structure, and the exit status of the search.
    """

    end_time = time() + max_time

    dir_tree = Node(root_folder)
    if max_depth > 0:
        status = getChildren(dir_tree, max_depth, end_time)
    else:
        status = Status.MAX_DEPTH_REACHED

    # My default stdout is encoded in cp1252, ensure it changes to utf-8 for special characters
    sys.stdout.reconfigure(encoding="utf-8")

    if print_tree:
        # Output the tree in console
        # print(RenderTree(root)) # Don't use this one, as it doesn't look as nice
        for pre, fill, node in RenderTree(dir_tree):
            print(f"{pre}{node.name}")

    return dir_tree, status


def getChildren(node: Node, max_depth: int, end_time: float) -> Status:
    path = "/".join([_.name for _ in node.path])
    walk = os.walk(path)
    try:
        # This will throw a StopIteration exception when reaching the end of a branch
        dirpath, dirnames, filenames = next(walk)
    except StopIteration:
        return Status.OK

    status = Status.OK
    for child_dir in dirnames:
        c = Node(child_dir, parent=node)
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
        Node(child_file, parent=node)

    return status


if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="""
    Python serial os.walk based folder crawler.
    Conducts a recursive depth first search (up to a maximum depth) of a folder, returning the folder and filenames in a tree.
    """)
    parser.add_argument(
        "--root_folder",
        "-f",
        dest="root_folder",
        type=str,
        default=os.path.expanduser("~"),
        help="Path to the folder to use as the root of the search. Defaults to the user home directory.",
    )
    parser.add_argument(
        "--max_depth",
        "-d",
        dest="max_depth",
        type=int,
        default=3,
        help="Maximum folder depth to search to. Defaults to 3.",
    )
    parser.add_argument(
        "--max_time",
        "-t",
        dest="max_time",
        type=int,
        default=1e9,
        help="Maximum time in seconds to spend searching. Defaults to 1e9.",
    )
    parser.add_argument(
        "--print_tree",
        "-p",
        action='store_true', # "store_true" makes the default false
        help="Set true to print the tree. Defaults to False.",
    )

    args = parser.parse_args()
    args = vars(args)
    
    root_folder = args["root_folder"]
    max_depth = args["max_depth"]
    if not os.path.isdir(args["root_folder"]):
        print(f"Error, \"{root_folder}\" is not a valid folder")
        raise
    else:
        print(f"Crawling \"{root_folder}\" to a maximum depth of {max_depth}...")

    # Run the folder crawler
    start_time = time()
    dir_tree, status = crawlFolder(**args)
    duration = time() - start_time

    # Print status message
    if status == Status.MAX_TIME_EXCEEDED:
        print(f"Search stopped after reaching the time limit.")
    if status == Status.MAX_DEPTH_REACHED:
        print(f"Search completed down to a tree depth of {max_depth}.")
    if status == Status.OK:
        print(f"Search completed fully (tree depth never exceeded max depth).")

    # Size of a graph is the number of edges (tree order would be the size + 1)
    print(f"Tree size (# of edges): {len(dir_tree.descendants)}")
    print(f"Duration: {duration: .2f} seconds")

    pass

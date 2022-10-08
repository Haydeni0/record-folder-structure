
## To-do:

- Instead of having each node be a string, make it a class that gives more information about the file or directory
  - This will make it easier to tell if it's a file or a folder, even when reached max depth
- Check cpu vs read speed
- Check size of the tree 
  - Compare to the smallest size it could be (space efficiency) 
    - size of individual strings + pointers in bytes
- Could try in c++ with the [boost graph library](https://www.boost.org/doc/libs/1_70_0/libs/graph/doc/index.html)
- Make this threaded
- Try a different library with a built-in search

---

## Design:

1. Input root folder to search in
2. Input max tree depth to search until
3. Search the root folder for files and folders recursively to the max tree depth
   1. Allow for only recording certain file types, etc.
4. Save the file structure in some format
5. Create an output in an easy to visualise format
   1. E.g. an html document that can be easily clicked through

## Goals:

- Make use of already existing libraries if possible
- Be fast
- Store in a space efficient format
- Be easy to use, maybe implement as a command line utility with ability to pass in options
- Be safe, make sure it has read only permissions

---

## Notes:

- What existing libraries are there
  - What dos/unix commands are there available
    - git grep is really fast, not the same though
  - What libraries are there available in python for fast traversal of directories
  - Can we use something like voidtools everything
    - They use indexing, but maybe we don't need that because we aren't binary searching
  - Bread or depth first-search?
- Do we need a database for storage
- What is the file structure like physically on the disk
  - Are there performance benefits in traversing the directory tree in a certain way 
  - Is this already capitalised on with the library I'm using?
- Can it be parallelised?
  - Are we limited by cpu or read speed?
- Can cache certain things for speed
  - put things
- What format to save in for ease of use and space efficiency
  - Maybe json, or more basic tree structure linked list
  - It will just be text

- Getting a StopIteration exception
  - I think this happens when os.walk hits the bottom of a branch and resets back to the node above






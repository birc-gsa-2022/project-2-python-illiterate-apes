from collections import deque
import st

def LCP(a: str, b: str) -> int:
    """
    Finds the longest common prefix of a and b
    
    returns: 
    If there is no prefix returns 0 otherwise returns length of prefix
    """
    i = 0
    while(i < len(a) and i < len(b)):
        if a[i] != b[i]:
            return i
        i+=1
    return i

def search(root: st.Node, pattern: str, string: str):
    """
    Looks for a pattern in a string using a suffix tree of string.
    """
    #Avoid copies while slicing with memoryviews

    patternView = memoryview(pattern.encode())
    stringView = memoryview(string.encode())

    currNode = root.child
    
    patternProcessed = 0

    #Find pattern (I)
    queue = deque()
    
    while(True):

        prefixLength = LCP(patternView[patternProcessed:], stringView[currNode.start:currNode.end])
        if prefixLength + patternProcessed == len(pattern):
            #Pattern completely Found
            #Report all leafs that are child of currNode (II)
            queue.appendleft(currNode.child)
            while(queue):
                currNode = queue.pop()
                if type(currNode.child) == int:
                    #is leaf, so yield index
                    yield currNode.child
                else:
                    queue.appendleft(currNode.child)
                if currNode.sib:
                    queue.appendleft(currNode.sib)
            return

        elif prefixLength == currNode.end-currNode.start:
            #Proceed to a child of currNode, increase offset with previous edge length
            currNode = currNode.child
            patternProcessed += prefixLength
        else:
            #Match not found
            if currNode.sib:
                currNode = currNode.sib
            else:
                yield -1
                return

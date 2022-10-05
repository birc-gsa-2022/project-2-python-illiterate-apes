from __future__ import annotations
import argparse
from dataclasses import dataclass

@dataclass
class Node:
    start: int
    end: int
    child: Node | None # If end==len(x) then child is is the index
    sib : Node | None

    def __str__(self):
        return f"{self.start},{self.end},{type(self.child)}, {type(self.sib)}"
    
    def __len__(self):
        return self.end-self.start

SENTINEL = "$"

def getAllSuffixes(x):
    for i in range(1, len(x)):
        yield x[i:]+SENTINEL
    yield SENTINEL

def getMatch(x: str, y: str, n: Node, i: int):
    nchild = n.child
    while type(nchild) is Node:
        if x[nchild.start] == y[i]:
            iters = 1
            while nchild.start + iters < nchild.end and x[nchild.start+iters] == y[i+iters]:
                iters += 1
            return iters, nchild
        else:
            nchild = nchild.sib
    return -1, None

def getDifference(str1, str2, i, j, length):
    counter = 0
    while counter < length and i+counter<len(str1) and j+counter<len(str2):
        if str1[i+counter] != str2[j+counter]:
            return counter
        counter += 1
    return -1

def getSuffixTree(x: str):
    suffixes = getAllSuffixes(x)
    x += SENTINEL

    painList = []

    firstLeave = Node(0, len(x), None, None)
    root = Node(0, 0, firstLeave, None)
    painList.append(root)
    painList.append(firstLeave)

    for index, suf in enumerate(suffixes):        
        i = 0
        n = root
        
        while type(n) is Node:
            dif, match = getMatch(x, suf, n, i)
            if dif < 0:
                # Finishes at the node
                newNode = Node(index+i, len(x), index, n.child)
                n.child = newNode
                painList.append(newNode)
                break
            elif dif<match.end-match.start:
                # Finishes at the edge
                newNode = Node(index+i+dif, len(x), index, n.child)
                middleNode = Node(match.start, match.start+dif, newNode, match.sib)
                n.child = middleNode
                
                match.start += dif+1
                match.sib = newNode
                painList.append(newNode)
                painList.append(middleNode)
                break
            else:
                # We are still matching, search in match
                i += match.end-match.start
                n = match
        
    for p in painList:
        print(p)
    return root

def preorder(x, n: Node):
    if type(n) is Node:
        print("Begin",x[n.start: n.end])
        print(x[n.start: n.end])
        child = n.child
        while type(child) is Node:
            preorder(x, child)
            child = child.sib
        print("End",x[n.start: n.end])

        


def main():
    # argparser = argparse.ArgumentParser(
    #     description="Exact matching using a suffix tree")
    # argparser.add_argument("genome", type=argparse.FileType('r'))
    # argparser.add_argument("reads", type=argparse.FileType('r'))
    # args = argparser.parse_args()
    # print(f"Find every reads in {args.reads.name} " +
    #       f"in genome {args.genome.name}")
    
    tree = getSuffixTree("banana")
    #preorder("banana$", tree)


if __name__ == '__main__':
    main()

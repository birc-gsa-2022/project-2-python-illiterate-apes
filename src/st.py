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

SENTINEL = "$"

def getAllSuffixes(x):
    for i in range(1, len(x)):
        yield x[i:]+SENTINEL
    yield SENTINEL

def getMatch(x: str, n: Node, c=SENTINEL):
    nchild = n.child
    while type(nchild) is Node:
        if x[nchild.start] == c:
            return nchild
        else:
            nchild = nchild.sib
    return None

def getDifference(str1, str2, i, j, length):
    counter = 0
    while counter < length and i+counter<len(str1) and j+counter<len(str2):
        if str1[i+counter] != str2[j+counter]:
            return counter
        counter += 1
    return -1

def getSuffixTree(x: str):
    suffixes = getAllSuffixes(x)

    painList = []

    root = Node(0, len(x), None, None)
    painList.append(root)
    x += SENTINEL

    for index, suf in enumerate(suffixes):        
        n = root
        i = 0
        while type(n) is Node:
            match = getMatch(x, n, suf[i])
            if match:
                dif = getDifference(suf, x, i, match.start, match.end-match.start)
                if dif<0:
                    i += match.end-match.start
                    n = match
                    continue
                else:
                    newNode = Node(index+i+dif, len(x), index, n.child)
                    middleNode = Node(match.start, match.start+dif, newNode, match.sib)
                    n.child = middleNode
                    
                    match.start += dif+1
                    match.sib = newNode
                    painList.append(newNode)
                    painList.append(middleNode)
                    break
            else:
                newNode = Node(index+i, len(x), index, n.child)
                n.child = newNode
                painList.append(newNode)
                break
        
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

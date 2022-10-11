from __future__ import annotations
import argparse
from dataclasses import dataclass
import search
import fasta
import fastq
import re

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

def getMatch(x: str, n: Node, i: int):
    nchild = n.child
    while type(nchild) is Node:
        if x[nchild.start] == x[i]:
            iters = 1
            while nchild.start + iters < nchild.end and x[nchild.start+iters] == x[i+iters]:
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

SENTINEL = "$"
def getSuffixTree(x: str):
    x += SENTINEL

    # Create the root and the first leaf
    firstLeaf = Node(0, len(x), 1, None)
    root = Node(0, 0, firstLeaf, None)

    for startSuffix in range(1, len(x)):
        i = 0
        n = root
        
        while type(n) is Node:
            dif, match = getMatch(x, n, i+startSuffix)
            if dif < 0:
                # Finishes at the node
                newNode = Node(startSuffix+i, len(x), startSuffix+1, n.child)
                n.child = newNode
                break
            elif dif<len(match):
                # Finishes at the edge
                middleNode = Node(match.start, match.start+dif, None, match.sib)
                newNode = Node(startSuffix+i+dif, len(x), startSuffix+1, match)

                middleNode.child = newNode

                match.start += dif
                match.sib = None

                # Look for the sibling that points to the match node
                prevSib = n.child
                if prevSib == match:
                    n.child = middleNode
                else:
                    while prevSib.sib != match:
                        prevSib = prevSib.sib
                
                    prevSib.sib = middleNode

                break
            else:
                # We are still matching, search in match
                i += match.end-match.start
                n = match
    
    #preorder(x, root)
    return root

def preorder_r(x: str, n: Node, depth: int):
    if type(n) is Node:
        print("\t"*depth, end="")
        if len(n) > 0:
            print(x[n.start: n.end], end="")
        else:
            print(end="-")
        child = n.child
        if type(child) is int:
            print("",child)
        else:
            print()
            while type(child) is Node:
                preorder_r(x, child, depth+1)
                child = child.sib

def preorder(x: str, n: Node):
    print("Tree representation:")
    preorder_r(x, n, 0)

def getTrailingNumber(s):
    m = re.search(r'\d+$', s)
    return (s[:m.start()], int(s[m.start():]))

def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using a suffix tree")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()
    genomes = fasta.fasta_parse(args.genome)
    reads = fastq.fastq_parser(args.reads)

    out = []

    for g in genomes:
        tree = getSuffixTree(g[1])
        string = memoryview(g[1].encode())
        for r in reads:
            length = len(r[1])
            if length == 0:
                continue
            for m in search.search(tree, r[1], string):
                out.append((getTrailingNumber(r[0]), getTrailingNumber(g[0]), m, length, r[1]))

    for t in sorted(out, key=lambda x: (x[0], x[1], x[2])):
        print(f"{t[0][0]}{t[0][1]}\t{t[1][0]}{t[1][1]}\t{t[2]}\t{t[3]}M\t{t[4]}")


if __name__ == '__main__':
    main()

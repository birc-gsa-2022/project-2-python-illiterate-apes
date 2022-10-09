import matplotlib.pyplot as plt
import numpy as np
import search
import st
import timeit



 


def main():
    
    
    #Construction

    #Worst Case
    string = "a"*10
    runtimes = runtimeConstruction(string)
    x = np.array([i[0] for i in runtimes])
    y = np.array([i[1] for i in runtimes])
    plt.title("naive suffix tree construction algorithm")
    plt.xlabel("string length")
    plt.ylabel("Runtime")
    plt.plot(x,y)
    plt.show()

    #Search
    
    #Worst Case
    string = "a"*1000
    runtimes = runtimeSearch(string, "a")
    x = np.array([i[0] + i[1] for i in runtimes])
    y = np.array([i[2] for i in runtimes])
    plt.title("suffix tree search algorithm")
    plt.xlabel("pattern length + Number of Occurrences")
    plt.ylabel("Runtime")
    plt.plot(x,y)
    plt.show()



def runtimeConstruction(string: str):
    """
    measures runtimes for suffix tree construction
    """
    runtimes = []
    

    for i in range(1,20):
        start = timeit.default_timer()
        st.getSuffixTree(string*i)
        stop = timeit.default_timer()
        runtimes.append([len(string*i), stop - start])

    
    return runtimes

def runtimeSearch(string: str, pattern: str):
    """
    measures runtimes for suffix tree search
    """
    runtimes = []
    
    tree = st.getSuffixTree(string)
    string = memoryview(str(string).encode())
    for i in range(0,20):
        z = 0
        start = timeit.default_timer()
        for match in search.search(tree,pattern * i, string):
                z += 1
        stop = timeit.default_timer()
        runtimes.append([len(pattern*i), z, stop - start])

    
    return runtimes




if __name__ == "__main__":
    main()
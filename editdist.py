import sys
import numpy as np

"""Edit distance implementation"""

__author__=="Karolina Alexiou"
__email__=="carolinegr@gmail.com"

BOTH = 0
SKIP_B = 1
SKIP_A = 2

GAP="_"
MISMATCH="'"

def edit_dist(a,b):
    la = len(a)
    lb = len(b)
    # matrix to keep the cost of each step
    M = np.zeros([la+1, lb+1])
    # dictionary to keep the next step ie, chosen[(posi,posj)] = (newi,newj, hop_type)
    chosen = {}
    for i in range(lb):
        M[la][i] = lb -i 
    for i in range(la):
        M[i][lb] = la -i 

    for i in reversed(range(la)):
        for j in reversed(range(lb)):
            eq = a[i]==b[j]
            choices = [int(not eq) + M[i+1][j+1], 1+ M[i][j+1], 1 + M[i+1][j] ]
            next_hops = [(i+1, j+1, BOTH),(i,j+1, SKIP_B),(i+1,j, SKIP_A)]
            M[i][j] = np.min(choices)
            chosen[(i,j)] = next_hops[np.argmin(choices)]

    result = M[0][0]

    starti, startj, choice = chosen[(0,0)]
    sa = ""
    sb = ""
    while True:
        if choice == BOTH: # getting ai, bj
            sa+=a[starti]
            sb+=b[startj]
            if a[starti]!=b[startj]:
                sa+=MISMATCH
                sb+=MISMATCH
        if choice == SKIP_B: # skipping b[j] at a[i]
            sa+=GAP
            sb+=b[startj]

        if choice == SKIP_A: # skipping a[i] at b[j]
            sb+=GAP
            sa+=a[starti]
        starti, startj, choice = chosen[(starti,startj)]

        if startj==lb or starti==la:
            if startj<lb:
                sa+= GAP*(lb-startj)
                sb+=b[startj:]
            if starti<la:
                sb+= GAP*(la-starti)
                sa+=a[starti:]
            break

    print sa
    print sb   
    return result

if __name__=="__main__":
    assert(edit_dist("ice","iceds")==2)
    assert(edit_dist("Karoline","Carolin")==2)
    assert(edit_dist("paras","parasect")==3)
    assert(edit_dist("a pikachu","pica")==6)
    assert(edit_dist("paradise","dices")==6)
    assert(edit_dist("paradises","dice")==6)
    assert(edit_dist("i want ice cream","she wants ice")==10)
    print edit_dist(sys.argv[1],sys.argv[2])





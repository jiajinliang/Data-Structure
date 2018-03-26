#!/usr/bin/env python3
'''
Grading script for PA1 (BST)
Niema Moshiri 2017
'''
from subprocess import check_output,CalledProcessError
from os.path import isfile
from random import choice,randint,sample,shuffle

# global constants
KILL_TIME = 9 # kill execution if it takes more than 10 seconds
NUMWORDS = 10000 # number of words in big random dataset
LENWORD  = 100  # length of each word in big random dataset
SIZE_P = "+1 for correct size"
SIZE_F = "+0 for incorrect size"
HEIGHT_P = "+1 for correct height"
HEIGHT_F = "+0 for incorrect height"
EXIST_P = "+1 for finding existant element"
EXIST_F = "+0 for failing to find existant element"
NONEXIST_P = "+1 for not finding non-existant element"
NONEXIST_F = "+0 for 'finding' non-existant element"
MEMLEAK_P = "+1 for no memory leaks"
MEMLEAK_F = "+0 for memory leaks"


# build BST given strings
class Node:
    def __init__(self,word):
        self.word = word; self.left = None; self.right = None
def bst(words):
    root = None; n = 0; h = 0
    for word in words:
        if root is None:
            root = Node(word); n = 1
            continue
        curr = root; currH = 1
        while True:
            currH += 1
            if word < curr.word:
                if curr.left is None:
                    curr.left = Node(word); n += 1
                    if currH > h:
                        h = currH
                    break
                else:
                    curr = curr.left
            elif word > curr.word:
                if curr.right is None:
                    curr.right = Node(word); n += 1
                    if currH > h:
                        h = currH
                    break
                else:
                    curr = curr.right
            else:
                break
    return root,n,h

def test_simple_left_unbalanced(recursiveDepth=1):
    score = 0
    try:
        command = "timeout {}s ./main test.txt".format(KILL_TIME)
        o = check_output(command.split(), 
                         input=b"MOSHIRI, NIEMA\ny\nOSUNA, ERIC\nn\n")
        o = o.decode().lower().splitlines()
        if len(o) > 0 and o[0].strip() == 'Size of tree: 3'.lower():
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
        if len(o) > 1 and o[1].strip() == 'Height of tree: 3'.lower():
            print(HEIGHT_P); score += 1
        else:
            print(HEIGHT_F)
        if len(o) > 3 and o[3].strip() == 'MOSHIRI, NIEMA found!'.lower():
            print(EXIST_P); score += 1
        else:
            print(EXIST_F)
        if len(o) > 6 and o[6].strip() == 'OSUNA, ERIC NOT found'.lower():
            print(NONEXIST_P); score += 1
        else:
            print(NONEXIST_F)
    except CalledProcessError as error:
        if error.returncode == 124:
            if recursiveDepth == 1:
                print("Operation timed out. Reattempting")
                return test_simple_left_unbalanced(recursiveDepth + 1)
            else:
                print(("Your program took longer than %d seconds when " + 
                       "running the simple left-balanced tree test. " + 
                       "0 points") % KILL_TIME)
        else:
            print("Your program crashed when running the simple " +
                  "left-balanced tree test. 0 points")
    return score

def test_simple_right_unbalanced(recursiveDepth=1):
    score = 0
    try:
        command = "timeout {}s ./main test.txt".format(KILL_TIME)
        o = check_output(command.split(), 
                         input=b"MICALLEF, RYAN\ny\nOSUNA, ERIC\nn\n")
        o = o.decode().lower().splitlines()
        if len(o) > 0 and o[0].strip() == 'Size of tree: 4'.lower():
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
        if len(o) > 1 and o[1].strip() == 'Height of tree: 4'.lower():
            print(HEIGHT_P); score += 1
        else:
            print(HEIGHT_F)
        if len(o) > 3 and o[3].strip() == 'MICALLEF, RYAN NOT found'.lower():
            print(NONEXIST_P); score += 1
        else:
            print(NONEXIST_F)
        if len(o) > 6 and o[6].strip() == 'OSUNA, ERIC found!'.lower():
            print(EXIST_P); score += 1
        else:
            print(EXIST_F)
    except CalledProcessError as error:
        if error.returncode == 124:
            if recursiveDepth == 1:
                print("Operation timed out. Reattempting")
                return test_simple_right_unbalanced(recursiveDepth + 1)
            else:
                print(("Your program took longer than %d seconds when " + 
                       "running the simple rightt-balanced tree test. " + 
                       "0 points") % KILL_TIME)
        else:
            print("Your program crashed when running the simple test. 0 points")
    return score

def test_large_and_random(queries, words, words_set, recursiveDepth=1):
    score = 0
    try:
        command = "timeout {}s ./main test.txt".format(KILL_TIME)
        std_input = ("%s\ny\n%s\ny\n%s\ny\n%s\ny\n%s\ny\n%s\ny\n%s\ny\n%s\nn\n" 
                     % tuple(queries)).encode('ascii')
        o = check_output(command.split(), input=std_input)
        o = o.decode().lower().splitlines()
        root,n,h = bst(words)
        if len(o) > 0 and o[0].strip() == ("Size of tree: %d" % n).lower():
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
        if len(o) > 1  and o[1].strip() == ("Height of tree: %d" % h).lower():
            print(HEIGHT_P); score += 1
        else:
            print(HEIGHT_F)
        for i in range(3, len(o), 3):
            if int(i/3)-1 >= len(queries):
                print("Invalid program output. 0 points")
                continue
            query = queries[int(i/3)-1]
            if query in words_set:
                if o[i] == ("%s found!" % query).lower():
                    print(EXIST_P); score += 1
                else:
                    print(EXIST_F)
            else:
                if o[i] == ("%s NOT found" % query).lower():
                    print(NONEXIST_P); score += 1
                else:
                    print(NONEXIST_F)
        command = ("timeout {}s valgrind --log-fd=1 --leak-check=yes " +
                  "./main test.txt").format(KILL_TIME)
        o = check_output(command.split(), input=b"n\nn\n").decode()
        if "no leaks are possible" in o or ("definitely lost: 0 bytes" in o and 
                                            "indirectly lost: 0 bytes" in o):
            print(MEMLEAK_P); score += 1
        else:
            print(MEMLEAK_F)
    except CalledProcessError as error:
        if error.returncode == 124:
            if recursiveDepth == 1:
                print("Operation timed out. Reattempting")
                return test_large_and_random(queries, words, words_set, 
                                             recursiveDepth + 1)
            else:
                print(("Your program took longer than %d seconds when " + 
                       "running the large randomly-generated test. " + 
                       "0 points") % KILL_TIME)
        else:
            print("Your program crashed when running the large " +
                  "randomly-generated test. 0 points")
    return score


def test_empty_and_inorder(ints, recursiveDepth=1):
    score = 0
    try:
        check_output("g++ -g -Wall -std=c++11 -o test test.cpp".split())
        comp = True
    except CalledProcessError:
        print("Unable to compile tester for 'empty' and 'inorder', " + 
              "so 0 points will be awarded for those two")
        comp = False
    if comp:
        try:
            command = "timeout {}s ./test".format(KILL_TIME)
            lines = check_output(command.split()).decode().splitlines()
            l1 = lines[0]
            if len(lines) > 1:
                l2 = lines[1]
            else:
                l2 = ''
            if l1.strip() == '1':
                print("+1 for working 'empty' function"); score += 1
            else:
                print("+0 for non-working 'empty' function")
            if [float(i) for i in l2.split()] == sorted(ints):
                print("+1 for working 'inorder' function"); score += 1
            else:
                print("+0 for non-working 'inorder' function")
        except CalledProcessError as error:
            if error.returncode == 124:
                if recursiveDepth == 1:
                    print("Operation timed out. Reattempting")
                    return test_empty_and_inorder(ints, recursiveDepth + 1)
                else:
                    print(("Your program took longer than %d seconds when run" +
                           "ning 'empty' and 'inorder'. 0 points") % KILL_TIME)
            else:
                print("Unable to run tester for 'empty' and 'inorder', " +
                      "so 0 points will be awarded for those two")
    return score



# grade PA1
def grade():
    score = 0 # total possible = 22 (+1 for academic integrity, +2 for style)
    pos = 0

    # check if code can compile
    print("Checking if code compiles:")
    pos += 1
    try:
        check_output("make clean".split())
        check_output("rm -f main".split())
        check_output("make test_bst main".split())
        if not isfile("main"):
            print("Failed to compile using 'make' command. 0 points")
            exit()
        print("+1 for code compiling"); score += 1
    except CalledProcessError:
        print("Failed to compile using 'make' command. 0 points")
        exit()
    print()

    # simple sorted descending dataset
    print("Running simple left-unbalanced tree test:")
    f = open('test.txt','w')
    f.write("MOSHIRI, NIEMA\nMICALLEF, RYAN\nGARCIA, FELIX\nMOSHIRI, NIEMA")
    f.close()
    pos += 4
    score += test_simple_left_unbalanced()
    print()

    # simple sorted ascending dataset
    print("Running simple right-unbalanced tree test:")
    f = open('test.txt','w')
    f.write("GARCIA, FELIX\nMICALLEF, STEVE\nMOSHIRI, NIEMA\nOSUNA, ERIC")
    f.close()
    pos += 4
    score += test_simple_right_unbalanced()
    
    print()

    # big random dataset
    print("Running large randomly-generated test:")
    words = [''.join([choice('ACGT') for i in range(LENWORD)]) for _ in range(NUMWORDS)]
    words_set = set(words)
    f = open('test.txt','w')
    f.write('\n'.join(words))
    f.close()
    queries = sample(words_set,4) + [''.join([choice('ACGT') for i in range(LENWORD)]) for _ in range(4)] # query some words that are and are not in the BST
    shuffle(queries)
    pos += 3+len(queries)
    score += test_large_and_random(queries, words, words_set)
    
    print()

    # test empty and inorder
    print("Testing 'empty' and 'inorder' functions:")
    ints = set()
    while len(ints) < 5:
        ints.add(randint(100,1000))
    insert = "bst.insert(%d); bst.insert(%d); bst.insert(%d); bst.insert(%d); bst.insert(%d);" % tuple(ints)
    cpp = '#include "BST.hpp"\nusing namespace std;\nint main(int argc, char* argv[]) {\n  bool empty = true; BST<int> bst;\n  if(!bst.empty()) { empty = false; }\n  %s\n  if(bst.empty()) { empty = false; }\n  cout << empty << endl;\n  for(BST<int>::iterator it = bst.begin(); it != bst.end(); ++it) { cout << *it << " "; }\n}' % insert
    f = open('test.cpp','w')
    f.write(cpp)
    f.close()
    pos += 2
    
    score += test_empty_and_inorder(ints)
    print()
    print()

    # clean up at the end
    print("Total Score: %d/%d" % (score,pos))
    check_output("rm test test.txt test.cpp".split())
    check_output("make clean".split())

# main function: call grader
if __name__ == "__main__":
    grade()

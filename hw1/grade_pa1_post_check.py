#!/usr/bin/env python3
'''
Grading script for PA1 (BST)
Niema Moshiri 2017
Modified by Dylan McNamara 2018
'''
from subprocess import check_output,CalledProcessError
from os.path import isfile
from random import choice,randint,sample,shuffle

# global constants
KILL_TIME = 9  # kill execution if it takes more than this number in seconds
NUMWORDS = 10000  # number of words in big random dataset
LENWORD  = 100  # length of each word in big andom dataset
SIZE_P = "+1 for correct size"
SIZE_F = "+0 for incorrect size"
HEIGHT_P = "+1 for correct height"
HEIGHT_F = "+0 for incorrect height"
NEAREST_NEIGHBOR_P = "+1 for finding nearest neighbor point"
NEAREST_NEIGHBOR_F = "+0 for failing to find nearest neighbor"
MEMLEAK_P = "+1 for no memory leaks"
MEMLEAK_F = "+0 for memory leaks"


# Test methods
def test_distance(recursiveDepth=1):
    score = 0
    pos = 2
    test_cases = [((0, 0), (100, 100)), ((100, 100), (0, 0)), 
                  ((0, 0), (-100, -100)), ((-100, -100), (0, 0)),
                  ((0, 0), (0, 0)), ((-1.5, -3.2), (4.2, 9.1)),
                  ((2.3, -4.1), (-8.7, 6.8)), ((1.5, 3.2), (4.2, 9.1))]
    solutions = [20000, 20000, 20000, 20000, 0, 183.78, 239.81, 42.1]
    content = ""
    for case in test_cases:
        point1 = case[0]
        point2 = case[1]
        content += \
        """
            dist = Point::squareDistance(Point({}, {}), Point({}, {}));
            cout << dist << endl;
            
        """.format(point1[0], point1[1], point2[0], point2[1])

    cpp = \
        """
        #include <iostream>
        #include "KDT.hpp"
        using namespace std;
        int main(int argc, char ** argv) {{
        double dist;
        {}
        }}
        """.format(content)
    f = open("test.cpp", "wt")
    f.write(cpp)
    f.close()

    try:
        check_output("g++ -g -Wall -std=c++11 -o test test.cpp".split())
        comp = True
    except CalledProcessError:
        print("Unable to compile tester for 'empty' and 'inorder', " + 
              "so 0 points will be awarded for those two")
        comp = False
    try:
        command = "timeout {}s ./test".format(KILL_TIME)
        o = check_output(command.split())
        o = o.decode().lower().splitlines()
        num_correct = 0
        for index in range(len(solutions)):
            if (o[index] == str(solutions[index])):
                num_correct += 1
        if (num_correct >= len(solutions) / 2):
            print("+1 for mostly correct squareDistance function")
            score += 1
        else:
            print("+0 for mostly incorrect squareDistance function")
        if (num_correct == len(solutions)):
            print("+1 for correct squareDistance function")
            score += 1
        else: 
            print("+0 for incorrect squareDistance function")


    except CalledProcessError as error:
        if error.returncode == 124:
            if recursiveDepth == 1:
                print("Operation timed out. Reattempting")
                return test_distance(recursiveDepth + 1)
            else:
                print(("Your program took longer than %d seconds when " + 
                       "running the distance test. 0 points") % KILL_TIME)
        else:
            print("Your program crashed when running the distance test. " +
                  "0 points")
    return score, pos


def test_small_tree(recursiveDepth=1):
    score = 0
    pos = 4
    
    test_points = [(4, 5), (0, 2), (-1, 50), (5, 12), (6, 9), (5, 15), (3, 27)]
    query_points = [(3, 9), (4.5, 5), (100, 100), (6, 13), (0, 2), (3, 27)]
    solutions = [(6, 9), (4, 5), (-1, 50), (5, 12), (0, 2), (3, 27)]

    # Write test points to text file test.txt
    test_points = ["{} {}".format(point[0], point[1]) for point in test_points]
    test_file_content = "\n".join(test_points)
    f = open("test.txt", "wt")
    f.write(test_file_content)
    f.close()

    try:
        points = ["{} {}".format(point[0], point[1]) for point in query_points]
        # std_input = b("\ny\n".join(points) + "\nn\n")   # this doesn't work
        std_input = bytearray("\ny\n".join(points) + "\nn\n", "utf-8")
        command = "timeout {}s ./main2 test.txt".format(KILL_TIME)
        o = check_output(command.split(), input=std_input)
        o = o.decode().lower().splitlines()
        num_correct = 0

        # Check the results with the set of solution points
        for solution_index in range(len(solutions)):
            o_index = 3 * solution_index + 3
            if len(o) <= o_index:
                break
            solution = str(solutions[solution_index])
            if ("nearest point in tree: " + solution == o[o_index]):
                num_correct += 1

        if len(o) > 0 and o[0].strip() == 'Size of tree: 7'.lower():
            print(SIZE_P); 
            score += 1
        else:
            print(SIZE_F)

        if len(o) > 1 and o[1].strip() == 'Height of tree: 3'.lower():
            print(HEIGHT_P); 
            score += 1
        else:
            print(HEIGHT_F)

        if (num_correct >= len(solutions) / 2):
            print(NEAREST_NEIGHBOR_P)
            score += 1
        else:
            print(NEAREST_NEIGHBOR_F)
        if (num_correct == len(solutions)):
            print(NEAREST_NEIGHBOR_P)
            score += 1
        else:
            print(NEAREST_NEIGHBOR_F)
        
    except CalledProcessError as error:
        if error.returncode == 124:
            if recursiveDepth == 1:
                print("Operation timed out. Reattempting")
                return test_small_tree(recursiveDepth + 1)
            else:
                print(("Your program took longer than %d seconds when " + 
                       "running the simple left-balanced tree test. " + 
                       "0 points") % KILL_TIME)
        else:
            print("Your program crashed when running the simple " +
                  "left-balanced tree test. 0 points")
    return score, pos


def test_large_and_random(recursiveDepth=1):
    score = 0
    LARGE_TEST_POINT_VALUE = 7
    pos = 2 + 1 + LARGE_TEST_POINT_VALUE
    try:
        command = "timeout {}s ./main2 test_points.txt".format(KILL_TIME)
        input_points_file = open("queryPoints.txt", "r") 
        input_points = [line for line in input_points_file]

        solutions_file = open("solutionPoints.txt", "r") 
        solutions = ["({}, {})".format(line.split()[0], line.split()[1]) 
                            for line in solutions_file]

        std_input = bytearray("\ny\n".join(input_points) + "\nn\n", "utf-8")
        o = check_output(command.split(), input=std_input)
        o = o.decode().lower().splitlines()
        n = 1000
        h = 10

        if len(o) > 0 and o[0].strip() == ("Size of tree: %d" % n).lower():
            print(SIZE_P); score += 1
        else:
            print(SIZE_F)
        if len(o) > 1  and o[1].strip() == ("Height of tree: %d" % h).lower():
            print(HEIGHT_P); score += 1
        else:
            print(HEIGHT_F)

        # Check the results with the set of solution points
        num_correct = 0
        for solution_index in range(len(solutions)):
            o_index = 3 * solution_index + 3
            if len(o) <= o_index:
                break
            solution = solutions[solution_index]
            if ("nearest point in tree: " + solution == o[o_index]):
                num_correct += 1

        score_step = len(solutions) // LARGE_TEST_POINT_VALUE
        for test_count in range(LARGE_TEST_POINT_VALUE - 1):
            if num_correct > test_count * score_step:
                print(NEAREST_NEIGHBOR_P)
                score += 1
            else:
                print(NEAREST_NEIGHBOR_F)
        if num_correct == len(solutions):
            print(NEAREST_NEIGHBOR_P)
            score += 1
        else:
            print(NEAREST_NEIGHBOR_F)

        # check for memory leaks
        command = ("timeout {}s valgrind --log-fd=1 --leak-check=yes " +
                   "./main2 test.txt").format(KILL_TIME)
        o = check_output(command.split(), input=b"0 0\nn\n").decode()
        if "no leaks are possible" in o or ("definitely lost: 0 bytes" in o and 
                                            "indirectly lost: 0 bytes" in o):
            print(MEMLEAK_P); score += 1
        else:
            print(MEMLEAK_F)

    except CalledProcessError as error:
        if error.returncode == 124:
            if recursiveDepth == 1:
                print("Operation timed out. Reattempting")
                return test_large_and_random(recursiveDepth + 1)
            else:
                print(("Your program took longer than %d seconds when " + 
                       "running the large randomly-generated test. " + 
                       "0 points") % KILL_TIME)
        else:
            print("Your program crashed when running the large " +
                  "randomly-generated test. 0 points")
    return score, pos


def test_empty(recursiveDepth=1):
    score = 0
    pos = 3
    f = open("test.txt", "wt")
    f.close()

    # Write test points to text file test.txt
    cpp = \
    """
    #include <iostream>
    #include "KDT.hpp"

    using namespace std;

    int main(int argc, char ** argv) {
        KDT tree; 
        vector<Point> points;
        
        tree.build(points);
        cout << "Size of tree: " << tree.size() << endl;
        cout << "Height of tree: " << tree.height() << endl;

        vector<Point> test_cases;
        test_cases.push_back(Point());
        test_cases.push_back(Point(-1, -1));
        test_cases.push_back(Point(2, 3));
        test_cases.push_back(Point(2000, -3000));
        test_cases.push_back(Point(-23.5692, 34.762));

        vector<Point>::iterator vit = test_cases.begin();
        for (; vit != test_cases.end(); vit++) {
            BST<Point>::iterator result = tree.findNearestNeighbor(*vit);

            if (result != tree.end()) {
                cout << "Fail" << endl;
                break;
            }
        }

        if (!tree.empty()) {
            cout << "Fail" << endl;
        }
        tree.build(test_cases);
        if (tree.empty()) {
            cout << "Fail" << endl;
        }
        return 0;
    }
        
    """

    f = open('test.cpp','w')
    f.write(cpp)
    f.close()


    try:
        check_output("g++ -g -Wall -std=c++11 -o test test.cpp".split())
        comp = True
    except CalledProcessError:
        print("Unable to compile tester for 'empty', " + 
              "so 0 points will be awarded")
        comp = False
    if comp:
        try:
            command = "timeout {}s ./test".format(KILL_TIME)
            o = check_output(command.split())
            o = o.decode().lower().splitlines()
            num_correct = 0

            # Check the results with the set of solution points
            if len(o) > 0 and o[0].strip() == 'Size of tree: 0'.lower():
                print(SIZE_P); 
                score += 1
            else:
                print(SIZE_F)

            if len(o) > 1 and o[1].strip() == 'Height of tree: 0'.lower():
                print(HEIGHT_P); 
                score += 1
            else:
                print(HEIGHT_F)

            if ("Fail".lower() in o or len(o) > 2):
                print("+0 for incorrect empty function")
            else:
                print("+1 for working empty function")
                score += 1
            
        except CalledProcessError as error:
            if error.returncode == 124:
                if recursiveDepth == 1:
                    print("Operation timed out. Reattempting")
                    return test_empty(recursiveDepth + 1)
                else:
                    print(("Your program took longer than %d seconds when " + 
                           "running the empty tree test. " + 
                           "0 points") % KILL_TIME)
            else:
                print("Your program crashed when running the " +
                      "empty tree test. 0 points")
    return score, pos


def test_inorder_and_build(recursiveDepth=1):
    score = 0
    pos = 3
    numbers = [i for i in range(randint(100, 110))]
    shuffle(numbers)
    test_points = [(numbers[i], numbers[i+1])
                   for i in range(0, len(numbers)-1, 2)]
    #test_points = [(4, 5), (0, 2), (-1, 50), (5, 12), (6, 9), (5, 15), (3, 27)]
    results = []
    try:
        for i in range(10):
            shuffle(test_points)
            insert = ""
            for point in test_points:
                insert += "\t\tpoints.push_back(Point{});\n".format(point)
            cpp = \
            """
            #include <iostream>
            #include "KDT.hpp"

            using namespace std;

            int main(int argc, char* argv[]) {{
                KDT tree;
                vector<Point> points;
                {}
                tree.build(points);
                tree.inorder();
            }}
            """.format(insert)
            f = open('test.cpp','w')
            f.write(cpp)
            f.close()

            try:
                check_output("g++ -g -Wall -std=c++11 -o test test.cpp".split())
                comp = True
            except CalledProcessError:
                print("Unable to compile tester for 'empty' and 'inorder', " + 
                      "so 0 points will be awarded for those two")
                break
            if comp:
                command = "timeout {}s ./test".format(KILL_TIME)
                lines = check_output(command.split()).decode().splitlines()
                results.append(lines)

        correct_result_length = [len(result) == len(test_points) 
                                 for result in results]
        if all(correct_result_length):
            print("+1 for correct number of elements printed")
            score += 1
        else:
            print("+0 for incorrect number of elements printed")

        equivalent_to_neighbor = [results[index] ==
                                  results[(index + 1) % len(results)]
                                  for index in range(len(results))]
        if all(equivalent_to_neighbor):
            print("+1 for equivalent build->inorder results")
            score += 1
        else:
            print("+0 for changing build->inorder")

        exists = [(str(point) in results[0]) for point in test_points]
        if all(exists):
            print("+1 for all points existing in the tree")
            score += 1
        else:
            print("+0 for missing points in the kd tree")


    except CalledProcessError as error:
        if error.returncode == 124:
            if recursiveDepth == 1:
                print("Operation timed out. Reattempting")
                return test_inorder_and_build(recursiveDepth + 1)
            else:
                print(("Your program took longer than %d seconds when run" +
                       "ning 'inorder' and 'build'. 0 points") % KILL_TIME)
        else:
            print("Unable to run tester for 'inorder' and 'build', " +
                  "so 0 points will be awarded for those two")
    return score, pos


# grade PA1 post checkpoint submission
def grade():
    score = 0 # total possible = 22 (+1 for academic integrity, +2 for style)
    pos = 0

    # check if code can compile
    print("Checking if code compiles:")
    pos += 1
    try:
        check_output("make clean".split())
        check_output("rm -f main2".split())
        check_output("make test_kdt main2".split())
        if not isfile("main2"):
            print("Failed to compile using 'make' command. 0 points")
            exit()
        print("+1 for code compiling"); score += 1
    except CalledProcessError:
        print("Failed to compile using 'make' command. 0 points")
        exit()
    print()

    print("Running square distance test:")
    score_increase, pos_increase = test_distance()
    score += score_increase
    pos += pos_increase
    print()

    # test empty 
    print("Testing 'empty' function:")
    score_increase, pos_increase = test_empty()
    score += score_increase
    pos += pos_increase
    print()

    # test inorder, and build
    print("Testing 'inorder' and 'build' functions:")
    score_increase, pos_increase = test_inorder_and_build()
    score += score_increase
    pos += pos_increase
    print()

    # simple small tree
    print("Running simple kdtree test (requires main2):")
    score_increase, pos_increase = test_small_tree()
    score += score_increase
    pos += pos_increase
    print()

    # big random dataset
    print("Running large randomly-generated test (requires main2):")
    score_increase, pos_increase = test_large_and_random()
    score += score_increase
    pos += pos_increase
    print()

    """
    print("Running memory leak test:")
    score_increase, pos_increase = test_memory_leaks()
    score += score_increase
    pos += pos_increase
    print()
    """

    print()

    # clean up at the end
    print("Total Score: %d/%d" % (score,pos))
    check_output("rm test test.txt test.cpp".split())
    check_output("make clean".split())


# main function: call grader
if __name__ == "__main__":
    grade()

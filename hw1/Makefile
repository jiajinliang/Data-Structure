# A simple makefile for CSE 100 P1

#use g++ for everything
CC= g++  	

# include debugging symbols in object files,
# and enable all warnings
CXXFLAGS= -g -Wall -std=c++11

#include debugging symbols in executable
LDFLAGS= -g	

default: test_bst main test_kdt main2

test_bst: test_BST.o 
	g++ -o test_bst test_BST.o
main: main.o
	g++ -o main main.o
main2: main2.o
	g++ -o main2 main2.o
test_kdt: test_KDT.o
	g++ -o test_kdt test_KDT.o

main.o: BST.hpp BSTNode.hpp BSTIterator.hpp 
main2.o: KDT.hpp BST.hpp BSTNode.hpp BSTIterator.hpp 
test_BST.o: BST.hpp BSTNode.hpp BSTIterator.hpp 
test_KDT.o: KDT.hpp BST.hpp BSTNode.hpp BSTIterator.hpp 

clean:
	$(RM) main test_bst test_kdt main2 *.o

# A simple makefile for CSE 100 PA4

CC=g++
CXXFLAGS=-std=c++11
LDFLAGS=

# if passed "type=opt" at command-line, compile with "-O3" flag
# (otherwise use "-g" for debugging)

ifeq ($(type),opt)
    CPPFLAGS += -O3
    LDFLAGS += -O3
else
    CPPFLAGS +=-g
    LDFLAGS +=-g
endif

all: pathfinder linkpredictor awardsceremony



# include whatever source code *.hpp files pathfinder relies on
# (these are merely the ones that were used in the solution)

pathfinder: clean ActorGraph.o pathfinder.o
	$(CC) $(CXXFLAGS) -o pathfinder -g pathfinder.o ActorGraph.o

pathfinder.o: pathfinder.cpp

ActorGraph.o: ActorGraph.cpp ActorGraph.hpp

# include what ever source code *.hpp files ActorGraph relies on
# (these are merely the ones that were used in the solution)

# Note: you do not have to include a *.cpp file if it aleady has a paired *.hpp
# file that is already included with class/method headers


clean:
	rm -f pathfinder *.o core*


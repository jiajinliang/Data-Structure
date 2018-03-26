# A simple makefile for CSE 100 PA4


CC=g++
CXXFLAGS=-std=c++11
LDFLAGS=

# if passed "type=opt" at command-line, compile with "-O3" flag
# (otherwise use "-g" for debugging)

ifeq ($(type),db)
    CPPFLAGS +=-g
    LDFLAGS +=-g
else
    CPPFLAGS += -O3
    LDFLAGS += -O3
endif

all: pathfinder linkpredictor awardsceremony



# include whatever source code *.hpp files pathfinder relies on
# (these are merely the ones that were used in the solution)

pathfinder: ActorGraph.o pathfinder.o
	$(CC) $(CXXFLAGS) -o pathfinder $(CPPFLAGS) pathfinder.o ActorGraph.o
pathfinder.o: pathfinder.cpp

linkpredictor: ActorGraph.o linkpredictor.o
	$(CC) $(CXXFLAGS) -o linkpredictor $(CPPFLAGS) linkpredictor.o ActorGraph.o
linkpredictor.o: linkpredictor.cpp

awardsceremony: ActorGraph.o awardsceremony.o
	$(CC) $(CXXFLAGS) -o awardsceremony $(CPPFLAGS) awardsceremony.o ActorGraph.o
awardsceremony.o: awardsceremony.cpp

ActorGraph.o: ActorGraph.cpp ActorGraph.hpp

# include what ever source code *.hpp files ActorGraph relies on
# (these are merely the ones that were used in the solution)

# Note: you do not have to include a *.cpp file if it aleady has a paired *.hpp
# file that is already included with class/method headers


clean:
	rm -f pathfinder linkpredictor *.o core*

backup: *.cpp *.hpp Makefile
	cp *.cpp *.hpp Makefile ../../PA_Backup/pa3/

restore: *.cpp *.hpp Makefile
	cp ../../PA_Backup/pa3/* .

update:	*.cpp *.hpp Makefile
	scp *.cpp *.hpp Makefile til253@ieng6.ucsd.edu:~/../../../cs100w/til253/pa3/

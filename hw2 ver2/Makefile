# A starter makefile for CSE 100 P2
# I believe this make file works. However, my make knowledge is not very good,
# so this file doesn't exhibit all best practices
# Areas for improvement:
# - CXX, CXXFLAGS and LDFLAGS might be special variable names. Possibly we don't need to explicitly use them on each line?
# - we're compiling all the .hpp files in addition to the .cpp files. We do this because we've put lots of code in them.
#   However, that's not good practice - it's best to leave the code in .cpp files. Because we're compiling .hpp files,
#   we're creating unnecessary build artifacts and slowing down the builds minorly.
# - I believe there is syntax that can condense all the compiling targets into a single line, likewise all the linking targets
#   This syntax would be more maintainable, but less legible

#use g++ for everything
CXX= g++

# include debugging symbols in object files,
# and enable all warnings
CXXFLAGS= -g -Wall -std=c++11

#include debugging symbols in executable
LDFLAGS= -g -std=c++11

default: main 

part2: main2

main: clean main.o Autocomplete TST.o
	$(CXX) $(LDFLAGS) -o main main.o Autocomplete.hpp TST.o

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c main.cpp

Autocomplete: Autocomplete.hpp
	$(CXX) $(CXXFLAGS) -c Autocomplete.hpp

main2: clean main2.o DocumentGenerator Graph.o 
	$(CXX) $(LDFLAGS) -o main2 main2.o DocumentGenerator.hpp Graph.o

main2.o: main2.cpp
	$(CXX) $(CXXFLAGS) -c main2.cpp

DocumentGenerator: DocumentGenerator.hpp
	$(CXX) $(CXXFLAGS) -c DocumentGenerator.hpp

DocumentGeneratorUtils: DocumentGeneratorUtils.hpp
	$(CXX) $(CXXFLAGS) -c DocumentGeneratorUtils.hpp

AutocompleteUtils: AutocompleteUtils.hpp
	$(CXX) $(CXXFLAGS) -c AutocompleteUtils.hpp

TST.o: TST.cpp
	$(CXX) $(CXXFLAGS) -c TST.cpp

TST: TST.hpp
	$(CXX) $(CXXFLAGS) -c TST.hpp

mytest.o: main_test.cpp
	$(CXX) $(CXXFLAGS) -c main_test.cpp

mytest: mytest.o TST
	$(CXX) $(CXXFLAGS) -o main_test main_test.o  TST.hpp

Graph: Graph.hpp
	$(CXX) $(CXXFLAGS) -c Graph.hpp

Graph.o: Graph.cpp
	$(CXX) $(CXXFLAGS) -c Graph.cpp

clean:
	$(RM) main main2 *.o *.gch

clean2:
	$(RM) *.gch

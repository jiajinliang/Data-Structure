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
CC= g++ -o

# include debugging symbols in object files,
# and enable all warnings
CXXFLAGS= -g -Wall -std=c++11

#include debugging symbols in executable
LDFLAGS= -g -std=c++11

default: main main2

part2: main2

main: main.o
	g++ -g -o main main.o

main2: main2.o
	g++ -g -o main2 main2.o

main.o: Autocomplete.hpp AutocompleteUtils.hpp MWT.hpp
main2.o: DocumentGenerator.hpp AutocompleteUtils.hpp MWT.hpp

clean:
	$(RM) main main2 *.o *.gch

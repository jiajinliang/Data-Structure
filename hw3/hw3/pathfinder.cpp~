#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <stdio.h>
#include "ActorGraph.hpp"
using namespace std;

int main(int argc, const char** argv) {
	bool weighted;		// weighted graph or nt
	string line;		// a line in the file

	if(argc != 5) {
		cerr << "Incorrect number of arguments." << endl;
		exit(-1);
	}

	if(*argv[2] == 'w') {
		weighted = true;
	} else {
		weighted = false;
	}

	ActorGraph actor_movie;
	actor_movie.loadFromFile(argv[1], weighted);
	
	remove(argv[4]);
	if(!actor_movie.findPath(argv[3], argv[4], weighted)) {
		exit(-1);
	}
}

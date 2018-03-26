#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <stdio.h>
#include "ActorGraph.hpp"
#include "ActorGraph.cpp"
using namespace std;

int main(int argc, const char** argv) {
	bool weighted;		// weighted graph or nt
	string line;		// a line in the file

	if(argc != 4) {
		cerr << "Incorrect number of arguments." << endl;
		exit(-1);
	}

	ActorGraph actor_movie;
	actor_movie.loadFromFile(argv[1], 0);
	
	remove(argv[3]);
	if(!actor_movie.findkcore(atoi(argv[2]), argv[3])) {
		exit(-1);
	}
}

#include <iostream>
#include <sstream>
#include "ActorGraph.hpp"
using namespace std;

int main(int argc, const char** argv) {
	if(argc != 4) {
		cerr << "Incorrect number of arguments." << endl;
		exit(-1);
	}

	ActorGraph actor_movie;

	actor_movie.loadFromFile(argv[1], false);

	remove(argv[3]);

	int k;
	stringstream value(argv[2]);
	value >> k;

	actor_movie.generateCore(k, argv[3]);
	return 0;
}

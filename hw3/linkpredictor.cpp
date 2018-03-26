#include <iostream>
#include "ActorGraph.hpp"
using namespace std;

int main(int argc, const char** argv) {
	if(argc != 5) {
		cerr << "Incorrect number of arguments." << endl;
		exit(-1);
	}

	ActorGraph actor_movie;

	actor_movie.loadFromFile(argv[1], true);

	remove(argv[3]);
	remove(argv[4]);

	actor_movie.findLink(argv[2], argv[3], argv[4]);
}

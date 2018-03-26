/**
 * File:	ActorGraph.cpp
 * Author:	Tianheng Liu, Jiajing Liang
 * Date:	Mar 15, 2018
 * Description:
 *	This file is meant to exist as a container for starter code that you can
 *	use to read the input file format defined in movie_casts.tsv. Feel free
 *	to modify any/all aspects as you wish.
 */


#include <iostream>
#include <iterator>
#include <fstream>
#include <sstream>
#include <queue>
#include <ctime>
#include "ActorGraph.hpp"
using namespace std;

int SIZE = 4;
static const char COMPUTE[] = "Computing ";
static const char PATH[] = "path for (";
static const char PREDICT[] = "predictions for (";
static const char IN[] = "--[";
static const char TO[] = ") -> (";
static const char WITH[] = "]-->(";
static const char FAILED_LOCATE[] = "Failed to locate '";
static const char OUTPUT_HEADER[] = "(actor)--[movie#@year]-->(actor)--...";
static const char OUTPUT_HEADER2[] = "Actor1,Actor2,Actor3,Actor4";
static const char NUM_OF_ACT[] = "#nodes: ";
static const char NUM_OF_MV[] = "#movies: ";
static const char NUM_OF_ED[] = "#edges: ";
static const char DONE[] = "done\n";

static long counter = 0;

// compare the cost
struct Cost {
	bool operator()(actor* act1, actor* act2) {
		return *act1 > *act2;
	}
};

// compare the number of common friend
struct Close {
	bool operator()(actor* act1, actor* act2) {
		return *act1 < *act2;
	}
};

void actor::countCommon() {
	set<actor*> links;
	for(movie* mv : movies) {
		for(actor* act : mv->actors) {
			if(act->checked) {
				links.insert(act);
			}
		}
	}
	common = links.size();
}

void actor::countNeighbour() {
	set<actor*> neighbours;
	for(movie* mv : movies) {
		for(actor* act : mv->actors) {
			neighbours.insert(act);
		}
	}

	cost = neighbours.size();
}

// output a string to a file
void output(string path, string content) {
	ofstream outfile(path, ios::app);	// output stream

	// append the content to the output file
	outfile << content << endl;
	outfile.close();
}

// get four actors that has the most common friends
string getMax(priority_queue<actor*, vector<actor*>, Close>* q) {
	string result;				// return value
	actor* this_actor;			// current actor
	
	// pop the queue four times and add the names to result
	result = "";
	for(int i = 0; i < SIZE; i++) {
		this_actor = q->top();
		q->pop();
		result += this_actor->actor_name;
		if(i < SIZE - 1) {
			result += "\t";
		}
	}
	return result;
}

ActorGraph::ActorGraph(void) {}

//`destructor
ActorGraph::~ActorGraph(void) {
	unordered_map<string, actor*>::iterator act_it;	// actor iterator
	unordered_map<string, movie*>::iterator mv_it;	// movie iterator
	
	// free up memory for actors
	act_it = actors.begin();
	for( ; act_it != actors.end(); act_it++) {
		delete act_it->second;
	}

	// free up memory for movies
	mv_it = movies.begin();
	for( ; mv_it != movies.end(); mv_it++) {
		delete mv_it->second;
	}
}

// count the egdes in the graph
int ActorGraph::edgeCount() {
	unordered_map<string, movie*>::iterator mv_it;	// movie iterator
	int act_count;					// actor count
	int edge_count;					// edge count

	// count the edges that go through a movie and sum them up
	mv_it = movies.begin();
	edge_count = 0;
	for( ; mv_it != movies.end(); mv_it++) {
		act_count = mv_it->second->actors.size();
		edge_count += act_count * (act_count - 1);
	}

	return edge_count;
}

//'graph builder
bool ActorGraph::loadFromFile(const char* in_filename, bool weighted) {
	actor* this_actor;			// actor being inserted
	movie* this_movie;			// movie being inserted
	int act_count = 0;			// number of actors
	int mv_count = 0;			// number of movies
	unordered_map<string, actor*>::iterator actor_it;
						// act iterator
	unordered_map<string, movie*>::iterator movie_it;
						// mv iterator
	ifstream infile(in_filename);		// input stream

	bool have_header = false;

	// keep reading lines until the end of file is reached
	while (infile) {
		string s;

		// get the next line
		if (!getline( infile, s )) break;

		if (!have_header) {
			// skip the header
			have_header = true;
			continue;
		}

		istringstream ss( s );
		vector <string> record;

		while (ss) {
			string next;

			// get the next string before hitting a tab character
			// and put it in 'next'
			if (!getline( ss, next, '\t' )) break;

			record.push_back( next );
		}

		if (record.size() != 3) {
			// we should have exactly 3 columns
			continue;
		}

		string actor_name(record[0]);
		string movie_title(record[1]);
		int movie_year = stoi(record[2]);
		string movie_name = movie_title + "#@" + record[2];


		// if actor not found, create a new actor node
		actor_it = actors.find(actor_name);
		if(actor_it == actors.end()) {
			this_actor = new actor(actor_name);
			actors.insert(make_pair(actor_name, this_actor));
			act_count++;

		// if acotr found, go to this actor
		} else {
			this_actor = actor_it->second;
		}

		// if movie not found, create a new movie node
		movie_it = movies.find(movie_name);
		if(movie_it == movies.end()) {
			this_movie = new movie(movie_name, movie_year,
				weighted);
			movies.insert(make_pair(movie_name, this_movie));
			mv_count++;

		// if movie found, go to this movie
		} else {
			this_movie = movie_it->second;
		}

		// add the movie to the actor node
		this_actor->addMovie(this_movie);

		// add the actor to the movie node
		this_movie->addActor(this_actor);

	}

	if (!infile.eof()) {
		cerr << "Failed to read " << in_filename << "!\n";
		return false;
	}
	infile.close();

	// stdout message
	cout << NUM_OF_ACT << act_count << endl;
	cout << NUM_OF_MV << mv_count << endl;
	cout << NUM_OF_ED << edgeCount() << endl;
	cout << DONE;

	return true;
}

//`actor finder
actor* ActorGraph::firstActor(string name) {
	unordered_map<string, actor*>::iterator found;
						// iterator to the first actor

	// nullptr if not found, otherwise, return the pointer to the actor
	found = actors.find(name);
	if(found == actors.end()) {
		return nullptr;
	}

	return found->second;
}

//`trace back
string ActorGraph::traceBack(actor* this_actor, string actor1) {
	string result;				// return path

	// trace back to actor1
	result = "";
	while(this_actor->actor_name != actor1) {
		// write down the path
		result = IN + this_actor->from_movie->movie_name + WITH +
			this_actor->actor_name + ")" + result;

		// go to the previous actor
		this_actor = this_actor->from_movie->from_actor;
	}

	// add the actor1 to the result
	result = "(" + actor1 + ")" + result;

	return result;
}

//`reset graph
void ActorGraph::reset() {
	unordered_map<string, actor*>::iterator act;	// actor iterator
	unordered_map<string, movie*>::iterator mv;	// movie iterator

	// reset actors
	act = actors.begin();
	for( ; act != actors.end(); act++) {
		act->second->visited = false;
		act->second->checked = false;
		act->second->cost = 0;
		act->second->from_movie = nullptr;
		act->second->common = 0;
	}

	// reset movies
	mv = movies.begin();
	for( ; mv != movies.end(); mv++) {
		mv->second->visited = false;
		mv->second->from_actor = nullptr;
		mv->second->cost = 0;
	}
	
}

//`unweighted path finder
bool ActorGraph::uFindPath(string actor1, string actor2,
		const char* output_path) {
	actor* this_actor;				// pointer to actor1
	queue<actor*> queue;				// queue of the actors

	// find the first actor, mark done, add to the queue
	if(!(this_actor = firstActor(actor1))) {
		cerr << FAILED_LOCATE << "'" << actor1 << "'" << endl;
		return false;
	}

	this_actor->visited = true;
	queue.push(this_actor);

	// find the shortest path to the second actor
	while(!queue.empty()) {
		// pop the actor from the queue
		this_actor = queue.front();
		queue.pop();

		// add the actors related to this_actor to the queue
		// loop through movie list of this_actor
		for(movie* mv : this_actor->movies) {
			// if this movie has been visited, go to next one
			if(mv->visited) {
				continue;
			}
			
			// mark done the movie, assign this_actor to the movie
			mv->visited = true;
			mv->from_actor = this_actor;

			// loop through the actor list of the movie
			for(actor* act : mv->actors) {
				// if the actor has been visited, go to next one
				if(act->visited) {
					continue;
				}

				// mark done the actor, compute the cost,
					// assign the movie to the actor
				act->visited = true;
				act->from_movie = mv;

				// if actor2 found
				if(act->actor_name == actor2) {
					// output to the file
					output(output_path,
						traceBack(act, actor1));
					
					// reset the graph
					reset();

					return true;
				}

				// add the actor to the queue
				queue.push(act);
			}
		}
	}

	return false;
}

//`weighted path finder
bool ActorGraph::wFindPath(string actor1, string actor2,
		const char* output_path) {
	actor* this_actor;				// pointer to actor1
	int temp_cost;					// temperary cost
	priority_queue<actor*, vector<actor*>, Cost> queue;
							// queue of the actors

	// find the first actor, add to the queue
	if(!(this_actor = firstActor(actor1))) {
		cerr << FAILED_LOCATE << "'" << actor1 << "'" << endl;
		return false;
	}

	queue.push(this_actor);

	// find the shortest path to the second actor
	while(!queue.empty()) {
		// pop the queue
		this_actor = queue.top();
		queue.pop();
		
		// if the actor has been visited, go to the next one
		if(this_actor->visited) {
			continue;
		}

		// mark done this_actor
		this_actor->visited = true;

		// if actor2 found
		if(this_actor->actor_name == actor2) {
			// output to the file
			output(output_path, traceBack(this_actor, actor1));
			
			// reset the graph
			reset();

			return true;
		}

		// add the actor related to this_actor to the queue
		for(movie* mv : this_actor->movies) {
			// the cost for this_actor to get to next actor
			temp_cost = this_actor->cost + mv->weight;

			// if the movie has been visited, compare the cost
			if(mv->cost && temp_cost > mv->cost) {
				continue;
			}
			
			// update the cost, assign the actor to the moive
			mv->cost = temp_cost;
			mv->from_actor = this_actor;

			// loop through the actor list of the movie
			for(actor* act : mv->actors) {
				// if the actor has been visited, go to next one
				if(act->visited) {
					continue;
				}

				// if the actor is in the queue
					// compare the cost
				if(act->cost && mv->cost > act->cost) {
					continue;
				}

				// update the cost
					// assign the movie to the actor
				act->cost = mv->cost;
				act->from_movie = mv;

				// add the actor to the queue
				queue.push(act);
			}
		}
	}

	return false;
}


//`path finder
bool ActorGraph::findPath(const char* input_path, const char* output_path,
		bool weighted) {
	string line;				// a line in the file
	bool status;				// return status
	ifstream infile(input_path);		// infile stream

	// add the header to the output file
	output(output_path, OUTPUT_HEADER);
	
	// skip the input file header
	getline(infile, line);

	// read in a line and find the path between two actors
	while(infile) {
		if(!getline(infile, line)) {
			break;
		}

		istringstream ss(line);
		vector <string> record;

		// get the next string before hitting a tab character
		// and put it in 'next'
		while (ss) {
			string next;
			if (!getline( ss, next, '\t' )) {
				break;
			}

			record.push_back(next);
		}

		if(record.size() != 2) {
			continue;
		}

		// get the names of actor1 and actor2
		string actor1(record[0]);
		string actor2(record[1]);
		
		// stdout message
		cout << COMPUTE << PATH << actor1 << TO << actor2 << ")"
			<< endl;

		// find the shortest path
		if(weighted) {
			status = wFindPath(actor1, actor2, output_path);
		} else {
			status = uFindPath(actor1, actor2, output_path);
		}

		if(!status) {
			return status;
		}
	}

	return true;
}

//`link finder
bool ActorGraph::findLink(const char* input_path, const char* output_path1,
		const char* output_path2) {
	string actor_name;			// name of first actor
	actor* this_actor;			// current actor
	ifstream infile(input_path);		// input file stream

	// skip input header
	getline(infile, actor_name);

	// output header
	output(output_path1, OUTPUT_HEADER2);
	output(output_path2, OUTPUT_HEADER2);

	while(infile) {
		queue<actor*> queue;			// queue for first layer
		priority_queue<actor*, vector<actor*>, Close> old_friend;
							// old friend queue
		priority_queue<actor*, vector<actor*>, Close> new_friend;
							// new friend queue

		// get name
		if(!getline(infile, actor_name)) {
			break;
		}

		// stdout message
		cout << COMPUTE << PREDICT << actor_name << ")" << endl;

		// failed to locate the first actor
		if(!(this_actor = firstActor(actor_name))) {
			cerr << FAILED_LOCATE << "'" << actor_name << "'"
				<< endl;
			return false;
		}

		this_actor->visited = true;
		
		// enqueue first the layer
		for(movie* mv : this_actor->movies) {
			mv->visited = true;
			for(actor* act : mv->actors) {
				if(act->visited) {
					continue;
				}

				act->visited = true;
				act->checked = true;
				queue.push(act);
			}
		}

		// enqueue new and old friend
		while(!queue.empty()) {
			this_actor = queue.front();
			queue.pop();
			
			// add old_friend
			this_actor->countCommon();
			old_friend.push(this_actor);

			// add new_friend
			for(movie* mv : this_actor->movies) {
				if(mv->visited) {
					continue;
				}

				mv->visited = true;
				for(actor* act : mv->actors) {
					if(act->visited) {
						continue;
					}

					act->visited = true;
					act->countCommon();
					new_friend.push(act);
				}
			}
		}
		
		// output result
		output(output_path1, getMax(&old_friend));
		output(output_path2, getMax(&new_friend));

		// reset the graph
		reset();
	}

	return true;
}

void ActorGraph::generateCore(int k, const char* output_path) {
	unordered_map<string, actor*>::iterator act_it;
	priority_queue<actor*, vector<actor*>, Cost> list;
	priority_queue<actor*, vector<actor*>, Close> invite;
	actor* this_actor;
	
	act_it = actors.begin();
	for( ; act_it != actors.end(); act_it++) {
		act_it->second->countNeighbour();
		list.push(act_it->second);
	}

	while(list.top()->cost < k) {
		this_actor = list.top();
		list.pop();

		if(this_actor->visited) {
			continue;
		}

		this_actor->visited = true;

		vector<actor*> reduced;
		for(movie* mv : this_actor->movies) {
			for(actor* act : mv->actors) {
				if(!act->checked) {
					act->checked = true;
					act->cost--;
					list.push(act);
					reduced.push_back(act);
				}
			}
		}

		for(actor* act : reduced) {
			act->checked = false;
		}
	}

	act_it = actors.begin();
	for( ; act_it != actors.end(); act_it++) {
		if(!act_it->second->visited) {
			invite.push(act_it->second);
		}
	}

	ofstream outfile(output_path);
	outfile << "Actor" << endl;
	while(!invite.empty()) {
		outfile << invite.top()->actor_name << endl;
		invite.pop();
	}
	outfile.close();
}

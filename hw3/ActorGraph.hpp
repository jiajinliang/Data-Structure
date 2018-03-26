/*
 * ActorGraph.hpp
 * Author: <YOUR NAME HERE>
 * Date:   <DATE HERE>
 *
 * This file is meant to exist as a container for starter code that you can use
 * to read the input file format
 * defined in movie_casts.tsv. Feel free to modify any/all aspects as you wish.
 */

#ifndef ACTORGRAPH_HPP
#define ACTORGRAPH_HPP

#include <vector>
#include <string>
#include <queue>
#include <set>
#include <unordered_map>
using namespace std;

// Maybe include some data structures here
const int YEAR = 2019;
struct movie;

struct actor {
	string actor_name;
	vector<movie*> movies;
	int cost;
	int common;
	bool visited;
	bool checked;
	movie* from_movie;

	actor(string act) {
		actor_name = act;
		visited = false;
		from_movie = nullptr;
		cost = 0;
		common = 0;
		checked = false;
	}

	void addMovie(movie* mv) {
		movies.push_back(mv);
	}

	bool operator>(const actor &act) {
		return cost > act.cost;
	}

	bool operator<(const actor &act) {
		if(common == act.common) {
			return actor_name.compare(act.actor_name) > 0;
		}
		return common < act.common;
	}

	void countCommon();
	
	void countNeighbour();
};

struct movie {
	string movie_name;
	vector<actor*> actors;
	unordered_map<string, actor*> list;
	int weight;
	int cost;
	bool visited;
	actor* from_actor;

	movie(string mv, int yr, bool weighted) {
		movie_name = mv;
		from_actor = nullptr;
		visited = false;

		if(weighted) {
			weight = YEAR - yr;
		} else {
			weight = 1;
		}
		cost = 0;
	}

	void addActor(actor* act) {
		actors.push_back(act);
		list[act->actor_name] = act;
	}
};

class ActorGraph {
	protected:
		// Maybe add class data structure(s) here

	public:
		unordered_map<string, actor*> actors;
		unordered_map<string, movie*> movies;

		ActorGraph(void);

		~ActorGraph(void);

		/** You can modify this method definition as you wish
		 *
		 * Load the graph from a tab-delimited file of actor->movie
		 * relationships.
		 *
		 * in_filename - input filename
		 * use_weighted_edges - if true, compute edge weights as
		 * 1 + (2018 - movie_year), otherwise all edge weights will be 1
		 *
		 * return true if file was loaded sucessfully, false otherwise
		 */
		bool loadFromFile(const char* in_filename, bool weighted);

		bool findPath(const char* input_path, const char* output_path,
				bool weighted);

		bool uFindPath(string actor1, string actor2,
				const char* output_path);

		bool wFindPath(string actor1, string actor2,
				const char* output_path);

		int edgeCount();

		actor* firstActor(string name);

		string traceBack(actor* this_actor, string actor1);

		//void linkBuilder();

		bool findLink(const char*, const char*, const char*);

		void generateCore(int, const char*);

		void reset();

		// Maybe add some more methods here

};
#endif // ACTORGRAPH_HPP

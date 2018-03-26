/**
 *  CSE 100 PA2 C++ Autocomplete
 *  Author: Jonathan Margoliash
 *  Modified from code authored by: Jor-el Briones, Christine Alvarado
 */

#ifndef AUTOCOMPLETE_HPP
#define AUTOCOMPLETE_HPP

#include <vector>
#include <string>
#include <algorithm>
#include "TST.hpp"
using namespace std;

struct TSTNode;

/**
 *  You may implement this class as either a mulit-way trie
 *  or a ternary search trie.
 */
class Autocomplete : public TST
{

public:
  /* 
  Create an Autocomplete object.
  This object should be trained on the words vector
  That is - the predictCompletions() function below should pull autocomplete
  suggestions from this vector

  Input: words. Must be all lowercase, with most  non-word characters removed (e.g. ',' ';' '%' etc.)
  In addition to alphabetic characters, words may contain digits, single apostrophes, dashes etc.
  */
  Autocomplete(const vector<string> words) {
    //TODO (done)
    for(string w : words)
		insert(w);
  }

  /* Return up to 10 of the most frequent completions
   * of the prefix, such that the completions are words in the dictionary.
   * These completions should be listed from most frequent to least.
   * If there are fewer than 10 legal completions, this
   * function returns a vector with as many completions as possible.
   * Otherwise, 10 completions should be returned.
   * If no completions exist, then the function returns a vector of size 0.
   * The prefix itself might be included in the returned words if the prefix
   * is a word (and is among the 10 most frequent completions
   * of the prefix)
   * If you need to choose between two or more completions which have the same frequency,
   * choose the one that comes first in alphabetical order.
   *
   * Inputs: prefix. The prefix to be completed. Must be of length >= 1.
   * Return: the vector of completions
   */
  vector<string> predictCompletions(const string prefix) {
    return predictCompletionsHelper(prefix); //TODO (done)
  }

  /* Destructor */
  ~Autocomplete() {
    //TODO (done)
    // nothing is created on heap in this scope
    // it will automatically call the destructor of TST
  }

  //You may add your own code here

private:

  //you may add your own code here

	vector<string> predictCompletionsHelper(const string prefix) const {

		// empty tree case, return empty vector
		if(empty())
			return vector<string>();

		// empty prefix, return every word
		if(prefix == "")
			return getWords(root);

		// find the prefix's node's location
		TSTNode* curr = root;
		for(unsigned int i = 0; i < prefix.length(); i++) {
			if(curr == NULL)
				return vector<string>(); // not found the prefix

			if(curr->character == prefix[i]) {
				if(i == prefix.length()-1)
					break;
				else
					curr = curr->middle;
			}
			else if(curr->character > prefix[i]) {
				curr = curr->left;
				i--;
			}
			else {
				curr = curr->right;
				i--;
			}
		}

		// return all the words startng with current node's word
		return getWords(curr);
	}

};

#endif // AUTOCOMPLETE_HPP

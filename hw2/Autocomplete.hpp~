/**
 *  CSE 100 PA2 C++ Autocomplete
 *  Author: Jonathan Margoliash
 *  Modified from code authored by: Jor-el Briones, Christine Alvarado
 */

#ifndef AUTOCOMPLETE_HPP
#define AUTOCOMPLETE_HPP

#include <vector>
#include <string>
#include <unordered_map>
#include <iterator>
#include <algorithm>
#include "MWT.hpp"
using namespace std;

/**
 *  You may implement this class as either a mulit-way trie
 *  or a ternary search trie.
 */
class Autocomplete
{
public:

  /* 
  Create an Autocomplete object.
  This object should be trained on the words vector
  That is - the predictCompletions() function below should pull autocomplete
  suggestions from this vector

  Input: words. Must be all lowercase, with most  non-word characters removed
		(e.g. ',' ';' '%' etc.)
  In addition to alphabetic characters, words may contain digits, single
		apostrophes, dashes etc.
  */
	//`autocomplete
  Autocomplete(const vector<string> words) {
		tree = new MWT();
		tree->insert(words);
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
   * If you need to choose between two or more completions which have the same
	 * frequency, choose the one that comes first in alphabetical order.
   *
   * Inputs: prefix. The prefix to be completed. Must be of length >= 1.
   * Return: the vector of completions
   */
	//`predict
  vector<string> predictCompletions(const string prefix) {
		return tree->search(prefix);
  }

  /* destructor */
  ~Autocomplete() {
		delete tree;
  }
  //You may add your own code here

private:
  //you may add your own code here
	MWT* tree;
};

#endif // AUTOCOMPLETE_HPP

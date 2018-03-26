#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <assert.h>

#include "AutocompleteUtils.hpp"
#include "Autocomplete.hpp"

using namespace std;

// generates predictions based on the dictionary at the given file location, using the given list of prefixes
// predictions are printed to cout:
// all the predictions for a single prefix are printed out in order on a single line, separated by spaces
// the predictions for each prefix are printed on their own line
void runTest(const string fileLocation, const vector<string> prefixes) {
  vector<string> words = AutocompleteUtils::getWords(fileLocation);
  Autocomplete* autocomplete = new Autocomplete(words);

  for (string prefix : prefixes) {
    vector<string> completions = autocomplete->predictCompletions(prefix);
    for (string completion : completions) {
      cout << completion << " ";
    } 
    cout << endl;
  }

  delete autocomplete;
}


//Example use: ./main path/to/corpus.txt prefix1 prefix2, e.g. ./main TestCases/ModerateCorpus w wasn't wasn'ta x
//First argument: path to the file containing the corpus of words to be loaded
//If the second argument is '-o', then its followed by a fixed number of arguments
//All the following arguments (or all the arguments after the first, if '-o' is not supplied)
//are prefixes to be completed
//e.g. ./main path/to/corpus.txt prefix1 prefix2 ...
// or ./main path/to/corpus.txt -o option1 prefix1 prefix2 ...
//currently, there is only one option
//option1: number of times to repeat the test
//instead of a list of prefixes, a file of prefixes can be supplied
//e.g. ./main path/to/corpus.txt -p path/to/prefixes.txt
//see runTest for output details
int main(int argc, const char ** argv) {

  if(argc < 2){
      cout << "Incorrect number of arguments." << endl;
      cout << "\t First argument: name of dictionary file." << endl;
      cout << endl;
      exit(-1);
  }

  unsigned int numRepetitions = 1;
  int prefixStartIdx = 2;
  if (string(argv[2]).compare("-o") == 0) {
    if (argc < 4) {
      cout << "Incorrect number of arguments" << endl;
      cout << "Expected syntax like ./main path/to/corpus.txt -o option1 prefix1 prefix2";
      exit(-1);
    }
    try {
        numRepetitions = stoi(string(argv[3]));
    } catch (exception e) {
      cout << "First option must be an integer - the number of repetitions" << endl;
      exit(-1);
    }

    prefixStartIdx = 4;
  }


  //Load prefixes, either from input vector or from file
  vector<string> prefixes;
  if (string(argv[prefixStartIdx]).compare("-p") == 0) {
    assert(argc = prefixStartIdx + 2);
    prefixes = AutocompleteUtils::getWords(argv[prefixStartIdx + 1]);
  } else {
    for (int prefixIdx = prefixStartIdx; prefixIdx < argc; prefixIdx ++) {
      prefixes.push_back(argv[prefixIdx]);
    }
  }

  for (unsigned int count = 0; count < numRepetitions; count ++) {
    runTest(argv[1], prefixes);
  }
}

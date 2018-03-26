#ifndef AUTOCOMPLETE_UTILS_HPP
#define AUTOCOMPLETE_UTILS_HPP

#include <string>
#include <fstream>
#include <vector>
#include <iostream>

using namespace std;

namespace AutocompleteUtils {

  const string whitespace = " \t\r\n\v\f";

  //break a line over whitespace separators
  vector<string> tokenize(const string line) {
    vector<string> words;
    vector<char> word;
    for (unsigned char c : line) {
      if (whitespace.find(c) == string::npos) {
        word.push_back(c);
      } else if (word.size() > 0) {
        words.push_back(string(word.begin(), word.end()));
        word.clear();
      }
    }
    if (word.size() > 0) {
      words.push_back(string(word.begin(), word.end()));
    }
    return words;
  }

  //load a file and return a vector of all the words in that file
  //this function only splits the contents of the file over whitespace
  //and does not make exceptions for punctuation or unwanted characters
  vector<string> getWords(const string fileLocation) {
    vector<string> words;

    ifstream infile;
    infile.open(fileLocation);

    if (!infile) {
      cerr << "Couldn't open file: " << fileLocation << endl;
      exit(1);
    }

    string line;
    while(getline(infile, line)) {
      vector<string> wordsInLine = tokenize(line);
      words.insert(words.end(), wordsInLine.begin(), wordsInLine.end());
    }

    return words;  
  }
}

#endif // AUTOCOMPLETE_UTILS_HPP

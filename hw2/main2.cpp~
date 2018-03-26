#include <iostream>
#include <string.h>
#include <sstream>

#include "DocumentGenerator.hpp"

using namespace std;


//Example use: ./main2 singleword path/to/directory theword numreps
//./main2 document path/to/directory numwords
int main(int argc, const char ** argv) {

  if(argc < 2 || (strcmp(argv[1], "document") != 0 && strcmp(argv[1], "singleword") != 0 && strcmp(argv[1], "-r") != 0)) {
    if (argc < 2) { 
      cout << "Incorrect number of arguments." << endl;
    }
    cout << "First argument: name of test (either 'document' or 'singleword' or '-r')" << endl;
    cout << endl;
    exit(-1);
  }

  int numReps = 1;
  if(strcmp(argv[1], "-r") == 0) {
    if (argc < 3) {
      cout << "Incorrect number of arguments. Expected num repetitions after -r." << endl;
    }
    stringstream ss;
    ss << argv[2];
    ss >> numReps;
    if (ss.fail()) {
      cerr << "Couldn't read number of reps." << endl;
      exit(-1);
    }
    argv = &argv[2];
    argc -= 2;
  }
 
  for (int rep = 0; rep < numReps; rep++) { 
    if(argc < 3) {
      cout << "Incorrect number of arguments. Second argument should be the directory to load documents from\n";
      exit(-1);
    }
  
    if (strcmp(argv[1], "document") == 0) {
      if (argc < 4) {
        cout << "Incorrect number of arguments\n";
        cout << "Third argument should be the number of words to generate\n";
        exit(-1);
      }
      stringstream ss;
      ss << argv[3];
      int numWords;
      ss >> numWords;
      if (ss.fail()) {
        cout << "Third argument not an integer\n";
        exit(-1);
      }
    
      int numInternalReps = 1;
      if (argc == 5) {
	stringstream ss;
        ss << argv[4];
        ss >> numInternalReps;
	if (ss.fail()) {
          cout << "Fourth arg not an integer\n";
	  exit(-1);
        }
      } 
      //check for a repetition argument
      for (int internalRep = 0; internalRep < numInternalReps; internalRep++) {
        DocumentGenerator dg(argv[2]);
        cout << dg.generateDocument(numWords);
        cout << endl;
      }
    } else if (strcmp(argv[1], "singleword") == 0) {
      if (argc < 5) {
        cout << "Incorrect number of arguments\n";
        cout << "Third argument should be the word to generate words from\n";
        cout << "Fourth argument should be the number of words to generate from that start\n";
        exit(-1);
      }
      stringstream ss;
      ss << argv[4];
      int numWords;
      ss >> numWords;
      if (ss.fail()) {
        cout << "Fifth argument not an integer\n";
        exit(-1);
      }
      
      DocumentGenerator dg(argv[2]);
      for (int i=0; i<numWords; i++) {
        cout << dg.generateNextWord(argv[3]);
        cout <<" ";
      }
      cout << "\n";
    } else {
      cerr << "Couldn't recognize first argument. This line should never be reached." << endl;
      exit(-1);
    }
  }
};


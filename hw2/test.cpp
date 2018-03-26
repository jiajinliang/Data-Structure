#include <iostream>
#include <string.h>
#include <sstream>
#include "DocumentGenerator.hpp"

using namespace std;

int main() {
	DocumentGenerator a("myTest/");

	string result = a.generateDocument(100);
	cout << result << endl;
}

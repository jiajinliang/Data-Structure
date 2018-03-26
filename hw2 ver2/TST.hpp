#ifndef TST_HPP
#define TST_HPP
#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <utility>
#include <stack>
using namespace std;

// global variable
const unsigned int CAPACITY = 10;

// TSTNode decleration
struct TSTNode{

	TSTNode* parent;
	TSTNode* left;
	TSTNode* middle;
	TSTNode* right;
	char character;
	bool wordNode;
	unsigned int frequency;

	TSTNode(const char & c) : character(c), wordNode(false), frequency(0) {
		left = right = middle = parent = 0;
	}
};

class TST {

	public:
		TST();
		virtual ~TST();
		void insert(string &word);
		bool find(const string word) const;
		bool empty() const;
		void inorder(TSTNode *n) const;
		vector<string> getWords(TSTNode* n) const;

	protected:
		TSTNode*root;

	private:
		void insert_helper(unsigned int pos, const string &word, TSTNode* curr);
		void deleteAll(TSTNode* n);
		void inorder_helper(TSTNode* n) const;
		void getWords_helper(TSTNode*n, vector<pair<string,int>> &vp) const;
		void addWord(TSTNode* n, vector<pair<string,int>> &vp)const;

};


#endif // TST_HPP

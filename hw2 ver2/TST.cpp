#include "TST.hpp"
#include <iostream>
#include <string>
#include <stack>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

// comparator function for vector<pair<string,int>> 
bool compFreq(const pair<string,int> &p1, const pair<string,int> &p2) {
	if(p1.second == p2.second) {
		return (p1.first > p2.first);
	}
	return (p1.second < p2.second);
}

// default constructor
TST::TST() : root(0) {}

// destructor
TST::~TST(){
	if(root)
		deleteAll(root);
}

// insert a word into the tree
void TST::insert(string &word){

	// empty tree
	if(root == NULL) {
		root = new TSTNode(word[0]);
		TSTNode* curr = root;
		insert_helper(1, word, curr);
	}

	// not empty tree
	else {

		TSTNode* curr = root;

		// for each character in word
		for(unsigned int i = 0; i < word.length(); i++) {

			// same character case
			if(curr->character == word[i]) {

				// end of word, then increment the frequency
				if(i == word.length()-1) {
					if(curr->wordNode == false)
						curr->wordNode = true;
					curr->frequency += 1;
					break;
				}

				// go to middle child
				if(curr->middle) {
					curr = curr->middle;
					//continue;
				}

				// if middle child doesn't exist, insert all
				else {
					insert_helper(i+1, word, curr);
					break;
				}
			}

			// smaller character case, go left
			else if(curr->character > word[i]){

				// if left child is null, insert all
				if(curr->left == NULL) {
					curr->left = new TSTNode(word[i]);
					curr->left->parent = curr;
					curr = curr->left;
					insert_helper(i+1, word, curr);
					break;
				}	

				// if left child is not null, go left
				else {
					curr = curr->left;
					i--;
					//continue; 
				}
			}

			// larger character case,  go right
			else { // if(curr->character < word[i])

				// if right child is null, insert all
				if(curr->right == NULL) {
					curr->right = new TSTNode(word[i]);
					curr->right->parent = curr;
					curr = curr->right;
					insert_helper(i+1, word, curr);
					break;
				}	

				// if right child is not null, go right
				else {
					curr = curr->right;
					i--;
					//continue; 
				}
			}
		}	
	}
}

// find if a string is in the tree	
bool TST::find(const string word) const {

	if(root == NULL)
		return false;

	TSTNode* curr = root;

	for(unsigned int i = 0; i < word.length(); i++) {
		if(curr == NULL)
			return false;

		if(curr->character == word[i]) {
			if(i == word.length()-1) {
				if(curr->wordNode)
					return true;
			}
			else
				curr = curr->middle;
		}
		else if(curr->character > word[i]) {
			curr = curr->left;
			i--;
		}
		else {
			curr = curr->right;
			i--;
		}
	}

	return false;
}

bool TST::empty() const {
	if(root == NULL)
		return true;
	return false;

} 

void TST::inorder(TSTNode *n) const {
	inorder_helper(n);
}

// get all the words starting with current node's word
vector<string> TST::getWords(TSTNode* n) const {

	vector<pair<string,int>> vp;
	if(n->wordNode)
		addWord(n, vp);
	getWords_helper(n->middle, vp);

	if(vp.size() == 0)
		return vector<string>();

	sort(vp.begin(), vp.end(), compFreq);
	reverse(vp.begin(), vp.end());

	vector<string> vs;
	for(auto w : vp)
		vs.push_back(get<0>(w));

	return vs;
}

// insert the rest of word all the way down in middle
void TST::insert_helper(unsigned int pos, const string &word, TSTNode* curr) {
	for(unsigned int i = pos; i < word.length(); i++) {
		curr->middle = new TSTNode(word[i]);
		curr->middle->parent = curr;
		curr = curr->middle;
	}
	curr->wordNode = true;
	curr->frequency = 1;
}

// delete all nodes
void TST::deleteAll(TSTNode* n){

	if(n == NULL)
		return;

	deleteAll(n->left);
	deleteAll(n->middle);
	deleteAll(n->right);
	delete(n);
}

// in-orderly print all words
void TST::inorder_helper(TSTNode* n) const{

	if(n == NULL)
		return;

	inorder(n->left);

	if(n->wordNode) {
		TSTNode* curr = n;
		unsigned int freq = curr->frequency;
		stack<char> st;
		st.push(curr->character);
		while(curr->parent) {
			if(curr == curr->parent->middle) {
				st.push(curr->parent->character);
			}
			curr = curr->parent;
		}

		while(!st.empty()) {
			cout << st.top();
			st.pop();
		}
		cout << " " << freq << endl;
	}

	inorder(n->middle);
	inorder(n->right);
}

// get words of the current node
void TST::getWords_helper(TSTNode*n, vector<pair<string,int>> &vp) const {

	if(n == NULL)
		return;

	getWords_helper(n->left, vp);

	if(n->wordNode) {
		addWord(n, vp);
	}

	getWords_helper(n->middle, vp);
	getWords_helper(n->right, vp);
}

// add a word to the vector pair (capacity is 10)
void TST::addWord(TSTNode* n, vector<pair<string,int>> &vp)const {

	TSTNode* curr = n;
	unsigned int freq = curr->frequency;
	stack<char> st;
	st.push(curr->character);

	while(curr->parent) {
		if(curr == curr->parent->middle) {
			st.push(curr->parent->character);
		}
		curr = curr->parent;
	}

	string word = "";
	while(!st.empty()) {
		word += st.top();
		st.pop();
	}
	if(vp.size() < CAPACITY)
		vp.push_back(pair<string,int>(word,freq));
	else {
		sort(vp.begin(), vp.end(), compFreq);
		pair<string,int> p(word, freq);
		if(compFreq(vp[0], p))
			vp[0].swap(p);
	}
}





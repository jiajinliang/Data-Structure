#ifndef BST_HPP
#define BST_HPP
#include "BSTNode.hpp"
#include "BSTIterator.hpp"
#include <iostream>
using namespace std;

template<typename Data>
class BST {

protected:

  /** Pointer to the root of this BST, or 0 if the BST is empty */
  BSTNode<Data>* root;

  /** Number of Data items stored in this BST. */
  unsigned int isize;

  /** Height of this BST. */
  unsigned int iheight;
  
public:

  /** define iterator as an aliased typename for BSTIterator<Data>. */
  typedef BSTIterator<Data> iterator;

  /** Default constructor.
      Initialize an empty BST.
   */
  BST() : root(0), isize(0), iheight(0) {  }


  /** Default destructor.
      Delete every node in this BST.
   */ // TODO
  virtual ~BST() {
		deleteAll(root);
  }

  /** Given a reference to a Data item, insert a copy of it in this BST.
   *  Return  true if the item was added to this BST
   *  as a result of this call to insert,
   *  false if an item equal to this one was already in this BST.
   *  Note: This function should use only the '<' operator when comparing
   *  Data items. (should not use ==, >, <=, >=)  For the reasoning
   *  behind this, see the assignment writeup.
   */ // TODO
  virtual bool insert(const Data& item) {
		if(!root) {
			root=new BSTNode<Data>(item);
			isize++;
			iheight++;
			return 1;
		}
		BSTNode<Data>* current=root;
		while(true) {
			if(item<current->data) {
				if(current->left) {
					current=current->left;
				} else {
					current->left=new BSTNode<Data>(item);
					current->left->parent=current;
					break;
				}
			} else if(current->data<item) {
				if(current->right) {
					current=current->right;
				} else {
					current->right=new BSTNode<Data>(item);
					current->right->parent=current;
					break;
				}
			} else {
				return 0;
			}
		}
		unsigned int counter=1;
		while(current) {
			current=current->parent;
			counter++;
		}
		iheight=max(iheight,counter);
		isize++;
		return 1;
  }


  /** Find a Data item in the BST.
   *  Return an iterator pointing to the item, or pointing past
   *  the last node in the BST if not found.
   *  Note: This function should use only the '<' operator when comparing
   *  Data items. (should not use ==, >, <=, >=).  For the reasoning
   *  behind this, see the assignment writeup.
   */ // TODO
  virtual iterator find(const Data& item) const {
		if(root) {
			BSTNode<Data>* current=root;
			while(true) {
				if(item<current->data) {
					if(current->left) {
						current=current->left;
					} else {
						break;
					}
				} else if(current->data<item) {
					if(current->right) {
						current=current->right;
					} else {
						break;
					}
				} else {
					iterator found(current);
					return found;
				}
			}
		}
		iterator notFound(nullptr);
		return notFound;
  }

  
  /** Return the number of items currently in the BST.
   */ // TODO
  unsigned int size() const {
		return isize;
  }
  
  /** Return the height of the BST.
   */ // TODO
  unsigned int height() const {
		return iheight;
  }


  /** Return true if the BST is empty, else false.
   */ // TODO
  bool empty() const {
		if(!root) {
			return 1;
		}
		return 0;
  }

  /** Return an iterator pointing to the first item in the BST (not the root).
   */ // TODO
  iterator begin() const {
		iterator begin(first(root));
		return begin;
  }

  /** Return an iterator pointing past the last item in the BST.
   */
  iterator end() const {
    return typename BST<Data>::iterator(0);
  }

  /** Perform an inorder traversal of this BST.
   */
  void inorder() const {
    inorder(root);
  }


private:

  /** Recursive inorder traversal 'helper' function */

  /** Inorder traverse BST, print out the data of each node in ascending order.
      Implementing inorder and deleteAll base on the pseudo code is an easy way to get started.
   */ // TODO
  void inorder(BSTNode<Data>* n) const {
    /* Pseudo Code:
      if current node is null: return;
      recursively traverse left sub-tree
      print current node data
      recursively traverse right sub-tree
    */
		if(!n) {
			return;
		}
		inorder(n->left);
		cout<<n<<endl;
		inorder(n->right);
  }

  /** Find the first element of the BST
   */ 
  static BSTNode<Data>* first(BSTNode<Data>* curr) {
    if(curr == 0) return 0;
    while(curr->left != 0) curr = curr->left;
    return curr;
  }

  /** do a postorder traversal, deleting nodes
   */ // TODO
  static void deleteAll(BSTNode<Data>* n) {
    /* Pseudo Code:
      if current node is null: return;
      recursively delete left sub-tree
      recursively delete right sub-tree
      delete current node
    */
		if(!n) {
			return;
		}
		deleteAll(n->left);
		deleteAll(n->right);
		delete n;
		n=nullptr;
  }


 };


#endif //BST_HPP

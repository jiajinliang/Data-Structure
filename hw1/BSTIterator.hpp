#ifndef BSTITERATOR_HPP
#define BSTITERATOR_HPP
#include "BSTNode.hpp"
#include <list>
#include <iterator>
using namespace std;

template<typename Data>
class BSTIterator : public iterator<input_iterator_tag,Data> {

private:

  BSTNode<Data>* curr;

public:

  /** Constructor.  Use the argument to initialize the current BSTNode
   *  in this BSTIterator.
   */ // CHECK
  BSTIterator(BSTNode<Data>* curr) {
		this->curr=curr;
  }

  /** Dereference operator. */
  Data operator*() const {
    return curr->data;
  }
  
  /** Pre-increment operator. */
  BSTIterator<Data>& operator++() {
    curr = curr->successor();
    return *this;
  }

  /** Post-increment operator. */
  BSTIterator<Data> operator++(int) {
    BSTIterator before = BSTIterator(curr);
    ++(*this);
    return before;
  }

  /** Equality test operator. */ // CHECK
  bool operator==(BSTIterator<Data> const & other) const {
		return curr==other.curr;
  }

  /** Inequality test operator. */ // CHECK
  bool operator!=(BSTIterator<Data> const & other) const {
		return curr!=other.curr;
  }

};

#endif //BSTITERATOR_HPP

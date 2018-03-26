#ifndef MATRIXMULT_HPP
#define MATRIXMULT_HPP
#include <iostream>
#include <vector>

using namespace std;

template <class T>
class MatrixOperations {
public:
  vector<vector<T>> matrixA;
  vector<vector<T>> matrixB;
  MatrixOperations(const vector<vector<T>> &a, const vector<vector<T>> &b)  {
   matrixA = a;
   matrixB = b;
  }
  vector<vector<T>> matrixMultiply()
  {
    const int dim1 = matrixA.size();     // a rows
    const int dim2 = matrixA[0].size();  // a cols
    const int dim3 = matrixB[0].size();  // b cols

    vector<vector<T>> prodMatrix(dim1,vector<T>(dim3, 0));
    for (auto itop = 0; itop < dim1; itop+=32)
    {
        for (auto jtop = 0; jtop < dim3; jtop+=32)
        {
            for (auto ktop = 0; ktop < dim2; ktop+=32)
            {
		for (auto i = itop; i<((itop+32)>dim1?dim1:(itop+32));i++){

		  for (auto j = jtop; j<((jtop+32)>dim3?dim3:(jtop+32));j++) {

		    for (auto k = ktop; k<((ktop+32)>dim2?dim2:(ktop+32));k++) {

                	prodMatrix[i][j] += matrixA[i][k] * matrixB[k][j];
		    }
		  }
		}
            }
        }
    }
    return prodMatrix;
  }


};

#endif

cimport cython
cimport numpy as cnp
import numpy as np


@cython.wraparound(False)
@cython.boundscheck(False)
cpdef cnp.ndarray[cnp.float64_t, ndim=2] _matrix_multiply(cnp.ndarray[cnp.float64_t, ndim=2] A, 
                                                         cnp.ndarray[cnp.float64_t, ndim=2] B):
    cdef int i, j, k
    cdef int A_rows = A.shape[0]
    cdef int A_cols = A.shape[1]
    cdef int B_cols = B.shape[1]

    cdef cnp.ndarray[cnp.float64_t, ndim=2] C = np.zeros((A_rows, B_cols), dtype=np.float64)
    
    for i in range(A_rows):
        for j in range(B_cols):
            for k in range(A_cols):
                C[i, j] += A[i, k] * B[k, j]
    
    return C

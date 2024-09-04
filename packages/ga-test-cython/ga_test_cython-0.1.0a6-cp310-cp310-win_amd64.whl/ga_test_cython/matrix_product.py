from ga_test_cython.operations_utils.dot_product_utils import _matrix_multiply


def matrix_multiply(a, b):
    if a.shape[1] != b.shape[0]:
        raise ValueError("The number of columns in A have to be the same of number of rows in B.")
    return _matrix_multiply(a, b)

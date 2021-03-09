import numpy as np

testmatrix = np.asarray([[34/50,-20/50,12/50], [-20/50,25/50,15/50], [12/50,15/50,41/50]])
print(np.linalg.eigvals(testmatrix))

def find_det(A):
    d0 = A[0][0]*(A[1][1]*A[2][2]-A[2][1]*A[1][2])
    d1 = A[0][1]*(A[1][0]*A[2][2]-A[2][0]*A[1][2])
    d2 = A[0][2]*(A[1][0]*A[2][1]-A[2][0]*A[1][1])
    return d0-d1+d2


def find_eigenvalues(A):
    l1_1 = (A[0][0]*A[1][1])+(A[0][0]*A[2][2])+(A[1][1]*A[2][2])-(A[2][1]*A[1][2])
    l1_2 = (A[0][1]*A[1][0])
    l1_3 = (A[0][2]*A[2][0])
    l1 = -l1_1+l1_2+l1_3
    l2 = A[0][0]+A[1][1]+A[2][2]
    l3 = -1
    r_1 = (A[0][0]*A[1][1]*A[2][2])-(A[0][0]*A[2][1]*A[1][2])
    r_2 = (A[0][1]*A[1][0]*A[2][2])-(A[0][1]*A[2][0]*A[1][2])
    r_3 = (A[0][2]*A[1][0]*A[2][1])-(A[0][2]*A[2][0]*A[1][1])
    r = r_1 - r_2 + r_3
    roots = np.roots([l3, l2, l1, r])
    print(f"EQ is: {l3}λ^3 {l2}λ^2 {l1}λ {r}")
    print("Eigenvalues:")
    for i, root in enumerate(roots):
        print(f"λ_{i+1} = {round(root, 4)}")
    return roots


def find_eigenvectors(A, eval_A):
    n = A.shape[0]
    evec_A = np.zeros((n, n))
    for k in range(n):
        M = np.delete(A, k, axis=0)
        M = np.delete(M, k, axis=1)
        eval_M = np.linalg.eigvals(M)

        nominator = [np.prod(eval_A[i] - eval_M) for i in range(n)]
        denom = [np.prod(np.delete(eval_A[i] - eval_A, i)) for i in range(n)]
        evec_A[k, :] = np.array(nominator) / np.array(denom)
    return evec_A



print('Det:',find_det(testmatrix))
eval_A = find_eigenvalues(testmatrix)
evec_A = find_eigenvectors(testmatrix, eval_A)
print(evec_A)
print(np.rint(evec_A))
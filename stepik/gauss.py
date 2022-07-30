import numpy as np


def main():
    n, m = map(int, input().split())
    matrix = np.array([list(map(int, input().split())) for i in range(n)])
    matrix_coef = np.array([matrix[i][:m] for i in range(n)])
    b = np.array([matrix[i][m] for i in range(n)])

    if np.linalg.matrix_rank(matrix) != np.linalg.matrix_rank(matrix_coef):
        print('NO')
    elif np.linalg.matrix_rank(matrix_coef) == m:
        print('YES')
        answer = np.linalg.solve(matrix_coef, b)
        print(' '.join(map(str, answer)))
    else:
        print('INF')


if __name__ == "__main__":
    main()

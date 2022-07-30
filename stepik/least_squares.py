import numpy as np


def main():
	n, m = map(int, input().split())
	matrix = np.array([list(map(int, input().split())) for i in range(n)])
	matrix_coef = np.array([[matrix[i][k] for i in range(n)] for k in range(m)])
	b = np.array([matrix[i][m] for i in range(n)])

	b_sla = np.array([np.dot(b, vector_coef) for vector_coef in matrix_coef])
	matrix_coef_sla = np.array([[np.dot(i, k) for i in matrix_coef] for k in matrix_coef])
	coef = np.linalg.solve(matrix_coef_sla, b_sla)
	print(' '.join(map(str, coef)))



if __name__ == "__main__":
	main()
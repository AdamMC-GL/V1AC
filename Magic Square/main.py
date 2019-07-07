import numpy as np
from math import sqrt


class MagicSquareSolver:
    def __init__(self, array, solve_immediate=True):
        self.matrix = array
        self.dim = array.ndim + 1
        self.comparison_matrix = self.get_comparison_matrix()

        self.derived_comparison_matrix = self.get_zero_matrix()
        self.inverse = None
        self.solution = None

        self.shape = self.matrix.shape[0]

        self.height = int(sqrt(self.shape))
        self.width = self.height
        self.solved = self.matrix
        self.vector_solved = None
        self.cached_solve = False

        self.validation = 0
        if solve_immediate:
            self.solve()

    @staticmethod
    def get_comparison_matrix():
        return np.array([
            [1, 1, 1, 0, 0, 0, 0, 0, 0, -1],  # H1
            [0, 0, 0, 1, 1, 1, 0, 0, 0, -1],  # H2
            [0, 0, 0, 0, 0, 0, 1, 1, 1, -1],  # H3
            [1, 0, 0, 1, 0, 0, 1, 0, 0, -1],  # V1
            [1, 0, 0, 0, 1, 0, 0, 0, 1, -1],  # L - R
            [0, 1, 0, 0, 1, 0, 0, 1, 0, -1],  # V2
            [0, 0, 1, 0, 1, 0, 1, 0, 0, -1],  # R - L
            [0, 0, 1, 0, 0, 1, 0, 0, 1, -1],  # V3
            [0, 0, 0, 0, 3, 0, 0, 0, 0, -1],  # Sum
        ])

    @staticmethod
    def get_zero_matrix():
        return np.zeros(shape=(9, 1))

    def solve_grid(self):
        for row in range(len(self.comparison_matrix) - 1):
            for column in range(len(self.comparison_matrix[row]) - 1):
                if self.matrix[column] is None:
                    continue

                self.derived_comparison_matrix[row] -= self.comparison_matrix[row][column] * self.matrix[column]
                self.comparison_matrix[row][column] = 0
        self.inverse = np.linalg.pinv(self.comparison_matrix)
        self.vector_solved = self.inverse.dot(self.derived_comparison_matrix)
        self.setup_solution_matrix()

    def setup_solution_matrix(self):
        for item in range(len(self.matrix) - 1):
            if self.matrix[item] is None:
                self.solved[item] = self.vector_solved[item][0]
        self.solved = (np.round(self.solved.astype(np.double)))
        self.solved.resize(self.width, self.height)

    def solve(self):
        if self.cached_solve:
            return self.solved
        self.solve_grid()
        self.cached_solve = True
        return self.solved


mss = MagicSquareSolver(np.array([
    None, 1, None,
    None, 5, None,
    None, None, 3,
]))

solved = mss.solve()

print(solved)

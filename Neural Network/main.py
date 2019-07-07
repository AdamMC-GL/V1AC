import json
import sys

try:
    if sys.argv[2]:
        cli = sys.argv[1]  # Acquiring the file name from our command line
except IndexError:
    cli = None


class Parser(object):
    init_matrix = None
    matrices = []

    def parse_layer_data(self):
        for layer in self.init_matrix:
            iter_matrix = []
            weights = self.init_matrix[layer]["weights"]
            output_layer_size = int(self.init_matrix[layer]["size_out"])

            for node_weights in weights:
                node = weights[node_weights]
                list_weights = [0] * int(output_layer_size)

                for weight in node:
                    weight_index = int(weight) - 1

                    list_weights[weight_index] = float(node[weight])

                iter_matrix.append(list_weights)
            self.matrices.append(iter_matrix)

        return self.matrices

    def init_file(self, file_name=None):
        file_found = False

        if file_name:
            try:
                self.init_matrix = json.load(open(file_name, 'r'))
                file_found = True
            except FileNotFoundError:
                file_name = None
                print("- Argument invalid -")
        if not file_name and not file_found:
            while True:
                try:
                    print("Insert the file name: ")
                    file_name = input(" ")
                    self.init_matrix = json.load(open(file_name, 'r'))
                    break
                except FileNotFoundError:
                    print("File not found, try again.")
        return self.parse_layer_data()


class NNMatrix(object):
    weight_factor = 1  # Implying that if we haven't changed the weight, a multiplication should be the squared.

    outcome = []
    iter_outcome = []
    left_bound_matrix = []
    right_bound_matrix = []

    def multiply(self, matrices):

        default_vector = [1, 1, 1, 1, 1]

        if len(matrices) == 1:
            return self.multiplication_execution(default_vector, matrices[0])

        prev_result = self.multiplication_execution(matrices[-2], matrices[-1])

        return self.multiplication_execution(default_vector, prev_result, True)

    @staticmethod
    def multiplication_execution(left_hand, right_hand, format_return=False):
        dot_result = []
        result_row = []

        if not isinstance(right_hand[0], list):
            right_hand = [right_hand]

        if not isinstance(left_hand[0], list):
            left_hand = [left_hand]

        for x in range(len(right_hand[0])):  # Preventing more zeroes than required to show
            result_row.append(0)

        for i in range(len(left_hand)):
            dot_result.append(result_row.copy())

        for l_rows in range(len(left_hand)):
            for cols in range(len(right_hand[0])):
                for r_row in range(len(right_hand)):
                    dot_result[l_rows][cols] += left_hand[l_rows][r_row] * right_hand[r_row][cols]

        if format_return:
            dot_result = dot_result[0]
            print(dot_result)
            return dot_result
        return dot_result


nnm = NNMatrix()

parser = Parser()

matrix = parser.init_file('example-2layer.json')
nnm.multiply(matrix)

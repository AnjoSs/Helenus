import csv

from UseCaseAnalyser_Class import ABCUseCaseAnalyser


class Tester:
    @staticmethod
    def test_correct_unambiguity_2(dfa):
        if sorted(dfa.states) == sorted(['A', 'B', 'B2', 'Aba', 'B2ab']):
            assert sorted(dfa.state_transition_matrix.matrix) == sorted(
                [[['a'], [], [], [], ['b']],
                 [[], ['b'], [], ['a'], []],
                 [[], [], ['b'], ['a'], []],
                 [['a'], [], [], [], ['b']],
                 [[], [], ['b'], ['a'], []]])
            return
        if sorted(dfa.states) == sorted(['A', 'B', 'B2', 'Aaa', 'B2bb']):
            assert sorted(dfa.state_transition_matrix.matrix) == sorted(
                [[[], [], ['b'], ['a'], []],
                 [['a'], ['b'], [], [], []],
                 [['a'], [], [], [], ['b']],
                 [[], [], ['b'], ['a'], []],
                 [['a'], [], [], [], ['b']]])
            return
        if sorted(dfa.states) == sorted(['A', 'B', 'B2', 'Aba', 'B2bb']):
            assert sorted(dfa.state_transition_matrix.matrix) == sorted(
                [[['a'], [], ['b'], [], []],
                 [[], ['b'], [], ['a'], []],
                 [[], [], [], ['a'], ['b']],
                 [['a'], [], ['b'], [], []],
                 [[], [], [], ['a'], ['b']]])
            return
        if sorted(dfa.states) == sorted(['A', 'B', 'B2', 'Aaa', 'B2ab']):
            assert sorted(dfa.state_transition_matrix.matrix) == sorted(
                [[[], [], [], ['a'], ['b']],
                 [['a'], ['b'], [], [], []],
                 [['a'], [], ['b'], [], []],
                 [[], [], [], ['a'], ['b']],
                 [['a'], [], ['b'], [], []]])
            return
        assert 0 == 1

    @staticmethod
    def test_correct_dfa_bpi11(dfa):
        print("Testing dfa")
        expected_input = []
        for letter in dfa.alphabet:
            expected_input.append(str(letter))
        for row in dfa.state_transition_matrix.matrix:
            actual_input = []
            for col in row:
                assert(len(col) < 2)
                if len(col) != 0:
                    actual_input.append(col[0])
            assert(sorted(expected_input) == sorted(actual_input))

    # expected trained matrix because generated with eventGen.py:
    #       1c  1b  0a  0c
    # 1c    0.6 0.2 0.2 0
    # 1b    0.4 0.3 0.3 0
    # 0a    0   0.1 0.7 0.2
    # 0c    0   0.2 0.2 0.6
    @staticmethod
    def test_correct_trained_matrix_abc(trained_matrix):
        for row in trained_matrix:
            percentage_sum = 0
            for col in row:
                percentage_sum += col[0]
            assert(round(percentage_sum, 3) == 1.0)

        assert(round(trained_matrix[0][0][0], 1) == 0.6)
        assert(round(trained_matrix[0][1][0], 1) == 0.2)
        assert(round(trained_matrix[0][2][0], 1) == 0.2)
        assert(round(trained_matrix[0][3][0], 1) == 0)
        assert(round(trained_matrix[1][0][0], 1) == 0.4)
        assert(round(trained_matrix[1][1][0], 1) == 0.3)
        assert(round(trained_matrix[1][2][0], 1) == 0.3)
        assert(round(trained_matrix[1][3][0], 1) == 0)
        assert(round(trained_matrix[2][0][0], 1) == 0)
        assert(round(trained_matrix[2][1][0], 1) == 0.1)
        assert(round(trained_matrix[2][2][0], 1) == 0.7)
        assert(round(trained_matrix[2][3][0], 1) == 0.2)
        assert(round(trained_matrix[3][0][0], 1) == 0)
        assert(round(trained_matrix[3][1][0], 1) == 0.2)
        assert(round(trained_matrix[3][2][0], 1) == 0.2)
        assert(round(trained_matrix[3][3][0], 1) == 0.6)

    @staticmethod
    def test_correct_trained_matrix_bpi11(trained_matrix, dfa):
        for row in trained_matrix:
            percentage_sum = 0
            for col in row:
                percentage_sum += col[0]
            assert(round(percentage_sum, 3) == 1.0 or percentage_sum == 0)

    @staticmethod
    def test_correct_trained_matrix_bpi19(trained_matrix):
        for row in trained_matrix:
            percentage_sum = 0
            for col in row:
                percentage_sum += col[0]
            assert (round(percentage_sum, 3) == 1.0 or percentage_sum == 0)

    @staticmethod
    def test_precision():
        pred_path = 'test/pred.csv'
        actual_path = 'test/actual.csv'
        with open(actual_path, 'w', newline='\n') as a:
            w = csv.writer(a)
            w.writerow(['a'])  # 1c -> 0a
            w.writerow(['b'])  # 0a -> 1b
            w.writerow(['b'])  # 1b -> 1b

        # correct prediction
        with open(pred_path, 'w', newline='\n') as p:
            w2 = csv.writer(p)
            w2.writerow(['1c', 'a', "0a", 2])
            w2.writerow(['0a', 'b', "1b", 1])
            w2.writerow(['1b', 'b', "1b", 0])

        analyser = ABCUseCaseAnalyser()
        analyser.get_dfa()
        precision = analyser.get_precision(actual_path, pred_path, 0, 2)
        assert(precision == 1.0)

        # semi correct prediction
        with open(pred_path, 'w', newline='\n') as p:
            w2 = csv.writer(p)
            w2.writerow(['1c', 'a', "0a", 1])
            w2.writerow(['0a', 'b', "1b", 1])
            w2.writerow(['1b', 'b', "1b", 0])

        analyser = ABCUseCaseAnalyser()
        analyser.get_dfa()
        precision = analyser.get_precision(actual_path, pred_path, 0, 2)
        assert (precision == 0.5)

        # wrong prediction
        with open(pred_path, 'w', newline='\n') as p:
            w2 = csv.writer(p)
            w2.writerow(['1c', 'a', "0a", 1])
            w2.writerow(['0a', 'b', "1b", 0])
            w2.writerow(['1b', 'b', "1b", 0])  # TODO dow we want to allow predictions of 0?

        analyser = ABCUseCaseAnalyser()
        analyser.get_dfa()
        precision = analyser.get_precision(actual_path, pred_path, 0, 2)
        assert (precision == 0.0)



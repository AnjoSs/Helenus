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
            assert(percentage_sum == 1.0)

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
    def test_correct_trained_matrix_bpi11(trained_matrix):
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

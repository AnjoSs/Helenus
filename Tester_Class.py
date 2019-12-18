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

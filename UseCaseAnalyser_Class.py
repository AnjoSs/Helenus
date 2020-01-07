import csv
import copy
import abc

# TODO: Use BPI challenge 2019 --> only 42 event types
from DFA_Class import DFA
from State_Transition_Matrix_Class import State_Transition_Matrix


class UseCaseAnalyser:
    def __init__(self):
        super().__init__()
        self.states = self.get_states()
        self.start_state = self.get_start_state()
        self.final_states = self.get_final_states()
        self.alphabet = self.get_alphabet()
        self.trained_matrix = {}

    @abc.abstractmethod
    def get_states(self):
        pass

    @abc.abstractmethod
    def get_final_states(self):
        pass

    @abc.abstractmethod
    def get_start_state(self):
        pass

    @abc.abstractmethod
    def get_matrix(self):
        pass

    @abc.abstractmethod
    def get_alphabet(self):
        pass

    def get_dfa(self):
        states = self.get_states()
        start_state = self.get_start_state()
        final_states = self.get_final_states()
        alphabet = self.get_alphabet()
        matrix = self.get_matrix()
        return DFA(states, start_state, alphabet, final_states, matrix)

    def train_matrix(self, dfa, data_path, training_count):
        # Copy original matrix + fill with 0
        matrix = copy.deepcopy(dfa.state_transition_matrix.matrix)
        for next_event in matrix:
            for col in next_event:
                col.clear()
                col.append(0)

        # replay log entries + count transitions
        with open(data_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)  # skip headline
            current_state = dfa.start_state[0]
            for i in range(0, training_count):
                next_event = next(csv_reader)
                next_state = dfa.delta(current_state, next_event)
                matrix[dfa.state_transition_matrix.state_list.index(current_state)][
                    dfa.state_transition_matrix.state_list.index(next_state)][0] += 1
                current_state = next_state

        # calculate percentage
        for next_event in matrix:
            for col in next_event:
                col[0] = col[0] / training_count

        self.trained_matrix = matrix
        return


"""
An UseCaseAnalyser especially for the BPI2011 challenge. With LTL: G(a -> Fb)
Special here: event types and alphabet are no the same thing.
We take event types from the log, e.g. "cea - tumormarker mbv meia" and take their index as alphabet.
"""


class BPIUseCaseAnalyser(UseCaseAnalyser):
    def __init__(self):
        super().__init__()
        self.a = "cea - tumormarker mbv meia"
        self.b = "squamous cell carcinoma mbv eia"
        self.event_types = self.get_event_types()

    def get_states(self):
        return ["A", "B"]

    def get_final_states(self):
        return ["B"]

    def get_start_state(self):
        return ["B"]

    def get_event_types(self):
        with open('data/hospital_log.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)
            event_types = []
            while len(event_types) < 8:
                row = next(csv_reader)
                if row[1] not in event_types:
                    event_types.append(row[1])

            # TODO change back to this if all event types wanted:
            # for row in csv_reader:
            #    if row[1] not in event_types:
            #        event_types.append(row[1])
            # if 'squamous' in row[1]:
            #    print(row[1])
            if self.a not in event_types:
                event_types.append(self.a)
            if self.b not in event_types:
                event_types.append(self.b)

        # print("Event Types: " + str(event_types))
        # print("Event Count: " + str(count))
        return event_types

    def get_alphabet(self):
        # TODO: ATTENTION: only taking a few event types!
        return range(0, 10)

    def get_matrix(self):
        row_AA = []
        row_BB = []
        for event in self.event_types:
            if event != self.b:
                row_AA.append(str(self.event_types.index(event)))
            if event != self.a:
                row_BB.append(str(self.event_types.index(event)))

        state_transition_matrix = [[row_AA, [str(self.event_types.index(self.b))]],
                                   [row_BB, [str(self.event_types.index(self.a))]]]
        return State_Transition_Matrix(self.states, self.alphabet, state_transition_matrix)

    def train_matrix(self, dfa, data_path, training_count):
        # Copy original matrix + fill with 0
        matrix = copy.deepcopy(dfa.state_transition_matrix.matrix)
        for row in matrix:
            for col in row:
                col.clear()
                col.append(0)

        # replay training_count log entries + count transitions
        with open(data_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)
            current_state = dfa.start_state[0]
            actual_training_count = 0
            for i in range(0, training_count):
                row = next(csv_reader)
                if row[1] in self.event_types:
                    actual_training_count += 1  # TODO: necessary because not all event types taken
                    next_state = dfa.delta(current_state, str(self.event_types.index(row[1])))
                    matrix[dfa.state_transition_matrix.state_list.index(current_state)][
                        dfa.state_transition_matrix.state_list.index(next_state)][0] += 1
                    current_state = next_state

        # calculate percentage
        for row in matrix:
            for col in row:
                col[0] = col[0] / actual_training_count

        self.trained_matrix = matrix
        return


class ABCUseCaseAnalyser(UseCaseAnalyser):
    def __init__(self):
        super().__init__()

    def get_states(self):
        pass  # TODO

    def get_final_states(self):
        pass  # TODO

    def get_start_state(self):
        pass  # TODO

    def get_alphabet(self):
        # TODO belongs to what LTL?
        return ['a', 'b', 'c']

    def get_matrix(self):
        # TODO belongs to what LTL?
        return

    def train_matrix(self, dfa, data_path, training_count):
        pass  # TODO

import csv
import copy
import abc
import numpy as np

from DFA_Class import DFA
from State_Transition_Matrix_Class import State_Transition_Matrix


class UseCaseAnalyser:
    def __init__(self):
        super().__init__()
        self.states = self.get_states()
        self.start_state = self.get_start_state()
        self.final_states = self.get_final_states()
        self.alphabet = self.get_alphabet()
        self.initial_matrix = self.get_matrix()
        self.dfa = self.get_dfa()
        self.trained_matrix = np.array([])
        self.delimiter = ';'
        self.depth_matrices = {}
        self.depth_final_state_probability = {}

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

    @abc.abstractmethod
    def access_event(self, row):
        pass

    @abc.abstractmethod
    def access_instance(self, row):
        pass

    def get_dfa(self):
        return DFA(self.states, self.start_state, self.alphabet, self.final_states, self.initial_matrix)

    def train_matrix(self, dfa, data_path, training_count, max_distance, has_header, has_instances=False):
        # Copy original matrix + fill with 0
        # plus: save for each state how often it was visited to compute percentages
        matrix = copy.deepcopy(dfa.state_transition_matrix.matrix)
        state_visits = []
        instance_states = {}
        for row in matrix:
            state_visits.append(0)
            for i in range(0, len(row)):
                row[i] = 0

        # replay log entries + count transitions
        with open(data_path, encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
            if has_header:
                next(csv_reader)
            current_state = dfa.start_state[0]
            for i in range(0, training_count):
                next_row = next(csv_reader)
                if has_instances:
                    if self.access_instance(next_row) in instance_states.keys():
                        current_state = instance_states.get(self.access_instance(next_row))
                    else:
                        current_state = dfa.start_state[0]
                current_state_idx = dfa.state_transition_matrix.state_list.index(current_state)
                state_visits[current_state_idx] += 1
                next_event = self.access_event(next_row)
                next_state = dfa.delta_np(current_state, next_event)
                matrix[current_state_idx][dfa.state_transition_matrix.state_list.index(next_state)] += 1
                current_state = next_state
                if has_instances:
                    instance_states[self.access_instance(next_row)] = current_state

        # calculate percentage
        for row_idx, row in enumerate(matrix):
            for i in range(0, len(row)):
                if state_visits[row_idx] != 0:
                    row[i] = row[i] / state_visits[row_idx]

        self.trained_matrix = np.array(matrix)
        self.compute_depth_matrices(max_distance)
        return

    def compute_depth_matrices(self, max_distance):
        final_states_vector = np.array([[]])
        for state in self.states:
            if state in self.final_states:
                final_states_vector = np.concatenate((final_states_vector, np.array([[1]])), axis=1)
            else:
                final_states_vector = np.concatenate((final_states_vector, np.array([[0]])), axis=1)
        final_states_vector = final_states_vector.T
        nulling_matrix = np.identity(len(self.states))
        for idx, state in enumerate(self.states):
            if state in self.final_states:
                nulling_matrix[idx][idx] = 0

        for depth in range(1, max_distance + 1):
            if depth == 1:
                depth_matrix = self.trained_matrix
            else:
                depth_matrix = self.depth_matrices[depth - 1].dot(self.trained_matrix)
            self.depth_final_state_probability[depth] = depth_matrix.dot(final_states_vector)
            self.depth_matrices[depth] = depth_matrix.dot(nulling_matrix)

    def predict_matrix(self, dfa, data_path, log_begin, log_end, result_path, max_distance, threshold):
        with open(data_path, encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
            current_state = dfa.start_state[0]

            # skip unwanted log entries
            for i in range(0, log_begin):
                next(csv_reader)

            with open(result_path, 'w', newline='\n', encoding='windows-1252') as resultFile:
                csv_writer = csv.writer(resultFile, delimiter=self.delimiter)
                if log_end is None:
                    for current_event in csv_reader:
                        new_state = dfa.delta_np(current_state, self.access_event(current_event))

                        # iterate over events and predict the shortest path that leads to an accepting state
                        # with p > threshold
                        spread = self.find_spread(new_state, max_distance, threshold)
                        # edge case for small dataset
                        if spread is None:
                            spread = -1

                        csv_writer.writerow([current_state, self.access_event(current_event), new_state, spread])
                        current_state = new_state
                else:
                    for i in range(log_begin, log_end):
                        current_event = next(csv_reader)
                        new_state = dfa.delta_np(current_state, self.access_event(current_event))

                        # iterate over events and predict the shortest path that leads to an accepting state
                        # with p > threshold
                        spread = self.find_spread(new_state, max_distance, threshold)
                        # edge case for small dataset
                        if spread is None:
                            spread = -1

                        csv_writer.writerow([current_state, self.access_event(current_event), new_state, spread])
                        current_state = new_state
        return

    def find_spread(self, current_state, max_distance, threshold):
        if current_state in self.final_states:
            return 0
        prob = 0
        current_state_idx = self.states.index(current_state)
        for possible_spread in range(1, max_distance + 1):
            prob += self.depth_final_state_probability[possible_spread][current_state_idx]
            if prob >= threshold:
                return possible_spread
        return -1

    def get_precision(self, actual_data_path, predicted_data_path, actual_log_begin, predicted_log_begin,
                      predicted_log_end, max_spread):
        with open(predicted_data_path, encoding='windows-1252') as predicted_file:
            precision_score = []
            predicted_reader = csv.reader(predicted_file, delimiter=self.delimiter)
            # skip to log_begin position
            for i in range(0, predicted_log_begin):
                next(predicted_reader)
            file_length = 0
            with open(predicted_data_path, encoding='windows-1252') as f:
                for r in csv.reader(f):
                    file_length += 1
            if predicted_log_end is None:
                predicted_log_end = file_length
            # check correctness of predictions
            for i in range(predicted_log_begin, predicted_log_end):
                predicted_row = next(predicted_reader)
                current_state = predicted_row[2]
                predicted_spread = int(predicted_row[3])
                # compare prediction spread with actual spread
                with open(actual_data_path, encoding='windows-1252') as actual_file:
                    actual_reader = csv.reader(actual_file, delimiter=self.delimiter)
                    # skip to actual_log_begin position
                    for j in range(0, actual_log_begin + i):
                        next(actual_reader)
                    event_leading_to_current_state = self.access_event(next(actual_reader))
                    assert (event_leading_to_current_state == int(predicted_row[1]))
                    # case for prediction that final state is not reached in next max_spread events
                    if predicted_spread == -1:
                        prediction_correct = 1
                        forecast_end = min(max_spread, file_length - i - 1)
                        for j in range(0, forecast_end):
                            next_row = next(actual_reader)
                            next_event = self.access_event(next_row)
                            actual_next_state = self.dfa.delta_np(current_state, next_event)
                            if actual_next_state in self.dfa.final_states:
                                prediction_correct = 0
                                break
                    elif predicted_spread == 0:
                        if current_state in self.final_states:
                            prediction_correct = 1
                        else:
                            print("error")
                    else:
                        prediction_correct = 0
                        # check for predicted_spread many actual events if they lead to a final state or not
                        forecast_end = min(max_spread, file_length - i - 1)
                        for j in range(0, forecast_end):
                            next_row = next(actual_reader)
                            next_event = self.access_event(next_row)
                            actual_next_state = self.dfa.delta_np(current_state, next_event)
                            if actual_next_state in self.dfa.final_states:
                                prediction_correct = 1
                                break
                    precision_score.append(prediction_correct)
            return sum(precision_score) / len(precision_score)


"""
An UseCaseAnalyser especially for the BPI2011 challenge. With LTL: G(a -> Fb)
Special here: event types and alphabet are not the same thing.
We take event types from the log, e.g. "cea - tumormarker mbv meia" and take their index as alphabet.
"""


class BPIUseCaseAnalyser(UseCaseAnalyser):
    def __init__(self):
        self.a = "cea - tumormarker mbv meia"
        self.b = "squamous cell carcinoma mbv eia"
        self.event_types = self.get_event_types()
        super().__init__()

    def get_states(self):
        return ["A", "B"]

    def get_final_states(self):
        return ["B"]

    def get_start_state(self):
        return ["B"]

    def get_event_types(self):
        with open('data/hospital_log.csv', encoding='windows-1252') as csv_file:
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
        return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def get_matrix(self):
        row_AA = []
        row_BB = []
        for event_idx, event in enumerate(self.event_types):
            if event != self.b:
                row_AA.append(str(event_idx))
            if event != self.a:
                row_BB.append(str(event_idx))

        state_transition_matrix = [[row_AA, [str(self.event_types.index(self.b))]],
                                   [[str(self.event_types.index(self.a))], row_BB]]
        return State_Transition_Matrix(self.states, self.alphabet, state_transition_matrix)

    def access_event(self, row):
        if row[1] in self.event_types:
            return str(self.event_types.index(row[1]))
        else:
            return

    def train_matrix(self, dfa, data_path, training_count):
        # Copy original matrix + fill with 0
        # plus: save for each state how often it was visited to compute percentages
        matrix = copy.deepcopy(dfa.state_transition_matrix.matrix)
        state_visits = []
        for row in matrix:
            state_visits.append(0)
            for col in row:
                col.clear()
                col.append(0)

        # replay training_count log entries + count transitions
        with open(data_path, encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)
            current_state = dfa.start_state[0]
            current_state_idx = dfa.state_transition_matrix.state_list.index(current_state)
            for i in range(0, training_count):
                row = next(csv_reader)
                if row[1] in self.event_types:
                    state_visits[current_state_idx] += 1
                    next_state = dfa.delta_np(current_state, str(self.event_types.index(row[1])))
                    matrix[current_state_idx][dfa.state_transition_matrix.state_list.index(next_state)][0] += 1
                    current_state = next_state

        # calculate percentage
        for row_idx, row in enumerate(matrix):
            for col in row:
                if state_visits[row_idx] != 0:
                    col[0] = col[0] / state_visits[row_idx]

        self.trained_matrix = matrix
        return

    def predict_matrix(self, dfa, data_path, log_begin, log_end, result_path, max_distance, threshold):
        with open(data_path, encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
            next(csv_reader)
            current_state = dfa.start_state[0]

            # skip unwanted log entries
            for i in range(0, log_begin):
                next(csv_reader)

            with open(result_path, 'w', newline='\n', encoding='windows-1252') as resultFile:
                csv_writer = csv.writer(resultFile, delimiter=self.delimiter)
                for i in range(log_begin, log_end):
                    current_event = next(csv_reader)
                    if self.access_event(current_event) in self.alphabet:
                        new_state = dfa.delta_np(current_state, self.access_event(current_event))

                        spread = self.find_spread(current_state, max_distance, threshold)

                        csv_writer.writerow([current_state, self.access_event(current_event), new_state, spread])
                        current_state = new_state
        return


"""
LTL: G(a -> Fb) with alphabet [a,b,c]
Input case already is of order 1.
"""


class ABCUseCaseAnalyser(UseCaseAnalyser):
    def __init__(self):
        super().__init__()

    def get_states(self):
        return ["1c", "1b", "0a", "0c"]

    def get_final_states(self):
        return ["1c", "1b"]

    def get_start_state(self):
        return ["1c"]

    def get_alphabet(self):
        return ['a', 'b', 'c']

    def access_event(self, row):
        return row[0]

    #       1c  1b  0a  0c
    # 1c    c   b   a
    # 1b    c   b   a
    # 0a        b   a   c
    # 0c        b   a   c
    def get_matrix(self):
        matrix = [[["c"], ["b"], ["a"], []],
                  [["c"], ["b"], ["a"], []],
                  [[], ["b"], ["a"], ["c"]],
                  [[], ["b"], ["a"], ["c"]]]
        return State_Transition_Matrix(self.states, self.alphabet, matrix)


"""
BPI 2019 Challenge
LTL: G('Record Invoice Receipt' → F'Clear Invoice') = G(a --> Fb)
initial order 0
"""


class BPI19UseCaseAnalyser(UseCaseAnalyser):
    def __init__(self):
        self.a = 'Record Invoice Receipt'
        self.b = 'Clear Invoice'
        self.event_types = self.get_event_types()
        super().__init__()
        self.delimiter = ','

    def get_states(self):
        return ["no", "yes"]

    def get_final_states(self):
        return ["yes"]

    def get_start_state(self):
        return ["yes"]

    def get_matrix(self):
        cell_no_no = []
        cell_yes_yes = []
        for event in self.event_types:
            if event != self.b:
                cell_no_no.append(self.event_types.index(event) + 1)
            if event != self.a:
                cell_yes_yes.append(self.event_types.index(event) + 1)
        state_transition_matrix = [[cell_no_no, [self.event_types.index(self.b) + 1]],
                                   [[self.event_types.index(self.a) + 1], cell_yes_yes]]
        return State_Transition_Matrix(self.states, self.alphabet, state_transition_matrix)

    def get_alphabet(self):
        index_alphabet = list()
        for i in range(0, len(self.event_types)):
            index_alphabet.append(i + 1)
        return index_alphabet

    def access_event(self, row):
        return self.event_types.index(row[19]) + 1

    def access_instance(self, row):
        return row[15]

    @staticmethod
    def get_event_types():
        with open('data/bpi19_cleaned.csv', encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            event_types = []
            count = 0
            for row in csv_reader:
                if row[19] not in event_types:
                    event_types.append(row[19])
                    count += 1

        return event_types


class BPI19FinallyAnalyser(BPI19UseCaseAnalyser):
    def __init__(self):
        super().__init__()
        self.a = 'Clear Invoice'
        self.delimiter = ','

    def get_start_state(self):
        return ["no"]

    def get_matrix(self):
        cell_no_no = []
        cell_yes_yes = []
        for event in self.event_types:
            if event != self.a:
                cell_no_no.append(self.event_types.index(event) + 1)
            cell_yes_yes.append(self.event_types.index(event) + 1)
        state_transition_matrix = [[cell_no_no, [self.event_types.index(self.a) + 1]],
                                   [[], cell_yes_yes]]
        return State_Transition_Matrix(self.states, self.alphabet, state_transition_matrix)


class FinalState:
    def __init__(self, p, s):
        self.p = p
        self.s = s


class QueueState:
    def __init__(self, index, distance, probability):
        self.i = index
        self.d = distance
        self.p = probability


"""
LTL: G(m -> Fs) with alphabet [m,s,c]
"""


class MateUseCaseAnalyser(UseCaseAnalyser):
    def __init__(self):
        super().__init__()

    def get_states(self):
        return ['1', '0']

    def get_final_states(self):
        return ['1']

    def get_start_state(self):
        return ['1']

    def get_alphabet(self):
        return ['m', 's', 'c']

    def access_event(self, row):
        return row[0]

    #     1     0
    # 1   s,c   m
    # 0   s    m,c
    def get_matrix(self):
        matrix = [[['s', 'c'], ['m']],
                  [['s'], ['m', 'c']]]
        return State_Transition_Matrix(self.states, self.alphabet, matrix)


""" LTL: F'calculate final price' """
class AutoUseCaseAnalyser(UseCaseAnalyser):
    def __init__(self):
        self.actual_alphabet = []
        super().__init__()
        self.delimiter = ','

    def get_states(self):
        return ['0', '1']

    def get_final_states(self):
        return ['1']

    def get_start_state(self):
        return ['0']

    def get_alphabet(self):
        alphabet = []
        with open('data/auto.csv') as f:
            r = csv.reader(f, delimiter=',')
            for row in r:
                if row[1] not in alphabet:
                    alphabet.append(row[1])
        self.actual_alphabet = alphabet
        index_alphabet = list()
        for i in range(0, len(alphabet)):
            index_alphabet.append(i + 1)
        return index_alphabet

    def access_event(self, row):
        return self.actual_alphabet.index(row[1]) + 1

    def access_instance(self, row):
        return row[0]

    #     0     1
    # 0   *\x   x
    # 1   -    `*
    def get_matrix(self):
        x = self.actual_alphabet.index(" \'calculate final price\'") + 1
        except_x = []
        for a in self.alphabet:
            if a != x:
                except_x.append(a)
        matrix = [[except_x, [x]],
                  [[], copy.deepcopy(self.alphabet)]]
        return State_Transition_Matrix(self.states, self.alphabet, matrix)

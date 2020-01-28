import csv
import copy
import abc

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
        self.trained_matrix = {}
        self.delimiter = ';'

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

    def get_dfa(self):
        return DFA(self.states, self.start_state, self.alphabet, self.final_states, self.initial_matrix)

    def train_matrix(self, dfa, data_path, training_count):
        # Copy original matrix + fill with 0
        # plus: save for each state how often it was visited to compute percentages
        matrix = copy.deepcopy(dfa.state_transition_matrix.matrix)
        state_visits = []
        for event in matrix:
            state_visits.append(0)
            for col in event:
                col.clear()
                col.append(0)

        # replay log entries + count transitions
        with open(data_path, encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
            next(csv_reader)  # skip headline
            current_state = dfa.start_state[0]
            for i in range(0, training_count):
                state_visits[dfa.state_transition_matrix.state_list.index(current_state)] += 1
                next_event = self.access_event(next(csv_reader))
                next_state = dfa.delta(current_state, next_event)
                matrix[dfa.state_transition_matrix.state_list.index(current_state)][
                    dfa.state_transition_matrix.state_list.index(next_state)][0] += 1
                current_state = next_state

        # calculate percentage
        for row in matrix:
            for col in row:
                if state_visits[matrix.index(row)] != 0:
                    col[0] = col[0] / state_visits[matrix.index(row)]

        self.trained_matrix = matrix
        return

    def predict_matrix(self, dfa, data_path, log_begin, log_end, result_path, max_distance, threshold):
        with open(data_path, encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
            current_state = dfa.start_state[0]

            # skip unwanted log entries
            for i in range(0, log_begin):
                next(csv_reader)

            with open(result_path, 'w', newline='\n', encoding='windows-1252') as resultFile:
                csv_writer = csv.writer(resultFile, delimiter=self.delimiter)
                for i in range(log_begin, log_end):
                    current_event = next(csv_reader)
                    new_state = dfa.delta(current_state, self.access_event(current_event))

                    # iterate over events and predict the shortest path that leads to an accepting state
                    # with p > threshold
                    spread = self.find_spread3(new_state, max_distance, threshold)
                    # edge case for small dataset
                    if spread is None:
                        spread = -1

                    csv_writer.writerow([current_state, self.access_event(current_event), new_state, spread])
                    current_state = new_state
        return

    def find_spread3(self, current_state, max_distance, threshold):
        queue = []
        final_state_probs = {}
        for f in self.final_states:
            final_state_probs[self.states.index(f)] = FinalState(0.0, 0)
        current_state_index = self.states.index(current_state)
        # Step 1: Add all level 1 states to queue
        for neighbor_index, neighbor_prob in enumerate(self.trained_matrix[current_state_index]):
            if neighbor_prob[0] != 0:
                if self.states[neighbor_index] in self.final_states and neighbor_prob[0] > threshold:
                    return 1
                if neighbor_index in final_state_probs.keys():
                    final_state_probs[neighbor_index].p += neighbor_prob[0]
                    final_state_probs[neighbor_index].s = 1
                queue.append(QueueState(neighbor_index, 1, neighbor_prob[0]))
        # Step 2: Successively browse higher distances
        while queue:
            e = queue[0]
            queue.remove(e)
            # Unsuccessful ending condition
            if e.d > max_distance:
                return -1
            for neighbor_index, neighbor_prob in enumerate(self.trained_matrix[e.i]):
                if neighbor_prob[0] != 0:
                    if neighbor_index in final_state_probs.keys():
                        final_state_probs[neighbor_index].p += e.p * neighbor_prob[0]
                        final_state_probs[neighbor_index].s = e.d + 1
                        # Successful ending condition
                        if final_state_probs[neighbor_index].p > threshold:
                            return final_state_probs[neighbor_index].s
                    queue.append(QueueState(neighbor_index, e.d + 1, e.p * neighbor_prob[0]))

    def get_precision(self, actual_data_path, predicted_data_path, actual_log_begin, predicted_log_begin,
                      predicted_log_end, max_spread):
        with open(predicted_data_path, encoding='windows-1252') as predicted_file:
            precision_score = []
            predicted_reader = csv.reader(predicted_file, delimiter=self.delimiter)
            # skip to log_begin position
            for i in range(0, predicted_log_begin):
                next(predicted_reader)
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
                    assert (event_leading_to_current_state == predicted_row[1])
                    # case for prediction that final state is not reached in next max_spread events
                    if predicted_spread == -1:
                        prediction_correct = 1
                        for j in range(0, max_spread):
                            next_row = next(actual_reader)
                            next_event = self.access_event(next_row)
                            actual_next_state = self.dfa.delta(current_state, next_event)
                            if actual_next_state in self.dfa.final_states:
                                prediction_correct = 0
                                break
                    elif predicted_spread == 0:
                        next_row = next(actual_reader)
                        next_event = self.access_event(next_row)  # next?event == predicted?row[1]
                        actual_next_state = self.dfa.delta(current_state, next_event)
                        if actual_next_state in self.dfa.final_states:
                            prediction_correct = 1
                    else:
                        prediction_correct = 0
                        # check for predicted_spread many actual events if they lead to a final state or not
                        for j in range(0, predicted_spread):
                            next_row = next(actual_reader)
                            next_event = self.access_event(next_row)
                            actual_next_state = self.dfa.delta(current_state, next_event)
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
        for event in self.event_types:
            if event != self.b:
                row_AA.append(str(self.event_types.index(event)))
            if event != self.a:
                row_BB.append(str(self.event_types.index(event)))

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
            for i in range(0, training_count):
                row = next(csv_reader)
                if row[1] in self.event_types:
                    state_visits[dfa.state_transition_matrix.state_list.index(current_state)] += 1
                    next_state = dfa.delta(current_state, str(self.event_types.index(row[1])))
                    matrix[dfa.state_transition_matrix.state_list.index(current_state)][
                        dfa.state_transition_matrix.state_list.index(next_state)][0] += 1
                    current_state = next_state

        # calculate percentage
        for row in matrix:
            for col in row:
                if state_visits[matrix.index(row)] != 0:
                    col[0] = col[0] / state_visits[matrix.index(row)]

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
                        new_state = dfa.delta(current_state, self.access_event(current_event))

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
LTL: F('SRM: Transfer Failed (E.Sys.)') == Fa
initial order 0
"""


class BPI19UseCaseAnalyser(UseCaseAnalyser):
    def __init__(self):
        self.a = 'SRM: Transfer Failed (E.Sys.)'
        self.event_types = self.get_event_types()
        super().__init__()
        self.delimiter = ','

    def get_states(self):
        return ["no", "yes"]

    def get_final_states(self):
        return ["yes"]

    def get_start_state(self):
        return ["no"]

    def get_matrix(self):
        cell_no_no = []
        cell_yes_yes = []
        for event in self.event_types:
            if event != self.a:
                cell_no_no.append(str(self.event_types.index(event)))
            cell_yes_yes.append(str(self.event_types.index(event)))
        state_transition_matrix = [[cell_no_no, [str(self.event_types.index(self.a))]],
                                   [[], cell_yes_yes]]
        return State_Transition_Matrix(self.states, self.alphabet, state_transition_matrix)

    def get_alphabet(self):
        return self.event_types

    def access_event(self, row):
        return str(self.event_types.index(row[19]))

    @staticmethod
    def get_event_types():
        with open('data/bpi19.csv', encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            event_types = []
            count = 0
            for row in csv_reader:
                if row[19] not in event_types:
                    event_types.append(row[19])
                    count += 1

        return event_types


class FinalState:
    def __init__(self, p, s):
        self.p = p
        self.s = s


class QueueState:
    def __init__(self, index, distance, probability):
        self.i = index
        self.d = distance
        self.p = probability

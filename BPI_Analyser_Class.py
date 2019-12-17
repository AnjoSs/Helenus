import csv
import copy


class BPIAnalyser:
    def __init__(self):
        self.event_types = self.get_event_types()
        self.trained_matrix = {}

    def get_event_types(self):
        with open('data/hospital_log.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)
            event_types = []
            while len(event_types) < 8:
                row = next(csv_reader)
                if row[1] not in event_types:
                    event_types.append(row[1])

            # TODO change back to this:
            #for row in csv_reader:
            #    if row[1] not in event_types:
            #        event_types.append(row[1])
                    # if 'squamous' in row[1]:
                    #    print(row[1])
            a = "cea - tumormarker mbv meia"
            b = "squamous cell carcinoma mbv eia"
            if a not in event_types:
                event_types.append(a)
            if b not in event_types:
                event_types.append(b)

        print("Event Types: " + str(event_types))
        #print("Event Count: " + str(count))
        self.event_types = event_types
        return event_types

    def get_matrix_GaFb(self, a, b):
        row_AA = []
        row_BB = []
        for event in self.event_types:
            if event != b:
                row_AA.append(str(self.event_types.index(event)))
            if event != a:
                row_BB.append(str(self.event_types.index(event)))

        state_transition_matrix = [[row_AA, [str(self.event_types.index(b))]], [row_BB, [str(self.event_types.index(a))]]]
        return state_transition_matrix

    def get_alphabet(self):
        # TODO: ATTENTION: only taking a few event types!
        return range(0, 10)

    def train_matrix(self, dfa):
        # Copy original matrix + fill with 0
        matrix = copy.deepcopy(dfa.state_transition_matrix.matrix)
        for row in matrix:
            for col in row:
                col.clear()
                col.append(0)

        # replay 75000 log entries + count transitions
        with open('data/hospital_log.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader)
            current_state = dfa.start_state[0]
            training_count = 75000
            actual_training_count = 0
            for i in range(0, training_count):
                row = next(csv_reader)
                if row[1] in self.event_types:
                    actual_training_count += 1  # TODO: necessary because not all event types taken
                    next_state = dfa.delta(current_state, str(self.event_types.index(row[1])))
                    matrix[dfa.states.index(current_state)][dfa.states.index(next_state)][0] += 1
                    current_state = next_state

        # calculate percentage
        for row in matrix:
            for col in row:
                col[0] = col[0] / actual_training_count

        self.trained_matrix = matrix
        return

import csv

from DFA_Class import DFA
from State_Transition_Matrix_Class import State_Transition_Matrix

with open('data/hospital_log.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)
    event_types = []
    count = 0
    for row in csv_reader:
        count += 1
        if row[1] not in event_types:
            event_types.append(row[1])
            # if 'squamous' in row[1]:
            #    print(row[1])

print(len(event_types))
print("Event Count: " + str(count))

a = "cea - tumormarker mbv meia"
b = "squamous cell carcinoma mbv eia"

states = ["A", "B"]
start_state = ["B"]
final_states = ["B"]

row_AA = []
row_BB = []
for event in event_types:
    if event != b:
        row_AA.append(event_types.index(event))
    if event != a:
        row_BB.append(event_types.index(event))

state_transition_matrix = [[row_AA, [event_types.index(b)]], [row_BB, [event_types.index(a)]]]
alphabet = range(0, len(event_types))


matrix = State_Transition_Matrix(states, alphabet, state_transition_matrix)
dfa = DFA(states, start_state, alphabet, final_states, matrix)
dfa.increase_unambiguity(1)


# TRAINING
# Copy original matrix + fill with 0

matrix = dfa.state_transition_matrix
for row in matrix:
    for col in row:
        col.removeAll()
        col.append(0)

# replay 1000 log entries + count transitions
with open('data/hospital_log.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)
    current_state = start_state
    training_count = 75000
    for i in range(0, training_count):
        row = next(csv_reader)
        matrix[current_state[0]][event_types[row[1]]][0] += 1

for row in matrix:
    for col in matrix:
        col[0] = col[0] / training_count

print(matrix)

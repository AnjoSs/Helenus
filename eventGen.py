import csv
import random
import numpy

class Generator:
    @staticmethod
    def generate_mate_use_case():
        events = ["Wrote a Line of Code",
                  "Drank Mate",
                  "Got Caffeine Shock"]
        log = []

        for i in range(0, 100):
            log.append(random.choice(events))

        print(log)
        print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')

    # should map on MC with order 1: (0 means non/accepting, 1 accepting)
    # LTL: G(a -> Fb)

    #       1c  1b  0a  0c
    # 1c    0.6 0.2 0.2 0
    # 1b    0.4 0.3 0.3 0
    # 0a    0   0.1 0.7 0.2
    # 0c    0   0.2 0.2 0.6
    @staticmethod
    def generate_abc_use_case(max_file_length):
        alphabet = ['a', 'b', 'c']
        with open('data/abc.csv', 'w+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            file_length = 0
            last_char = numpy.random.choice(alphabet)
            while file_length < max_file_length:
                csv_writer.writerow(last_char)
                if last_char == 'a':
                    last_char = numpy.random.choice(alphabet, p=[0.7, 0.1, 0.2])
                elif last_char == 'b':
                    last_char = numpy.random.choice(alphabet, p=[0.3, 0.3, 0.4])
                elif last_char == 'c':
                    last_char = numpy.random.choice(alphabet, p=[0.2, 0.2, 0.6])
                file_length += 1

    @staticmethod
    def gen_auto_data():
        with open('data/auto.csv') as csv_file:
            r = csv.reader(csv_file, delimiter=',')
            while True:
                n = next(r)
                if n[0] == '1':
                    print(n)

    # Events: m - drink mate, s - get shock, c - code
    # LTL: G(m --> Fs)
    @staticmethod
    def gen_mate_data(max_file_length):
        alphabet = ['m', 's', 'c']
        with open('data/mate.csv', 'w+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            file_length = 0
            last_event = random.choice(alphabet)
            s_to_last_event = random.choice(alphabet)
            while file_length < max_file_length:
                if s_to_last_event == 'm' and last_event == 'm':
                    new_event = numpy.random.choice(alphabet, p=[0.1, 0.8, 0.1])
                elif s_to_last_event == 'c' and last_event == 'c':
                    new_event = numpy.random.choice(alphabet, p=[0.25, 0.05, 0.7])
                else:
                    new_event = numpy.random.choice(alphabet, p=[0.5, 0.5, 0.0])
                s_to_last_event = last_event
                last_event = new_event
                csv_writer.writerow(new_event)
                file_length += 1


# Generator.generate_abc_use_case(100000)
# Generator.gen_auto_data()
Generator.gen_mate_data(100000)

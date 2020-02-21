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
    def gen_big_mate_data(max_file_length):
        alphabet = ['m', 's', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
        with open('data/mate.csv', 'w+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            file_length = 0
            last_event = random.choice(alphabet)
            s_to_last_event = random.choice(alphabet)
            while file_length < max_file_length:
                if s_to_last_event == 'm' and last_event == 'm':
                    new_event = numpy.random.choice(alphabet, p=[0.1, 0.8, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
                elif s_to_last_event == 'c' and last_event == 'c':
                    new_event = numpy.random.choice(alphabet, p=[0.25, 0.05, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
                else:
                    new_event = numpy.random.choice(alphabet)
                s_to_last_event = last_event
                last_event = new_event
                csv_writer.writerow(new_event)
                file_length += 1

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
                    new_event = numpy.random.choice(alphabet,
                                                    p=[0.1, 0.8, 0.1])
                elif s_to_last_event == 'c' and last_event == 'c':
                    new_event = numpy.random.choice(alphabet,
                                                    p=[0.25, 0.05, 0.7])
                else:
                    new_event = numpy.random.choice(alphabet)
                s_to_last_event = last_event
                last_event = new_event
                csv_writer.writerow(new_event)
                file_length += 1

    @staticmethod
    def bpi19_one_instances():
        with open("data/bpi19_cleaned.csv") as f:
            r = csv.reader(f, delimiter=',')
            next(r)  # skip headline
            instances = []
            for i in range(0, 5000):  # TODO revalidate training size
                next(r)
            count = 0
            for row in r:
                if len(instances) >= 100:
                    break
                if row[15] not in instances:
                    instances.append(row[15])
                    open("data/instances/" + str(count) + ".csv", 'w+', newline='')
                    count += 1
        with open("data/bpi19_cleaned.csv") as f:
            r = csv.reader(f, delimiter=',')
            next(r)  # skip headline
            for row in r:
                if row[15] in instances:
                    with open("data/instances/" + str(instances.index(row[15])) + ".csv", 'a', newline='') as g:
                        w = csv.writer(g, delimiter=',')
                        w.writerow(row)

            # # lookup index, write to file
            # for i in range(0, 100):
            #     with open("data/instances/" + str(i) + ".csv", 'w+', newline='') as g:
            #         next(r)  # skip headline
            #         w = csv.writer(g, delimiter=',')
            #         first = next(r)
            #         instances.append(first[15])
            #         instance = first[15]
            #         for row in r:
            #             if instance == row[15]:
            #                 w.writerow(row[19])

    @staticmethod
    def bpi19_cleanup():
        with open("data/bpi19.csv") as f:
            r = csv.reader(f, delimiter=',')
            with open("data/bpi19_cleaned_one_instance.csv", 'w+', newline='') as g:
                w = csv.writer(g, delimiter=',')
                w.writerow(next(r))  # headline
                # skip 320 lines
                for i in range(0, 320):
                    next(r)
                first = next(r)
                instance = first[15]  # 15 instead
                for row in r:
                    if instance == row[15]:
                        w.writerow(row)
# Generator.generate_abc_use_case(100000)
# Generator.gen_auto_data()
# Generator.gen_mate_data(100000)
Generator.bpi19_one_instances()

import random
from copy import deepcopy


def create_random_data_file(n, dimensionality, filename):
    f = open(filename, mode='w')

    for _ in range(0, n):
        f.write(vector_to_csv_line(get_random_vector(dimensionality, 0, 500)))


def create_data_file_with_random_patterns(n, max_pattern_size, max_reps, num_patterns, dimensionality, filename):
    f = open(filename, mode='w')

    lines_written = 0
    lines = []

    while lines_written < n:
        for _ in range(0, num_patterns):
            pattern = []
            pattern_size = random.randint(1, max_pattern_size)
            for _ in range(0, pattern_size):
                pattern.append(get_random_vector(dimensionality, 0, 500))

            for v in pattern:
                lines.append(vector_to_csv_line(v))
                lines_written += 1

            repetitions = random.randint(0, max_reps)
            for _ in range(0, repetitions):
                p_copy = deepcopy(pattern)
                shift = random.randint(-100, 300)
                for p in p_copy:
                    p[0] += shift
                    lines.append(vector_to_csv_line(p))
                    lines_written += 1

    for line in lines[0:n]:
        f.write(line)


def get_random_vector(dimensionality, min_val, max_val):
    vec = []
    for _ in range(0, dimensionality):
        rint = float(random.randint(min_val, max_val))
        rint += random.randint(1, 4) / 4
        vec.append(rint)

    return vec


def vector_to_csv_line(vec):
    s = ''
    for v in vec:
        s += str(v) + ', '

    return s[0:len(s) - 2] + '\n'


def csv_from_musicxml(musicxml_file_name, csv_name):
    f = open(csv_name, mode='w')
    # TODO: create this


if __name__ == '__main__':
    pass
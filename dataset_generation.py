import random
from vector import Vector


def create_random_data_file(n, dimensionality, filename):
    f = open(filename, mode='w')

    for _ in range(0, n):
        f.write(vector_to_csv_line(get_random_vector(dimensionality, 0, 500)))


def create_data_file_with_random_patterns(n, max_pattern_size, max_reps, num_patterns, dimensionality, filename):
    f = open(filename, mode='w')

    dataset_vectors = set()

    while len(dataset_vectors) <= n:
        for _ in range(0, num_patterns):
            pattern = []
            pattern_size = random.randint(1, max_pattern_size)
            for _ in range(0, pattern_size):
                v = get_random_vector(dimensionality, 0, 500)
                while v in dataset_vectors:
                    v = get_random_vector(dimensionality, 0, 500)

                pattern.append(v)

            for v in pattern:
                dataset_vectors.add(v)

            repetitions = random.randint(0, max_reps)
            for _ in range(0, repetitions):
                rand_components = []
                for _ in range(dimensionality):
                    rand_components.append(random.randint(0, 300))

                rand_vector = Vector(rand_components)

                for p in pattern:
                    translated_vec = p + rand_vector
                    dataset_vectors.add(translated_vec)

    for vec in list(dataset_vectors)[0:n]:
        f.write(vector_to_csv_line(vec))


def get_random_vector(dimensionality, min_val, max_val):
    components = []
    for _ in range(0, dimensionality):
        rint = float(random.randint(min_val, max_val))
        rint += random.randint(1, 4) / 4
        components.append(rint)

    return Vector(components)


def vector_to_csv_line(vec):
    s = ''
    for i in range(vec.dimensionality()):
        s += str(vec[i]) + ', '

    return s[0:len(s) - 2] + '\n'


def csv_from_musicxml(musicxml_file_name, csv_name):
    f = open(csv_name, mode='w')
    # TODO: create this


def create_random_datafiles(limits, increment, dimensionality):
    for n in range(limits[0], limits[1] + 1, increment):
        create_data_file_with_random_patterns(n, 5, 5, 5, dimensionality, 'testfiles/rand_patterns_'
                                                + str(n) + '_dim' + str(dimensionality) + '.csv')


if __name__ == '__main__':
    create_random_datafiles((100, 900), 100, 2)
    create_random_datafiles((1000, 20000), 1000, 2)

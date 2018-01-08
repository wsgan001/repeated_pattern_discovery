import random
from vector import Vector
import music21
from os import listdir
from os.path import isfile, join


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


def csv_from_midi(midi_file_name, csv_name):
    """ Creates a two-dimensional point set (onset time, chromatic pitch) from midi file. """

    midi_file = music21.midi.MidiFile()
    midi_file.open(filename=midi_file_name)
    midi_file.read()

    vectors = set()
    time = 0
    for track in midi_file.tracks:
        for event in track.events:
            if event.type == 'DeltaTime':
                time += event.time

            if event.type == 'NOTE_ON':
                pitch = event._getData()
                vectors.add(Vector([time/midi_file.ticksPerQuarterNote, pitch]))

    output_file = open(csv_name, mode='w')
    for vector in list(vectors):
        output_file.write(vector_to_csv_line(vector))


def create_csvs_from_midis(input_dir, output_dir):
    """ Creates two-dimensional point sets (onset time, chromatic pitch) from all MIDI files in input directory (input_dir).
        Saves point sets as csv files in output directory (output_dir). """

    if input_dir[len(input_dir) - 1] != '/':
        input_dir += '/'

    if output_dir[len(output_dir) - 1] != '/':
        output_dir += '/'

    files = [f for f in listdir(input_dir) if isfile(join(input_dir, f)) and '.mid' in f]
    for file in files:
        input_file = input_dir + file
        output_file = output_dir + file.replace('.mid', '.csv')
        csv_from_midi(input_file, output_file)


def create_random_datafiles(limits, increment, dimensionality):
    for n in range(limits[0], limits[1] + 1, increment):
        create_data_file_with_random_patterns(n, 5, 5, 5, dimensionality, 'testfiles/rand_patterns_'
                                                + str(n) + '_dim' + str(dimensionality) + '.csv')


def create_mtp_count_minimizing_dataset(filename, n):
    f = open(filename, mode='w')
    for x in range(0, n):
        f.write(vector_to_csv_line(Vector([x, 1])))


def create_mtp_count_maximizing_dataset(filename, n):
    f = open(filename, mode='w')
    y_incr = 0.01
    y = 0
    for x in range(0, n):
        y += x * y_incr
        f.write(vector_to_csv_line(Vector([x, y])))


def get_random_patterns_set():
    rand_patterns = {'testfiles/random_patterns/rand_patterns_1000_dim2.csv': 5,
                     'testfiles/random_patterns/rand_patterns_2000_dim2.csv': 5,
                     'testfiles/random_patterns/rand_patterns_3000_dim2.csv': 5,
                     'testfiles/random_patterns/rand_patterns_4000_dim2.csv': 5,
                     'testfiles/random_patterns/rand_patterns_5000_dim2.csv': 4,
                     'testfiles/random_patterns/rand_patterns_6000_dim2.csv': 4,
                     'testfiles/random_patterns/rand_patterns_7000_dim2.csv': 4,
                     'testfiles/random_patterns/rand_patterns_8000_dim2.csv': 3,
                     'testfiles/random_patterns/rand_patterns_9000_dim2.csv': 3,
                     'testfiles/random_patterns/rand_patterns_10000_dim2.csv': 2,
                     'testfiles/random_patterns/rand_patterns_11000_dim2.csv': 2,
                     'testfiles/random_patterns/rand_patterns_12000_dim2.csv': 2,
                     'testfiles/random_patterns/rand_patterns_13000_dim2.csv': 2,
                     'testfiles/random_patterns/rand_patterns_14000_dim2.csv': 2,
                     'testfiles/random_patterns/rand_patterns_15000_dim2.csv': 2}

    return rand_patterns


def get_mtp_count_max_dataset():
    mtp_count_max = {'testfiles/mtp_count_max/mtp_count_max_1000.csv': 5,
                     'testfiles/mtp_count_max/mtp_count_max_2000.csv': 5,
                     'testfiles/mtp_count_max/mtp_count_max_3000.csv': 5,
                     'testfiles/mtp_count_max/mtp_count_max_4000.csv': 5,
                     'testfiles/mtp_count_max/mtp_count_max_5000.csv': 4,
                     'testfiles/mtp_count_max/mtp_count_max_6000.csv': 4,
                     'testfiles/mtp_count_max/mtp_count_max_7000.csv': 4,
                     'testfiles/mtp_count_max/mtp_count_max_8000.csv': 3,
                     'testfiles/mtp_count_max/mtp_count_max_9000.csv': 3,
                     'testfiles/mtp_count_max/mtp_count_max_10000.csv': 2,
                     'testfiles/mtp_count_max/mtp_count_max_11000.csv': 2,
                     'testfiles/mtp_count_max/mtp_count_max_12000.csv': 2,
                     'testfiles/mtp_count_max/mtp_count_max_13000.csv': 2,
                     'testfiles/mtp_count_max/mtp_count_max_14000.csv': 2,
                     'testfiles/mtp_count_max/mtp_count_max_15000.csv': 2}

    return mtp_count_max


def get_mtp_count_min_dataset():
    mtp_count_min = {'testfiles/mtp_count_min/mtp_count_min_1000.csv': 5,
                     'testfiles/mtp_count_min/mtp_count_min_2000.csv': 5,
                     'testfiles/mtp_count_min/mtp_count_min_3000.csv': 5,
                     'testfiles/mtp_count_min/mtp_count_min_4000.csv': 5,
                     'testfiles/mtp_count_min/mtp_count_min_5000.csv': 4,
                     'testfiles/mtp_count_min/mtp_count_min_6000.csv': 4,
                     'testfiles/mtp_count_min/mtp_count_min_7000.csv': 4,
                     'testfiles/mtp_count_min/mtp_count_min_8000.csv': 3,
                     'testfiles/mtp_count_min/mtp_count_min_9000.csv': 3,
                     'testfiles/mtp_count_min/mtp_count_min_10000.csv': 2,
                     'testfiles/mtp_count_min/mtp_count_min_11000.csv': 2,
                     'testfiles/mtp_count_min/mtp_count_min_12000.csv': 2,
                     'testfiles/mtp_count_min/mtp_count_min_13000.csv': 2,
                     'testfiles/mtp_count_min/mtp_count_min_14000.csv': 2,
                     'testfiles/mtp_count_min/mtp_count_min_15000.csv': 2}

    return mtp_count_min


def main():
    create_csvs_from_midis('testfiles/midi_files/bach_wtk', 'testfiles/music_corpus/bach_wtk')


if __name__ == '__main__':
    main()
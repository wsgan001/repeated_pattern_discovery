import random
from vector import Vector
#import music21
from os import listdir
from os.path import isfile, join


def create_random_data_file(n, dimensionality, filename):
    f = open(filename, mode='w')

    for _ in range(0, n):
        f.write(vector_to_csv_line(get_random_vector(dimensionality, 0, 500)))


def create_data_file_with_random_patterns(n, min_pattern_size, max_pattern_size, max_reps, dimensionality, filename):
    f = open(filename, mode='w')

    dataset_vectors = set()

    while len(dataset_vectors) <= n:
        pattern_size = random.randint(min_pattern_size, max_pattern_size)
        pattern = get_random_pattern(pattern_size, dimensionality)

        for v in pattern:
            dataset_vectors.add(v)

        repetitions = random.randint(1, max_reps)
        for _ in range(0, repetitions):
            rand_vector = get_random_vector(dimensionality, 0, 1000)

            for p in pattern:
                translated_vec = p + rand_vector
                dataset_vectors.add(translated_vec)

    for vec in list(dataset_vectors)[0:n]:
        f.write(vector_to_csv_line(vec))


def get_random_pattern(pattern_size, dimensionality):
    pattern = []

    for _ in range(pattern_size):
        pattern.append(get_random_vector(dimensionality, 0, 1000))

    return pattern


def get_random_vector(dimensionality, min_val, max_val):
    components = []
    for _ in range(0, dimensionality):
        random_component = float(random.randint(min_val, max_val))
        random_component += random.randint(1, 4) / 4
        components.append(random_component)

    return Vector(components)


def vector_to_csv_line(vec):
    s = ''
    for i in range(vec.dimensionality()):
        s += str(vec[i]) + ', '

    return s[0:len(s) - 2] + '\n'


def csv_from_midi(midi_file_name, csv_name):
    """ Creates a two-dimensional point set (onset time, chromatic pitch) from midi file. """

    midi_file = None # music21.midi.MidiFile()
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
                vectors.add(Vector([compute_onset_time(time, midi_file.ticksPerQuarterNote), pitch]))

    output_file = open(csv_name, mode='w')
    for vector in list(vectors):
        output_file.write(vector_to_csv_line(vector))


def compute_onset_time(event_time, ticks_per_quarter):
    unquantized = event_time/ticks_per_quarter
    return round(unquantized*4)/4


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
        create_data_file_with_random_patterns(n, int(n/100), int(n/4), 30, dimensionality,
                                              'testfiles/random_patterns/rand_patterns_' + str(n) + '.csv')


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
    rand_patterns = {'testfiles/random_patterns/rand_patterns_500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_1000.csv': 1,
                     'testfiles/random_patterns/rand_patterns_1500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_2000.csv': 1,
                     'testfiles/random_patterns/rand_patterns_2500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_3000.csv': 1}

    return rand_patterns


def get_mtp_count_max_dataset():
    mtp_count_max = {'testfiles/mtp_count_max/mtp_count_max_500.csv': 1,
                     'testfiles/mtp_count_max/mtp_count_max_1000.csv': 1,
                     'testfiles/mtp_count_max/mtp_count_max_1500.csv': 1,
                     'testfiles/mtp_count_max/mtp_count_max_2000.csv': 1,
                     'testfiles/mtp_count_max/mtp_count_max_2500.csv': 1,
                     'testfiles/mtp_count_max/mtp_count_max_3000.csv': 1,
                     'testfiles/mtp_count_max/mtp_count_max_3500.csv': 1,
                     'testfiles/mtp_count_max/mtp_count_max_4000.csv': 1}

    return mtp_count_max


def get_mtp_count_min_dataset():
    mtp_count_min = {'testfiles/mtp_count_min/mtp_count_min_500.csv': 1,
                     'testfiles/mtp_count_min/mtp_count_min_1000.csv': 1,
                     'testfiles/mtp_count_min/mtp_count_min_1500.csv': 1,
                     'testfiles/mtp_count_min/mtp_count_min_2000.csv': 1,
                     'testfiles/mtp_count_min/mtp_count_min_2500.csv': 1,
                     'testfiles/mtp_count_min/mtp_count_min_3000.csv': 1,
                     'testfiles/mtp_count_min/mtp_count_min_3500.csv': 1,
                     'testfiles/mtp_count_min/mtp_count_min_4000.csv': 1}

    return mtp_count_min


def get_bach_wtk_datasets():
    bach = {'testfiles/music_corpus/bach_wtk/bwv846': 2,
            'testfiles/music_corpus/bach_wtk/bwv847': 2,
            'testfiles/music_corpus/bach_wtk/bwv848': 2,
            'testfiles/music_corpus/bach_wtk/bwv849': 2,
            'testfiles/music_corpus/bach_wtk/bwv850': 2,
            'testfiles/music_corpus/bach_wtk/bwv851': 2,
            'testfiles/music_corpus/bach_wtk/bwv852': 2,
            'testfiles/music_corpus/bach_wtk/bwv853': 2,
            'testfiles/music_corpus/bach_wtk/bwv854': 2,
            'testfiles/music_corpus/bach_wtk/bwv855': 2,
            'testfiles/music_corpus/bach_wtk/bwv856': 2,
            'testfiles/music_corpus/bach_wtk/bwv857': 2,
            'testfiles/music_corpus/bach_wtk/bwv858': 2,
            'testfiles/music_corpus/bach_wtk/bwv859': 2,
            'testfiles/music_corpus/bach_wtk/bwv860': 2,
            'testfiles/music_corpus/bach_wtk/bwv861': 2,
            'testfiles/music_corpus/bach_wtk/bwv862': 2,
            'testfiles/music_corpus/bach_wtk/bwv863': 2,
            'testfiles/music_corpus/bach_wtk/bwv864': 2,
            'testfiles/music_corpus/bach_wtk/bwv865': 2,
            'testfiles/music_corpus/bach_wtk/bwv866': 2,
            'testfiles/music_corpus/bach_wtk/bwv867': 2,
            'testfiles/music_corpus/bach_wtk/bwv868': 2,
            'testfiles/music_corpus/bach_wtk/bwv869': 2}

    return bach


def main():
    create_random_datafiles((5000, 8000), 500, 2)


if __name__ == '__main__':
    main()
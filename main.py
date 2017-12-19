from dataset import Dataset
import orig_algorithms
import new_algorithms
import performance
import helpers
from copy import deepcopy


def run_tec_filtering_algorithms(dataset):
    print('Number of MTPs', len(orig_algorithms.sia(deepcopy(dataset))))

    print('\nSiatec')
    helpers.print_tecs(orig_algorithms.siatec(deepcopy(dataset)))

    print('\nForth\'s algorithm')
    primary, secondary = orig_algorithms.forths_algorithm(deepcopy(dataset), 4, 1.7)
    helpers.print_tecs(primary)

    print('\nCosiatec')
    helpers.print_tecs(orig_algorithms.cosiatec(deepcopy(dataset)))

    print('\nSIATECCompress')
    helpers.print_tecs(orig_algorithms.siatec_compress(deepcopy(dataset)))


def test_sia_hash_time():
    for i in range(100, 1001, 100):
        performance.measure_function(new_algorithms.sia_hash,
                                     Dataset('testfiles/rand_patterns_' + str(i) + '_dim2.csv'), 2)


def test_siatec_hash_time():
    for i in range(100, 1001, 100):
        performance.measure_function(new_algorithms.siatec_hash,
                                     Dataset('testfiles/rand_patterns_' + str(i) + '_dim2.csv'), 2)


def print_examples():
    dataset = Dataset('testfiles/bach_wtk_excerpt.csv')
    helpers.print_mtps(orig_algorithms.sia(dataset))
    helpers.print_tecs(orig_algorithms.siatec(dataset))


def simplified_vec_str(vec):
    comps = []
    for k in range(vec.dimensionality()):
        comps.append(str(int(vec[k])))

    return '(' + ','.join(comps) + ')'


def print_v_for_dataset(dataset):

    dataset.sort_ascending()
    table_lines = [['\ ']]

    for i in range(len(dataset)):
        table_lines[0].append('$' + simplified_vec_str(dataset[i]) + '$')

    for i in range(len(dataset)):
        table_lines.append(['$' + simplified_vec_str(dataset[i]) + '$'])
        for j in range(len(dataset)):
            if i < j:
                table_lines[i + 1].append('$\\langle ' + simplified_vec_str(dataset[j] - dataset[i]) + ', ' + str(i) + '\\rangle $')
            else:
                table_lines[i + 1].append('\\ ')

    pos_string = '|'.join(['c' for v in dataset])
    print('\\begin{tabular}[pos]{' + pos_string + '|c}')

    for i in range(len(table_lines)):
        print('\t' + ' & '.join(table_lines[i]) + '\\\\')

    print('\\end{tabular}')


def main():
    print_v_for_dataset(Dataset('testfiles/bach_wtk_excerpt.csv'))


if __name__ == "__main__":
    main()
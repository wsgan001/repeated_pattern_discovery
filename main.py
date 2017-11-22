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


def hash_function_testing():
    for i in range(300, 501, 100):
        performance.measure_function(new_algorithms.sia_hash,
                                     Dataset('testfiles/rand_patterns_' + str(i) + '_dim2.csv'), 2)


def main():
    hash_function_testing()


if __name__ == "__main__":
    main()
from dataset import Dataset
import orig_algorithms
import new_algorithms
import performance
import dataset_generation
from operator import itemgetter
import helpers


def main():
    dataset = Dataset('testfiles/random_patterns/rand_patterns_800.csv')

    performance.measure_function(orig_algorithms.cosiatech, dataset, 1)
    performance.measure_function(orig_algorithms.siatech_compress, dataset, 1)
    performance.measure_function(lambda d: orig_algorithms.forths_algorithmh(d, 2, 2), dataset, 1)


if __name__ == "__main__":
    main()
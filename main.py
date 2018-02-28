from dataset import Dataset
import orig_algorithms
import new_algorithms
import performance
import dataset_generation
from operator import itemgetter
import helpers


def measure_siatech_siatechf():
    datasets = dataset_generation.get_random_patterns_set()

    performance.measure_function_time_on_datasets(new_algorithms.siatech, datasets, 'random_patterns')

    cr_th = 2
    performance.measure_function_time_on_datasets(lambda d: new_algorithms.siatechf(d, cr_th), datasets,
                                                  'random_patterns', algorithm_name='siatechf(th=' + str(cr_th) + ')')

    cr_th = 4
    performance.measure_function_time_on_datasets(lambda d: new_algorithms.siatechf(d, cr_th), datasets,
                                                  'random_patterns', algorithm_name='siatechf(th=' + str(cr_th) + ')')

    cr_th = 6
    performance.measure_function_time_on_datasets(lambda d: new_algorithms.siatechf(d, cr_th), datasets,
                                                  'random_patterns', algorithm_name='siatechf(th=' + str(cr_th) + ')')


def measure_filtering_algorithms():
    datasets = dataset_generation.get_random_patterns_set()

    performance.measure_function_time_on_datasets(lambda d: orig_algorithms.forths_algorithmh(d, 15, 0.5), datasets,
                                                  'random_patterns', algorithm_name="forths_algo(15,0.5)")

    performance.measure_function_time_on_datasets(orig_algorithms.cosiatech, datasets, 'random_patterns')

    cr_th = 3
    performance.measure_function_time_on_datasets(lambda d: new_algorithms.siatechf(d, cr_th), datasets,
                                                  'random_patterns', algorithm_name='siatechf(th=' + str(cr_th) + ')')

    performance.measure_function_time_on_datasets(orig_algorithms.siatech_compress, datasets, 'random_patterns')


def main():
    datasets = {'testfiles/random_patterns/rand_patterns_500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_1000.csv': 1,
                     'testfiles/random_patterns/rand_patterns_1500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_2000.csv': 1,
                     'testfiles/random_patterns/rand_patterns_2500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_3000.csv': 1,
                     'testfiles/random_patterns/rand_patterns_3500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_4000.csv': 1,
                     'testfiles/random_patterns/rand_patterns_4500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_5000.csv': 1,
                     'testfiles/random_patterns/rand_patterns_5500.csv': 1,
                     'testfiles/random_patterns/rand_patterns_6000.csv': 1}

    cr_th = 2
    performance.measure_function_time_on_datasets(lambda d: new_algorithms.siatechf(d, cr_th), datasets,
                                                  'random_patterns', algorithm_name='siatech_pf')


if __name__ == "__main__":
    main()
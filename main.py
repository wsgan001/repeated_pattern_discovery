from dataset import Dataset
import orig_algorithms
import new_algorithms
import performance
import dataset_generation
import helpers


def measure_mtp_algorithms_on_datasets(datasets, datasets_name):
    performance.measure_function_time_on_datasets(orig_algorithms.sia, datasets, datasets_name)
    r = 5
    performance.measure_function_time_on_datasets(lambda d: orig_algorithms.siar(d, r), datasets,
                                                  datasets_name, algorithm_name='siar(r=' + str(r) + ')')
    performance.measure_function_time_on_datasets(new_algorithms.siah, datasets, datasets_name)


def measure_mtp_algorithm_runtimes():
    rand_patterns = dataset_generation.get_random_patterns_set()
    mtp_count_max = dataset_generation.get_mtp_count_max_dataset()
    mtp_count_min = dataset_generation.get_mtp_count_min_dataset()
    measure_mtp_algorithms_on_datasets(rand_patterns, 'rand_patterns')
    measure_mtp_algorithms_on_datasets(mtp_count_max, 'mtp_count_max')
    measure_mtp_algorithms_on_datasets(mtp_count_min, 'mtp_count_min')


def measure_tec_algorithms_on_datasets(datasets, datasets_name):
    performance.measure_function_time_on_datasets(orig_algorithms.siatec, datasets, datasets_name)
    performance.measure_function_time_on_datasets(new_algorithms.siatech, datasets, datasets_name)


def measure_tec_algorithm_runtimes():
    rand_patterns = dataset_generation.get_random_patterns_set()
    mtp_count_max = dataset_generation.get_mtp_count_max_dataset()
    mtp_count_min = dataset_generation.get_mtp_count_min_dataset()
    measure_tec_algorithms_on_datasets(rand_patterns, 'rand_patterns')
    measure_tec_algorithms_on_datasets(mtp_count_max, 'mtp_count_max')
    measure_tec_algorithms_on_datasets(mtp_count_min, 'mtp_count_min')


def main():
    # measure_mtp_algorithm_runtimes()
    # measure_tec_algorithm_runtimes()
    dataset = Dataset('testfiles/random_patterns/rand_patterns_10_dim2.csv')
    sorted_d = Dataset.sort_ascending(dataset)
    mtps = orig_algorithms.sia(dataset)
    helpers.print_mtps(mtps)


if __name__ == "__main__":
    main()
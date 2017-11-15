import time
from copy import deepcopy
from dataset import Dataset


def measure_function(measured_function, input_data, iterations):
    times = []

    for _ in range(iterations):
        data = deepcopy(input_data)
        elapsed, result = measure_time(measured_function, data)
        times.append(elapsed)

    avg_time = 0
    for t in times:
        avg_time += t

    avg_time /= len(times)
    print('Running ' + measured_function.__name__ + '\nDataset: '
          + input_data.get_name() + '\nAverage time: ' + str(avg_time)
          + '\nResult size: ' + str(len(result)) + '\n')


def measure_time(measured_function, input_data):
    start = time.time()
    result = measured_function(input_data)
    end = time.time()
    elapsed = end - start
    return elapsed, result


def compare_mtp_algorithms(mtp_algo1, mtp_algo2):
    measure_function(mtp_algo1, Dataset('testfiles/rand_patterns_100.csv'), 1)
    measure_function(mtp_algo2, Dataset('testfiles/rand_patterns_100.csv'), 1)

    measure_function(mtp_algo1, Dataset('testfiles/rand_patterns_500.csv'), 1)
    measure_function(mtp_algo2, Dataset('testfiles/rand_patterns_500.csv'), 1)

    measure_function(mtp_algo1, Dataset('testfiles/rand_patterns_1000.csv'), 1)
    measure_function(mtp_algo2, Dataset('testfiles/rand_patterns_1000.csv'), 1)

    measure_function(mtp_algo1, Dataset('testfiles/rand_patterns_1500.csv'), 1)
    measure_function(mtp_algo2, Dataset('testfiles/rand_patterns_1500.csv'), 1)


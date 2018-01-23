import time
from datetime import datetime
from copy import deepcopy
from dataset import Dataset
from operator import itemgetter


def measure_function(measured_function, input_data, iterations, algorithm_name='', printout=True):
    times = []

    for _ in range(iterations):
        data = deepcopy(input_data)
        elapsed, result = measure_time(measured_function, data)
        times.append(elapsed)

    avg_time = 0
    for t in times:
        avg_time += t

    avg_time /= len(times)

    if algorithm_name == '':
        algorithm_name = measured_function.__name__

    if printout:
        print('Algorithm: ' + algorithm_name + '\nDataset: '
              + input_data.get_name() + ' (n=' + str(len(input_data)) + ')' + '\nAverage time: ' + str(avg_time)
              + '\nResult size: ' + str(len(result)) + '\n')

    return avg_time, result


def measure_time(measured_function, input_data):
    start = time.time()
    result = measured_function(input_data)
    end = time.time()
    elapsed = end - start
    return elapsed, result


def measure_function_time_on_datasets(measured_function, dataset_information, dataset_type, algorithm_name=''):

    if algorithm_name == '':
        algorithm_name = measured_function.__name__

    outputrows = []

    for dataset_name in dataset_information:
        iterations = dataset_information[dataset_name]
        dataset = Dataset(dataset_name)
        runtime, result = measure_function(measured_function, deepcopy(dataset), iterations, algorithm_name, printout=True)
        outputrows.append([algorithm_name, dataset.get_name(), str(len(dataset)), str(runtime), str(len(result))])

    outputrows.sort(key=itemgetter(3))

    timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.now())
    output_file_name = 'output/runtimes' + algorithm_name + '-' + dataset_type + '-' + timestamp + '.csv'
    outputfile = open(output_file_name, mode='w')
    outputfile.write('algorithm, dataset, dataset_size, runtime, result_size\n')

    for outputrow in outputrows:
        outputfile.write(', '.join(outputrow) + '\n')

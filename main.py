from dataset import Dataset
import orig_algorithms
import own_algorithms
import performance
import helpers


def main():
    dataset = Dataset('testfiles/rand_patterns_1500.csv')
    performance.measure_function(lambda d: orig_algorithms.siar(d, r=50), dataset, 1)
    performance.measure_function(own_algorithms.sia_map, dataset, 1)


if __name__ == "__main__":
    main()
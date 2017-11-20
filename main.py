from dataset import Dataset
import orig_algorithms
import new_algorithms
import performance
import helpers


def main():
    tecs = orig_algorithms.forths_algorithm(Dataset('testfiles/rand_patterns_100_dim2.csv'), 4, 5)
    print('Found', len(tecs), 'TECs')


if __name__ == "__main__":
    main()
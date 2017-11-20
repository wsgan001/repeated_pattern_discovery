from dataset import Dataset
import orig_algorithms
import new_algorithms
import performance
import helpers


def main():
    primary, secondary = orig_algorithms.forths_algorithm(Dataset('testfiles/rand_patterns_300_dim2.csv'), 2, 1)
    helpers.print_tecs(primary)


if __name__ == "__main__":
    main()
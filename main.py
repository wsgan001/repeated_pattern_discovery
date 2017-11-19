from dataset import Dataset
import orig_algorithms
import own_algorithms
import performance
import helpers


def main():
    r = 4

    # In Hundreds
    for i in range(1, 10):
        #performance.measure_function(lambda d: orig_algorithms.siar(d, r=r),
         #                            Dataset('testfiles/rand_patterns_' + str(i) + '00_dim2.csv'), 3,
          #                           algorithm_name='siar r=' + str(r))
        performance.measure_function(own_algorithms.sia_hash,
                                     Dataset('testfiles/rand_patterns_' + str(i) + '00_dim2.csv'), 3)

    # In thousands
    # for i in range(1, 2 + 1):
    #     performance.measure_function(lambda d: orig_algorithms.siar(d, r=r),
    #                                  Dataset('testfiles/rand_patterns_' + str(i) + '000_dim2.csv'), 2,
    #                                  algorithm_name='siar r=' + str(r))
    #     performance.measure_function(own_algorithms.sia_hash,
    #                                  Dataset('testfiles/rand_patterns_' + str(i) + '000_dim2.csv'), 2)
    #     performance.measure_function(orig_algorithms.sia,
    #                                  Dataset('testfiles/rand_patterns_' + str(i) + '000_dim2.csv'), 2)


if __name__ == "__main__":
    main()
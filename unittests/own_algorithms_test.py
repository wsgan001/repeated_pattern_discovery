import unittest
from dataset import Dataset
from vector import Vector
import own_algorithms
import helpers


class OrigAlgorithmsTest(unittest.TestCase):

    def test_own_sia(self):
        dataset = Dataset('unittest_data/test_data1.csv')
        result = own_algorithms.sia_hash(dataset)

        exp_res = []
        exp_res.append((Vector([2, 1]), [Vector([1, 2]), Vector([2, 1])]))
        exp_res.append((Vector([1, -1]), [Vector([1, 2]), Vector([3, 3])]))
        exp_res.append((Vector([3, 0]), [Vector([1, 2])]))
        exp_res.append((Vector([1, 2]), [Vector([2, 1])]))

        results_match = OrigAlgorithmsTest.check_result(result, exp_res)
        if not results_match:
            print('Incorrect result')
            helpers.print_mtps(result)

        self.assertTrue(results_match)

    def test_sia_with_data_from_meredith(self):
        dataset = Dataset('unittest_data/Meredith2002_fig11.csv')
        result = own_algorithms.sia_hash(dataset)
        helpers.print_mtps(result)

        exp_res = []
        exp_res.append((Vector([0, 1]), [Vector([2, 1]), Vector([2, 2])]))
        exp_res.append((Vector([0, 2]), [Vector([1, 1]), Vector([2, 1])]))
        exp_res.append((Vector([1, -2]), [Vector([1, 3])]))
        exp_res.append((Vector([1, -1]), [Vector([1, 3]), Vector([2, 3])]))
        exp_res.append((Vector([1, 0]), [Vector([1, 1]), Vector([1, 3]), Vector([2, 2])]))
        exp_res.append((Vector([1, 1]), [Vector([1, 1]), Vector([2, 1])]))
        exp_res.append((Vector([1, 2]), [Vector([1, 1])]))
        exp_res.append((Vector([2, -1]), [Vector([1, 3])]))
        exp_res.append((Vector([2, 1]), [Vector([1, 1])]))

        results_match = OrigAlgorithmsTest.check_result(result, exp_res)
        if not results_match:
            print('Incorrect result')
            helpers.print_mtps(result)

        self.assertTrue(results_match)

    @staticmethod
    def check_result(result, expected):
        results_match = True

        for exp in expected:
            if exp not in result:
                results_match = False
                print(exp, 'not in result')

        for res in result:
            if res not in expected:
                results_match = False
                print(res, 'not in expected')

        return results_match


if __name__ == '__main__':
    unittest.main()
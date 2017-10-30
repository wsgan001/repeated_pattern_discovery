import unittest
import file_reader
from vector import Vector


class FileReaderTest(unittest.TestCase):

    def test_dataset_from_file(self):
        dataset = file_reader.dataset_from_file('test_data.csv')
        self.assertEqual(len(dataset), 4)
        self.assertEqual(Vector([1, 2, 3]), dataset[0])
        self.assertEqual(Vector([0.1, 0, -1.2]), dataset[1])
        self.assertEqual(Vector([0, 0, 0]), dataset[2])
        self.assertEqual(Vector([-1, -2, -1234.1234]), dataset[3])


if __name__ == '__main__':
    unittest.main()
import csv
from vector import Vector


class Dataset:

    _vectors = []
    _name = ''

    def __init__(self, filename):
        self._vectors = self.dataset_from_file(filename)

        split_path = filename.split('/')
        self._name = split_path[len(split_path) - 1]

    def dataset_from_file(self, filename):
        dataset = []

        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            dimensionality = 0

            for row in csv_reader:
                components = []
                for component in row:
                    components.append(float(component))

                if dimensionality == 0:
                    dimensionality = len(components)

                if len(components) != dimensionality:
                    print('All vectors in dataset are not of same dimensionality!')

                dataset.append(Vector(components))

        return dataset

    def get_name(self):
        return self._name

    def __len__(self):
        return len(self._vectors)

    def __str__(self):
        dataset_string = ''
        for vector in self._vectors:
            dataset_string += str(vector) + '\n'

        return dataset_string

    def __getitem__(self, index):
        return self._vectors[index]

    def sort_ascending(self):
        self._vectors.sort()

    def remove_all(self, vectors):
        for vec in vectors:
            self._vectors.remove(vec)

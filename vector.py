class Vector:
    """ Defines a vector and the operations required for expressing symbolic music
        data as vectors as defined in SOURCE """

    _components = []

    def __init__(self, components):
        self._components = components

    def dimensionality(self):
        """ Returns the dimensionality of the vector. """
        return len(self._components)

    def get_component(self, i):
        """ Returns the ith component of the vector """
        return self._components[i]

    def __cmp__(self, other):
        """ Vectors are compared using lexicographical ordering. """

        for i in range(0, self.dimensionality()):
            if self.get_component(i) < other.get_component(i):
                return -1
            if self.get_component(i) > other.get_component(i):
                return 1

        return 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __str__(self):
        string_repr = '('
        for i in range(0, self.dimensionality()):
            string_repr += str(self.get_component(i)) + ', '

        string_repr = string_repr[0: len(string_repr)-2] + ')'
        return string_repr

    def __add__(self, other):
        summed_components = []

        for i in range(0, self.dimensionality()):
            summed_components.append(self.get_component(i) + other.get_component(i))

        return Vector(summed_components)

    def __sub__(self, other):
        subs_components = []

        for i in range(0, self.dimensionality()):
            subs_components.append(self.get_component(i) - other.get_component(i))

        return Vector(subs_components)






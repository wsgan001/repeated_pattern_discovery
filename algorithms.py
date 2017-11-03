from vector import Vector
from dataset import Dataset
from functools import cmp_to_key

""" Implements algorithms defined in:
    [Meredith2002]
    David Meredith, Kjell Lemström & Geraint A. Wiggins (2002).
    Algorithms for discovering repeated patterns in
    multidimensional representations of polyphonic music,
    Journal of New Music Research, 31:4, 321-345. """


def sia(d):
    """ Implements SIA as described in [Meredith2002]

        Returns the set of MTPs as a list of tuples where the
        first element is the translation vector and the second
        element is a list of vectors that form the corresponding pattern. """

    # Step 1: Sort the dataset in ascending order
    d.sort_ascending()

    # Step 2: Compute the vector table V
    v = []

    for i in range(0, len(d)):
        for j in range(i + 1, len(d)):
            v.append((d[j] - d[i], i))

    # Step 3: Sort v
    v.sort()

    # Step 4: Compute MTPs from v
    mtps = compute_mtps(v, d)

    return mtps


def compute_mtps(v, d):
    """ This implements the function in [Meredith2002] Fig. 18.
        Instead of printing out the MTPs they are returned as a list of doubles. """

    mtps = []

    i = 0

    while i < len(v):
        trans_vector = v[i][0]
        pattern = []
        pattern.append(d[v[i][1]])

        j = i + 1
        while j < len(v) and v[j][0] == v[i][0]:
            pattern.append(d[v[j][1]])
            j += 1

        i = j
        mtps.append((trans_vector, pattern))

    return mtps


def print_mtps(mtps):
    print('Printing MTPs count=' + str(len(mtps)))
    for mtp in mtps:
        mtp_string = str(mtp[0])
        mtp_string += ' : {'

        for vector in mtp[1]:
            mtp_string += str(vector) + ', '

        mtp_string = mtp_string[0:len(mtp_string) - 2]
        mtp_string += '}'
        print(mtp_string)


def siatec(d):
    """ Implements the SIATEC algorithm described in [Meredith2002].

        Returns the TECs of d as a list of pairs, where the first
        element is the MTP and the second element is the list of translators. """

    # Step 1: Sort dataset
    d.sort_ascending()

    # Step 2 and 3: Compute vector tables w and v
    w = []
    v = []
    for i in range(0, len(d)):
        w.append([])
        for j in range(0, len(d)):
            w[i].append((d[j] - d[i], i))
            if j > i:
                v.append(w[i][j])

    # Step 4: Sort v
    v.sort()

    # Step 5: Vectorize the MTPs.
    x = compute_x(d, v)

    # Step 6: Sort x
    x.sort(key=cmp_to_key(x_cmp))

    # Step 7: Compute TECs from sorted x.
    tecs = compute_tecs(x, v, w, d)

    return tecs


def print_tecs(tecs):
    print('Printing TECs, count=' + str(len(tecs)))
    for tec in tecs:
        print(Vector.vector_set_to_str(tec[0]) + ', ' + Vector.vector_set_to_str(tec[1]))


def vec(p):
    """ Computes the difference vectors between consecutive vectors
        of the pattern as defined by the VEC function in [Meredith2002]. """

    vec_p = []
    for i in range(1, len(p)):
        vec_p.append(p[i] - p[i - 1])

    return vec_p


def compute_x(d, v):
    """ Computes the set X as defined in [Meredith2002] Fig. 20. """

    i = 0
    x = []

    while i < len(v):
        q = []
        j = i + 1

        while j < len(v) and v[j][0] == v[i][0]:
            q.append(d[v[j][1]] - d[v[j - 1][1]])
            j += 1

        x.append((i, q))
        i = j

    return x


def x_cmp(x1, x2):
    """ Implements the comparison of elements of set x as defined
        in [Meredith2002] SIATEC step 6. """

    q1 = x1[1]
    q2 = x2[1]

    # Compare length of patterns first.
    if len(q1) < len(q2):
        return -1
    if len(q1) > len(q2):
        return 1

    # Compare patterns lexicographically.
    if q1 < q2:
        return -1
    if q1 > q2:
        return 1

    # If patterns are equal, then compare indices.
    return x1[0] - x2[0]


def compute_tecs(y, v, w, d):
    """ Implements algorithm of fig. 23 in [Meredith2002]. """

    i = 0
    tecs = []

    while i < len(y):
        j = y[i][0]
        pattern_indices = []
        while j < len(v) and v[j][0] == v[y[i][0]][0]:
            pattern_indices.append(v[j][1])
            j += 1

        pattern = collect_pattern(pattern_indices, d)
        translators = find_translators(pattern_indices, w, len(d))
        tecs.append((pattern, translators))

        i += 1
        while i < len(y) and y[i][1] == y[i - 1][1]:
            i += 1

    return tecs


def collect_pattern(pattern_indices, d):
    """ Algorithm in Fig. 24 of [Meredith2002] but instead
        of printing the pattern is collected into a list. """

    pattern = []
    for i in pattern_indices:
        pattern.append(d[i])
    return pattern


def find_translators(pattern_ind, w, data_size):
    """ Implements the algorithm in Fig. 25 of [Meredith2002] """
    translators = []

    pattern_len = len(pattern_ind)

    # The case of a pattern with size one needs to be handled separately.
    if pattern_len == 1:
        for j in range(0, len(w[0])):
            translators.append(w[pattern_ind[0]][j][0])
        return translators

    J = []
    for _ in range(0, pattern_len):
        J.append(0)

    finished = False
    k = 1

    while not finished:
        if J[k] <= J[k - 1]:
            J[k] = J[k - 1] + 1

        while J[k] <= data_size - pattern_len + k \
                and w[pattern_ind[k]][J[k]][0] < w[pattern_ind[k - 1]][J[k - 1]][0]:
            J[k] += 1

        if J[k] > data_size - pattern_len + k:
            finished = True
        elif w[pattern_ind[k]][J[k]][0] > w[pattern_ind[k - 1]][J[k - 1]][0]:
            k = 1
            J[0] += 1
            if J[0] > data_size - pattern_len + 1:
                finished = True
        elif k == len(pattern_ind) - 1:
            translators.append(w[pattern_ind[k]][J[k]][0])
            k = 0
            while k < pattern_len:
                J[k] += 1
                if J[k] > data_size - pattern_len + k:
                    finished = True
                    k = pattern_len - 1
                k += 1
            k = 1
        else:
            k += 1

    return translators






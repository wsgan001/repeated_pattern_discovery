from vector import Vector
from functools import cmp_to_key
from copy import deepcopy
from operator import itemgetter
import heuristics
from tec import TEC


""" Implements algorithms defined in:
    [Meredith2002]
    David Meredith, Kjell Lemström & Geraint A. Wiggins (2002).
    Algorithms for discovering repeated patterns in
    multidimensional representations of polyphonic music,
    Journal of New Music Research, 31:4, 321-345.

    [Meredith2013]
    David Meredith (2013).
    COSIATEC and SIATECCOMPRESS: Pattern Discovery by Geometric Compression.
    MIREX 2013, Curitiba, Brazil. Competition on Discovery of Repeated Themes and Sections. """


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
        print(str(tec))


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
        tecs.append(TEC(pattern, pattern_indices, translators))

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


def cosiatec(d):
    """ Implements the COSIATEC algorithm as described in [Meredith2013]. """
    d.sort_ascending()
    p = deepcopy(d) # TODO: Implement necessary functions for deep copying?
    best_tecs = []

    while p:
        best_tec = get_best_tec(p, d)
        best_tecs.append(best_tec)
        p.remove_all(best_tec.coverage())

    return best_tecs


def get_best_tec(p, d):
    """ Finds the best TEC in p, the copy of the dataset d. Figure 2 of [Meredith2013].  """

    v, w = compute_vector_tables(p)
    mcps = compute_mtp_cis_pairs(v)
    best_tec = None

    for i in range(0, len(mcps)):
        mcp = mcps[i]
        mtp_indices = mcp[1]
        tec = get_tec_for_mtp(mtp_indices, w, p)
        conj = get_conj(tec, d)
        tec = rem_red_tran(tec)
        conj = rem_red_tran(conj)

        if not best_tec or is_better_tec(tec, best_tec, d):
            best_tec = tec
        if is_better_tec(conj, best_tec, d):
            best_tec = conj

    return best_tec


def compute_vector_tables(p):
    """ Compute the vector table V as defined in [Meredith2013],
        and the vector table W as needed in SIATEC [Meredith2002]. """

    v = []
    w = []

    for i in range(0, len(p)):
        v.append([])
        w.append([])
        for j in range(0, len(p)):
            v[i].append((p[i] - p[j], p[j], j))
            w[i].append((p[j] - p[i], i))

    return v, w


def compute_mtp_cis_pairs(v):
    """ Implements algorithm of Figure 3 from [Meredith2013]. """

    w = []
    for i in range(0, len(v)):
        for j in range(0, len(v[i])):
            w.append(v[i][j])

    w.sort(key=itemgetter(0))

    mtps = []
    ciss = []
    vec = w[0][0]
    mtp = [w[0][1]]
    cis = [w[0][2]]

    for i in range(1, len(w)):
        vpi = w[i]
        if vpi[0] == vec:
            mtp.append(vpi[1])
            cis.append(vpi[2])
        else:
            mtps.append(mtp)
            ciss.append(cis)
            mtp = [vpi[1]]
            cis = [vpi[2]]
            vec = vpi[0]

    mtps.append(mtp)
    ciss.append(cis)

    mcps = []
    for i in range(0, len(mtps)):
        mcps.append((mtps[i], ciss[i]))

    return mcps


def get_tec_for_mtp(pattern_indices, w, p):
    """ Find the TEC for the given MTP. This function is not described in
        [Meredith2013] but is said to use the logic of SIATEC, so this function
        uses the logic of finding translators for the pattern used in SIATEC. """

    translators = find_translators(pattern_indices, w, len(p))
    pattern = []
    for index in pattern_indices:
        pattern.append(p[index])

    tec = TEC(pattern, pattern_indices, translators)
    return tec


def get_conj(tec, sorted_dataset):
    """ Computes the conjugate of a TEC as defined in equations
        7-9 of [Meredith2013]. """

    p_0 = tec.get_pattern()[0]
    conj_tec_pattern_ind = [tec.get_pattern_indices()[0]]
    p_prime = [p_0]

    for translator in tec.get_translators():
        if not translator.is_zero():
            p_prime_vec = p_0 + translator
            p_prime.append(p_prime_vec)

            # Find the index for the point in the pattern of the conjugate TEC.
            if p_prime_vec < p_0:
                for i in range(tec.get_pattern_indices()[0], -1, -1):
                    if sorted_dataset[i] == p_prime_vec:
                        conj_tec_pattern_ind.append(i)
                        break
            else:
                for i in range(tec.get_pattern_indices()[0], len(sorted_dataset)):
                    if sorted_dataset[i] == p_prime_vec:
                        conj_tec_pattern_ind.append(i)
                        break

    v_prime = [Vector.zero_vector(p_0.dimensionality())]
    for point in tec.get_pattern():
        p = point - p_0
        if not p.is_zero():
            v_prime.append(point - p_0)

    conj_tec = TEC(p_prime, conj_tec_pattern_ind, v_prime)

    return conj_tec


def rem_red_tran(tec):
    # TODO: Try to find a method for this.
    return tec


def is_better_tec(tec1, tec2, sorted_dataset):
    """ Implements algorithm from Figure 5 of [Meredith2013].
        Added else ifs so that the algorithm works correctly as described in the article text. """

    if heuristics.compression_ratio(tec1) > heuristics.compression_ratio(tec2):
        return True
    elif heuristics.compression_ratio(tec1) < heuristics.compression_ratio(tec2):
        return False

    if heuristics.bounding_box_compactness(tec1, sorted_dataset) > heuristics.bounding_box_compactness(tec2, sorted_dataset):
        return True
    elif heuristics.bounding_box_compactness(tec1, sorted_dataset) < heuristics.bounding_box_compactness(tec2,
                                                                                                         sorted_dataset):
        return False

    if len(tec1.coverage()) > len(tec2.coverage()):
        return True
    elif len(tec1.coverage()) < len(tec2.coverage()):
        return False

    # Compare pattern sizes
    if len(tec1.get_pattern()) > len(tec2.get_pattern()):
        return True
    elif len(tec1.get_pattern()) < len(tec2.get_pattern()):
        return False

    if heuristics.pattern_width(tec1) < heuristics.pattern_width(tec2):
        return True
    elif heuristics.pattern_width(tec1) > heuristics.pattern_width(tec2):
        return False

    if heuristics.pattern_volume(tec1) < heuristics.pattern_volume(tec2):
        return True

    return False

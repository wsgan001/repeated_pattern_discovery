from vector import Vector
from functools import cmp_to_key
from copy import deepcopy
from operator import itemgetter
import heuristics
from tec import TEC

""" Implements SIA family of algorithms. """


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


def find_translators(pattern_indices, w, data_size):
    """ Implements the algorithm in Fig. 25 of [Meredith2002] """
    translators = []

    pattern_len = len(pattern_indices)

    # The case of a pattern with size one needs to be handled separately.
    if pattern_len == 1:
        for j in range(0, len(w[0])):
            translators.append(w[pattern_indices[0]][j][0])
        return translators

    # This list keeps track of the index (=row) for columns in the difference
    # vector table. row_indices[k] is the row number for the column k.
    row_indices = []
    for _ in range(0, pattern_len):
        row_indices.append(0)

    finished = False
    k = 1

    while not finished:
        if row_indices[k] <= row_indices[k - 1]:
            row_indices[k] = row_indices[k - 1] + 1

        while row_indices[k] <= data_size - pattern_len + k \
                and w[pattern_indices[k]][row_indices[k]][0] < w[pattern_indices[k - 1]][row_indices[k - 1]][0]:
            row_indices[k] += 1

        if row_indices[k] > data_size - pattern_len + k:
            finished = True
        elif w[pattern_indices[k]][row_indices[k]][0] > w[pattern_indices[k - 1]][row_indices[k - 1]][0]:
            k = 1
            row_indices[0] += 1
            if row_indices[0] > data_size - pattern_len + 1:
                finished = True
        elif k == len(pattern_indices) - 1:
            translators.append(w[pattern_indices[k]][row_indices[k]][0])
            k = 0
            while k < pattern_len:
                row_indices[k] += 1
                if row_indices[k] > data_size - pattern_len + k:
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
    p = deepcopy(d)
    best_tecs = []

    while p:
        best_tec = get_best_tec(p, d)
        best_tecs.append(best_tec)
        p.remove_all(best_tec.coverage())

    return best_tecs


def siatec_compress(d):
    """ Implements the SIATECCompress algorithm described in [Meredith2013]. """

    d.sort_ascending()
    v, w = compute_vector_tables(d)
    mcps = compute_mtp_cis_pairs(v)
    remove_trans_eq_mtps(mcps)
    tecs = compute_tecs_from_mcps(d, w, mcps)
    add_conjugate_tecs(tecs, d)
    for tec in tecs:
        rem_red_tran(tec)
    sort_tecs_by_quality(tecs, d)
    return compute_encoding(tecs, d)


def remove_trans_eq_mtps(mcps):
    """ Removes translationally equivalent MTPs from mcps by
        removing redundant copies of MTPs that have the same
        vectorized representation. """

    i = 0
    while i < len(mcps):
        mcp = mcps[i]
        vectorized = vec(mcp[0])

        j = i + 1
        while j < len(mcps):
            if vectorized == vec(mcps[j][0]):
                mcps.pop(j)
            else:
                j += 1

        i += 1


def compute_tecs_from_mcps(d, v, mcps):
    tecs = []

    for mcp in mcps:
        tecs.append(get_tec_for_mtp(mcp[1], v, d))

    return tecs


def add_conjugate_tecs(tecs, d):
    conj_tecs = []
    for tec in tecs:
        conj_tecs.append(get_conj(tec, d))

    tecs += conj_tecs


def sort_tecs_by_quality(tecs, sorted_dataset):
    tecs.sort(key=cmp_to_key(lambda tec1, tec2: tec_quality_cmp(tec1, tec2, sorted_dataset)))


def tec_quality_cmp(tec1, tec2, sorted_dataset):
    if is_better_tec(tec1, tec2, sorted_dataset):
        return -1
    else:
        return 1


def compute_encoding(tecs, d):
    """ Implements algorithm in Figure 7 of [Meredith2013]. """

    best_tecs = []
    cover = []

    for i in range(0, len(tecs)):
        tec = tecs[i]
        s = tec.coverage()
        s_diff_cover = deepcopy(s)
        for p in cover:
            if p in s_diff_cover:
                s_diff_cover.remove(p)

        if len(s_diff_cover) > len(tec.get_pattern()) + len(tec.get_translators()) - 1:
            best_tecs.append(tec)
            cover += s

            dataset_covered = True
            for p in d:
                if p not in cover:
                    dataset_covered = False
                    break

            if dataset_covered:
                break

    return best_tecs


def get_best_tec(p, d):
    """ Finds the best TEC in p, the copy of the dataset d. Implements algorithm in Figure 2 of [Meredith2013].  """

    v, w = compute_vector_tables(p)
    mcps = compute_mtp_cis_pairs(v)
    best_tec = None

    for i in range(0, len(mcps)):
        mcp = mcps[i]
        mtp_indices = mcp[1]
        tec = get_tec_for_mtp(mtp_indices, w, p)
        conj = get_conj(tec, d)
        rem_red_tran(tec)
        rem_red_tran(conj)

        if not best_tec or is_better_tec(tec, best_tec, d):
            best_tec = tec
        if is_better_tec(conj, best_tec, d):
            best_tec = conj

    return best_tec


def compute_vector_tables(p):
    """ Compute the vector table V as defined in [Meredith2013],
        and the vector table W as needed by SIATEC [Meredith2002]. """

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
    """ Implements algorithm of Figure 3 from [Meredith2013].
        Returns a list of pairs where the first element is the set of
        vectors in the MTP and the second element is the list of indices
        for those vectors in the sorted dataset. """

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
    # TODO: Find a way to implement this.
    pass


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


def siact(d, compactness_th, cardinality_th, mtp_algorithm=sia):
    """ Implements the SIACT algorithm defined in Definition 7.2 of [Collins2011].
        Takes as its parameter the mtp_algorithm used for finding the MTPs of dataset d. """

    # First find MTPs of the dataset.
    mtps = mtp_algorithm(d)

    # Compactness trawl through each MTP
    compacted_mtps = []

    for mtp in mtps:
        compacted_mtps += compactness_trawl(mtp, compactness_th, cardinality_th, d)

    return compacted_mtps


def compactness_trawl(mtp, compactness_th, cardinality_th, sorted_dataset):
    """ Performs compactness trawling on an MTP as defined in Definition 7.2 of [Collins2011].
        Returns a list of patterns obtained from the input mtp.
        compactness_th is the compactness and cardinality_th the cardinality threshold. """

    diff_vector = mtp[0]
    pattern = mtp[1]

    compacted_mtps = []
    i = 0
    j = 0
    whole_pattern_compact = True

    while j < len(pattern) - 1:
        subpattern = pattern[i:j + 2]
        begin, end = heuristics.find_pattern_indices(subpattern, sorted_dataset)

        compactness = heuristics.compactness(begin, end, len(subpattern), sorted_dataset)
        if compactness < compactness_th:
            whole_pattern_compact = False
            compact_pattern = pattern[i:j + 1]

            if len(compact_pattern) >= cardinality_th:
                compacted_mtps.append((diff_vector, compact_pattern))

            i = j + 1

        j += 1

    # If the whole pattern has compactness above a, then check to see if it is large enough.
    if whole_pattern_compact and len(pattern) >= cardinality_th:
        compacted_mtps.append(mtp)

    return compacted_mtps


def siar(d, r):
    """ Implements SIAR as defined in [Collins2011] and [Meredith2016] Fig.13.14.
        Takes as parameters the dataset d and the number of subdiagonals r."""

    d.sort_ascending()

    # Compute r subdiagonals of vector table and store in V
    V = []
    for i in range(0, len(d) - 1):
        j = i + 1
        while j < len(d) and j <= i + r:
            V.append((d[j] - d[i], i))
            j += 1

    # Store patterns in E by sorting and segmenting V
    V.sort()
    E = []
    v = V[0][0]
    e = [d[V[0][1]]]
    for i in range(1, len(V)):
        if V[i][0] == v:
            e.append(d[V[i][1]])
        else:
            E.append(e)
            e = [d[V[i][1]]]
            v = V[i][0]

    E.append(e)

    # For each pattern in E, find +ve inter-point vectors and store in L
    L = []
    for i in range(0, len(E)):
        e = E[i]
        for j in range(0, len(e) - 1):
            for k in range(j + 1, len(e)):
                L.append(e[k] - e[j])

    # Remove duplicates from L and order vectors by decreasing frequency.
    L.sort()
    v = L[0]
    f = 1
    M = []
    for i in range(1, len(L)):
        if L[i] == v:
            f += 1
        else:
            M.append((v, f))
            f = 1
            v = L[i]

    M.append((v, f))
    M.sort(key=itemgetter(1), reverse=True)

    # Find the MTP for each vector in M, store it in S and return S
    S = []
    set_d = set(d)
    for i in range(0, len(M)):
        S.append(find_mtp(d, M[i][0], set_d))

    return S


def find_mtp(d, diff_vec, set_d):
    """ Find the MTP for diff_veb by finding the intersection of the sorted dataset
        d and the dataset translated by -diff_vec. """

    pattern = []

    for point in d:
        if point - diff_vec in set_d:
            pattern.append(point)

    mtp = (diff_vec, pattern)
    return mtp






from orig_algorithms import vec
from orig_algorithms import siatec
from orig_algorithms import sort_tecs_by_quality
from dataset import Dataset
from tec import TEC
from pattern import Pattern


def siah(d):
    """ Computes the MTPs of dataset d.
        Uses a dictionary/map to avoid having to sort the
        set of difference vectors. Runs in O(kn^2) average time. """

    d = Dataset.sort_ascending(d)
    # Dictionary of difference vector, index list pairs.
    mtp_dict = {}

    # Compute the difference vectors between points and add
    # the starting indexes to the lists corresponding to the
    # difference vector.
    for i in range(len(d)):
        for j in range(i + 1, len(d)):
            diff = d[j] - d[i]
            if diff in mtp_dict:
                mtp_dict[diff].append(i)
            else:
                mtp_dict[diff] = [i]

    # Collect the MTPs from the map.
    mtps = []
    for diff in mtp_dict:
        points = []
        for index in mtp_dict[diff]:
            points.append(d[index])

        mtps.append((diff, points))

    return mtps


def siatech(d):
    d = Dataset.sort_ascending(d)
    # Map of difference vector, index list pairs.
    mtp_map = {}

    # Compute the difference vectors between points and add both
    # the starting and ending index as pair to the lists corresponding to the
    # difference vector.
    for i in range(len(d)):
        for j in range(i + 1, len(d)):
            diff = d[j] - d[i]
            if diff in mtp_map:
                mtp_map[diff].append((i, j))
            else:
                mtp_map[diff] = [(i, j)]

    tecs = []
    single_point_pattern_handled = False
    handled_patterns = set()

    for diff_vec in mtp_map:
        pattern = []
        pattern_indices = []
        mtp = mtp_map[diff_vec]

        for index_pair in mtp:
            pattern_indices.append(index_pair[0])
            pattern.append(d[index_pair[0]])

        vectorized_pattern = Pattern(vec(pattern))

        if vectorized_pattern not in handled_patterns:
            translators = []
            if len(pattern) == 1 and not single_point_pattern_handled:
                for point in d:
                    translators.append(point - pattern[0])
                single_point_pattern_handled = True
            else:
                translators = find_translators(pattern, vectorized_pattern, mtp_map, d)

            tecs.append(TEC(pattern, pattern_indices, translators))
            handled_patterns.add(vectorized_pattern)

    return tecs


def find_translators(mtp, vectorized_mtp, mtp_map, sorted_dataset):
    target_indices = []
    for index_pair in mtp_map[vectorized_mtp[0]]:
        target_indices.append(index_pair[1])

    for i in range(1, len(vectorized_mtp)):
        v = vectorized_mtp[i]
        index_pair_list = mtp_map[v]

        tmp_target_indices = []
        i = 0
        j = 0
        while i < len(target_indices) and j < len(index_pair_list):
            if target_indices[i] == index_pair_list[j][0]:
                tmp_target_indices.append(index_pair_list[j][1])
                i += 1
                j += 1
            elif target_indices[i] < index_pair_list[j][0]:
                i += 1
            elif target_indices[i] > index_pair_list[j][0]:
                j += 1

        target_indices = tmp_target_indices

    translators = []
    last_point = mtp[len(mtp) - 1]

    for index in target_indices:
        p = sorted_dataset[index]
        translators.append(p - last_point)

    return translators


def cosiatech(d):
    tecs = siatec(d)
    sort_tecs_by_quality(tecs, d)

    best_tecs = []
    covered_points = set() # This is unnecessary, could be implemented by just looking at the indexes in the sorted d
    for i in range(len(tecs)):
        tec = tecs[i]

        contains_new_points = True
        covered_set = tec.coverage()

        for point in covered_set:
            if point in covered_points:
                contains_new_points = False
                break

        if contains_new_points:
            best_tecs.append(tec)
            for point in covered_set:
                covered_points.add(point)

        if len(covered_set) == len(d):
            break

    residual_points = []
    for p in d:
        if p not in covered_points:
            residual_points.append(p)

    best_tecs.append(TEC(residual_points, [], []))

    return best_tecs


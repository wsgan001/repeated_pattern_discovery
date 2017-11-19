from dataset import Dataset


def sia_hash(d):
    """ Computes the MTPs of dataset d.
        Uses a dictionary/map to avoid having to sort the
        set of difference vectors. Runs in O(kn^2) time. """

    d.sort_ascending()
    # Map of difference vector, index list pairs.
    mtp_map = {}

    # Compute the difference vectors between points and add
    # the starting indexes to the lists corresponding to the
    # difference vector.
    for i in range(len(d)):
        for j in range(i + 1, len(d)):
            diff = d[j] - d[i]
            if diff in mtp_map:
                mtp_map[diff].append(i)
            else:
                mtp_map[diff] = [i]

    # Collect the MTPs from the map.
    mtps = []
    for diff in mtp_map:
        points = []
        for index in mtp_map[diff]:
            points.append(d[index])

        mtps.append((diff, points))

    return mtps


import algorithms


def bounding_box_compactness(tec, sorted_dataset):
    """ Computes the fraction of points belonging to the pattern of the TEC in
        the minimum bounding box of the pattern. """

    pattern_size = len(tec.get_pattern_indices())
    if pattern_size == 1:
        return 1

    min_vector, max_vector = tec.get_bounding_box()

    selection_begin = tec.get_pattern_indices()[0]
    selection_end = tec.get_pattern_indices()[pattern_size - 1]

    # Extend selection in case there are points that have the same first component
    # as the minimum or maximum vectors.
    for i in range(selection_end, len(sorted_dataset)):
        if sorted_dataset[selection_end] <= max_vector:
            selection_end += 1
        else:
            break

    for i in range(selection_begin, 0, -1):
        if sorted_dataset[selection_begin] >= min_vector:
            selection_begin -= 1
        else:
            break

    selection_from_data = sorted_dataset[selection_begin:selection_end]
    num_points_in_bb = 0

    for p in selection_from_data:
        if is_within_bb(p, max_vector, min_vector):
            num_points_in_bb += 1

    return pattern_size / num_points_in_bb


def is_within_bb(point, max_vector, min_vector):
    """ Check if point is within the closed bounding box limited by
        max_vector and min_vector. """

    for i in range(0, point.dimensionality()):
        component = point[i]
        if component > max_vector[i]:
            return False

        if component < min_vector[i]:
            return False

    return True


def convex_hull_compactness(pattern_indices, sorted_dataset):
    return 1


def compression_ratio(tec):
    """ Computes compression ratio as defined in equation 10 [Meredith2013]. """

    return len(tec.coverage()) / (len(tec.get_pattern()) + len(tec.get_translators()) - 1)


def pattern_width(tec):
    """ Computes the difference of the greatest and smallest first components
        in the pattern. The first component is typically considered to express
        onset time of the pitch event.
        [Meredith2013] """

    min_first_comp = float('inf')
    max_first_comp = float('-inf')

    for p in tec.get_pattern():
        if p[0] < min_first_comp:
            min_first_comp = p[0]
        if p[0] > max_first_comp:
            max_first_comp = p[0]

    return max_first_comp - min_first_comp


def pattern_volume(tec):
    """ Computes the volume (area for 2-dimensional patterns) of the bounding box of the TEC pattern. """

    min_vec, max_vec = tec.get_bounding_box()
    differences = []
    for i in range(0, min_vec.dimensionality()):
        differences.append(max_vec[i] - min_vec[i])

    volume = 1
    for diff in differences:
        volume *= diff

    return volume

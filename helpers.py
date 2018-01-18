from copy import deepcopy
from vector import Vector
from tec import TEC
from dataset import Dataset


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


def print_mtp_set_properties(mtps, dataset):
    print('Number of MTPs:', len(mtps))
    print('Max number of MTPs in dataset:', int(len(dataset) * (len(dataset) - 1) / 2))
    print('Min number of MTPs in dataset:', len(dataset) - 1)
    
    avg_size = 0
    size_of_largest = 0
    for mtp in mtps:
        mtp_size = len(mtp[1])
        avg_size += mtp_size
        if mtp_size > size_of_largest:
            size_of_largest = mtp_size

    avg_size /= len(mtps)
    print('Average MTP size:', avg_size)
    print('Largest MTP size:', size_of_largest)


def print_tecs(tecs):
    print('Printing TECs, count=' + str(len(tecs)))
    for tec in tecs:
        print(str(tec))


def mtp_sets_are_same(mtps1, mtps2):
    """ Check that two sets of mtps are the same """

    mtps1_c = deepcopy(mtps1)
    mtps2_c = deepcopy(mtps2)

    mtps1_c.sort()
    mtps2_c.sort()

    return mtps1_c == mtps2_c


def tec_sets_are_same(tecs1, tecs2):

    covered_sets1 = get_covered_sets_of_tec_list(tecs1)
    covered_sets2 = get_covered_sets_of_tec_list(tecs2)

    return covered_sets1 == covered_sets2


def get_covered_sets_of_tec_list(tecs):
    covered_sets = []
    for t in tecs:
        cov_list = list(t.coverage())
        cov_list.sort()
        covered_sets.append(cov_list)

    return covered_sets


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


def tec_in_list(tec, list_of_tecs):
    cov_tec = tec.coverage()

    for t in list_of_tecs:
        cov_t = t.coverage()
        if cov_tec == cov_t:
            return True

    return False


def get_tecs_for_Meredith2002_fig11():
    exp_res = []
    exp_res.append(TEC([Vector([1, 3])], [], [Vector([0, -2]), Vector([0, 0]), Vector([1, -2]),
                                              Vector([1, -1]), Vector([1, 0]), Vector([2, -1])]))

    exp_res.append(TEC([Vector([2, 1]), Vector([2, 2])], [], [Vector([0, 0]), Vector([0, 1])]))

    exp_res.append(TEC([Vector([1, 1]), Vector([2, 1])], [], [Vector([0, 0]), Vector([0, 2]), Vector([1, 1])]))

    exp_res.append(TEC([Vector([1, 1]), Vector([1, 3]), Vector([2, 2])], [], [Vector([0, 0]), Vector([1, 0])]))
    return exp_res


def simplified_vec_str(vec):
    comps = []
    for k in range(vec.dimensionality()):
        comps.append(str(int(vec[k])))

    return '(' + ','.join(comps) + ')'


def print_v_for_dataset(dataset):
    """ Prints the difference vector table V for a dataset in a format almost suitable for copypasting to LaTeX. """
    dataset = Dataset.sort_ascending(dataset)
    table_lines = [['\ ']]

    for i in range(len(dataset)):
        table_lines[0].append('$' + simplified_vec_str(dataset[i]) + '$')

    for i in range(0, len(dataset)):
        table_lines.append(['$' + simplified_vec_str(dataset[i]) + '$'])

    for i in range(len(dataset)):
        for j in range(len(dataset)):
            if i < j:
                table_lines[j + 1].append('$\\langle ' + simplified_vec_str(dataset[j] - dataset[i]) + ', ' + str(i) + '\\rangle $')
            else:
                table_lines[j + 1].append('\\ ')

    pos_string = '|'.join(['c' for v in dataset])
    print('\\begin{tabular}[pos]{' + pos_string + '|c}')

    for i in range(len(table_lines)):
        print('\t' + ' & '.join(table_lines[i]) + '\\\\')

    print('\\end{tabular}')


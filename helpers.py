from copy import deepcopy


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



from input_func import input_func

def compute_score_transition(s1: list, s2: list):
    """
    compute score transition

    :param s1:
    :param s2:
    :return:

    assert(compute_score_transition([1,2,3], [3,5,6]) == 1)
    assert(compute_score_transition([1,2], [6]) == 0)
    assert(compute_score_transition([1,2,3, 4], [3,4,5,6]) == 2)
    """
    s1 = set(s1)
    s2 = set(s2)
    s_intersection = len(s1.intersection(s2))
    s_in_s1_not_in_s2 = len([tag for tag in s1 if tag not in s2])
    s_in_s2_not_in_s1 = len([tag for tag in s2 if tag not in s1])

    score = min([s_intersection,s_in_s1_not_in_s2, s_in_s2_not_in_s1])
    return score

def main():
    #horizontals, horizontal_ids, verticals, vertical_ids, dic = input_func('./data/b_lovely_landscapes.txt')
    #print(horizontals)

if __name__ == "__main__":
    main()



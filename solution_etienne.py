from __future__ import print_function
import os
import time
import numpy as np
import input_func
import compute_score
from solution_raphael import get_horiz_from_vert


def write_output(result_list, filename):
    with open(filename, 'w') as file:
        file.write(str(len(result_list))+"\n")
        for line in result_list:
            file.write(str(line)+"\n")

def maximize_horiz(horiz, n):
    slideshow = []
    taken = set()
    total_score = 0

    begin, end = 0, 0
    slideshow.append(0)

    for j in range(1, n):
        max_score = 0
        max_index = 0
        is_head = False
        # if j in taken:
        #     continue
        for i in range(j, n):
            # if i not in taken:
            s1 = compute_score.compute_score_transition(horiz[i][1], horiz[begin][1])
            s2 = compute_score.compute_score_transition(horiz[end][1], horiz[i][1])

            smax = max(s1, s2)
            if smax > max_score:
                is_head = s1 > s2
                max_score = smax
                max_index = i

            if smax > 2:
                break

        photo_id = horiz[max_index][0]
        if is_head:
            slideshow.insert(0, photo_id)
            begin = max_index
        else:
            slideshow.append(photo_id)
            end = max_index

        j = max_index

        total_score += max_score
        taken.add(max_index)
        print('score: ', total_score * 1e-3, j, '/', n)

    return slideshow, total_score


if __name__ == '__main__':
    file_path = "data/d_pet_pictures.txt"
    out_path = os.path.splitext(file_path)[0] + "_soluce.txt"

    horizontals, horizontal_ids, verticals, vertical_ids, dic, tags = input_func.input_func(file_path)


    lh = list(zip(horizontal_ids, horizontals))
    vh = list(zip(vertical_ids, verticals))
    lh = lh + get_horiz_from_vert(vh)


    #sort by num tags
    cat = [(len(tags), (id, tags) ) for id, tags in lh]
    z = sorted(cat)[::-1]

    final = [item[1] for item in z]

    print(final[0])

    print('start maximization')
    slideshow, score = maximize_horiz(final, len(final))
    print('total score: ', score)

    write_output(slideshow, out_path)

    #compute score
    compute_score.compute_score(file_path, out_path)



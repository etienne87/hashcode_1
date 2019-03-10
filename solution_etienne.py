from __future__ import print_function
import os
import random
import input_func
import compute_score
from solution_raphael import get_horiz_from_vert
from tqdm import tqdm


def write_output(result_list, filename):
    with open(filename, 'w') as file:
        file.write(str(len(result_list))+"\n")
        for line in result_list:
            file.write(str(line)+"\n")

def maximize_horiz_early_stop(horiz, n):
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

def maximize_horiz_brute_force(horiz, n, slideshow=None, total_score=0, taken=None, use_local=True, return_local=False):
    if slideshow is None:
        slideshow = []

    if taken is None:
        taken = set()


    localslideshow = []
    begin = 0
    end = begin
    taken.add(horiz[begin][0])

    localslideshow.append(horiz[begin][0])
    local_total_score = 0

    if return_local:
        use_local = True

    if not use_local:
        localslideshow = slideshow


    j = 0
    for j in range(n):
        jid = horiz[j][0]
        if jid in taken:
            continue

        max_score = 0
        max_index = min(n-1, j+1)
        is_head = False

        for i in range(0, n):
            iid = horiz[i][0]

            if iid not in taken:
                s1 = compute_score.compute_score_transition(horiz[i][1], horiz[begin][1])
                s2 = compute_score.compute_score_transition(horiz[end][1], horiz[i][1])

                smax = max(s1, s2)
                if smax > max_score:
                    is_head = s1 > s2
                    max_score = smax
                    max_index = i

        photo_id = horiz[max_index][0]
        if is_head:
            localslideshow.insert(0, photo_id)
            begin = max_index
        else:
            localslideshow.append(photo_id)
            end = max_index
        local_total_score += max_score
        taken.add(photo_id)
        if j%100 == 0:
            tmp_score = 0
            if return_local:
                tmp_score = local_total_score
            else:
                tmp_score = total_score
            print('score: ', tmp_score * 1e-3, j, '/', n)

    if return_local:
        return localslideshow, local_total_score

    if use_local:
        slideshow += localslideshow
        total_score += local_total_score
    else:
        slideshow = localslideshow
        total_score = local_total_score


    return slideshow, total_score

def maximize_groups_brute_force(groups):
    slideshow = groups[0][0]
    taken = set()

    for i in range(n):
        pass


def maximize_bruteforce_cluster(horiz, n, k=1000):
    size = n/k

    #V1
    overlap = size
    groups = [horiz[max(0,i*size-overlap):min(n,(i+1)*size+overlap)] for i in range(k)]
    last = -1
    slideshow = None
    score = 0
    taken = set()
    for i in range(k):
        slideshow, score = maximize_horiz_brute_force(groups[i], len(groups[i]), slideshow, score, taken)

    return slideshow, score


def sort_by_num_tags(photos):
    cat = [(len(tags), (id, tags)) for id, tags in photos]
    z = sorted(cat)[::-1]
    final = [item[1] for item in z]
    return final


def make_undic(dic):
    undic = {}
    for k, v in dic.iteritems():
        undic[v] = k
    return undic



def get_horiz_from_vert_etienne(list_vert):
    list_horiz_bonus = []
    taken = set()
    for i in tqdm(range(len(list_vert))):
        if i in taken:
            continue
        a = list_vert[i]
        aset = set(a[1])
        max_len = 0
        max_idx = 0
        for j in range(len(list_vert)):
            if j in taken or i == j:
                continue
            b = list_vert[j]
            bset = set(b[1])

            ulen = len(aset.union(bset))
            if ulen > max_len:
                max_len = ulen
                max_idx = j

            if ulen > len(a):
                break

        b = list_vert[max_idx]
        list_horiz_bonus += [(str(a[0])+" "+str(b[0]), list(set(a[1]+b[1])))]


    return list_horiz_bonus


if __name__ == '__main__':
    input_files = ["data/a_example.txt",
                   "data/b_lovely_landscapes.txt",
                   "data/c_memorable_moments.txt",
                   "data/d_pet_pictures.txt",
                   "data/e_shiny_selfies.txt"]

    file_path = input_files[3]
    out_path = os.path.splitext(file_path)[0] + "_soluce.txt"

    horizontals, horizontal_ids, verticals, vertical_ids, dic, tags = input_func.input_func(file_path)


    lh = list(zip(horizontal_ids, horizontals))
    vh = list(zip(vertical_ids, verticals))

    vh_sorted = sort_by_num_tags(vh)

    lh = lh + get_horiz_from_vert_etienne(vh_sorted)


    #sort by num tags
    final = sort_by_num_tags(lh)

    print('start maximization')
    slideshow, score = maximize_bruteforce_cluster(final, len(final))
    print('total score: ', score)


    print('write output: ')
    write_output(slideshow, out_path)

    submit_score = compute_score.compute_score(file_path, out_path)
    print('confirm score: ', submit_score)




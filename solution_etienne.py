from __future__ import print_function
import os
import random
import input_func
import compute_score
from solution_raphael import get_horiz_from_vert

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


def maximize_bruteforce_cluster(horiz, n, k=100):
    size = n/k

    #V1
    groups = [horiz[max(0,i*size-size/2):min(n,(i+1)*size+size/2)] for i in range(k)]
    last = -1
    slideshow = None
    score = 0
    taken = set()
    for i in range(k):
        slideshow, score = maximize_horiz_brute_force(groups[i], len(groups[i]), slideshow, score, taken)

    #V2
    #groups = [horiz[i*size:(i+1)*size] for i in range(k)]


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


def random_solution(all, n, threshold=1):
    #take n @ random that match
    slideshow = [random.randint(0, n)]
    begin, end = slideshow[0], slideshow[0]
    total_score = 0
    taken = set()
    print('make random solution: ')
    rng = range(n)
    for i in range(n):
        if i in taken:
            continue

        max_score = 0
        max_index = min(n - 1, i + 1)
        is_head = False
        random.shuffle(rng)
        for j in rng:

            if j in taken:
                continue

            s1 = compute_score.compute_score_transition(all[i][1], all[begin][1])
            s2 = compute_score.compute_score_transition(all[end][1], all[i][1])

            smax = max(s1, s2)
            if smax > max_score:
                is_head = s1 > s2
                max_score = smax
                max_index = i

            if smax > threshold:
                break

        photo_id = all[max_index][0]
        if is_head:
            slideshow.insert(0, photo_id)
            begin = max_index
        else:
            slideshow.append(photo_id)
            end = max_index

        total_score += max_score
        taken.add(max_index)
        print('score: ', total_score * 1e-3, i, '/', n)

    return slideshow, total_score


def evaluate(photo_ids, all_tags):
    slideshow = compute_score.photo_ids_to_tags(photo_ids, all_tags)
    score = 0
    for i in range(len(slideshow) - 1):
        score += compute_score.compute_score_transition(slideshow[i], slideshow[i + 1])
    return score

# def mutate(n_muts):
#     for i in range(n_muts):
#

def hill_climbing(all, n, popsize=5, max_iter=1000):
    population = []
    for i in range(popsize):
        sol, score = random_solution(all, 100)
        population.append((sol, score))

    for iter in range(max_iter):
        #mutate population
        population = []

        #evaluate
        population = [(item[0], evaluate(item[0])) for item in population]
        population = sorted(population, key=lambda x: x[1], reverse=True)

        print('best score: ', population[0][1])

        #selection, add random
        population = population[:int(popsize*2/3)]
        for i in range(len(population), popsize):
            sol, score = random_solution(all, n)
            population.append((sol,score))




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
    lh = lh + get_horiz_from_vert(vh)


    #sort by num tags
    final = sort_by_num_tags(lh)

    print('start maximization')
    slideshow, score = maximize_bruteforce_cluster(final, len(final))
    print('total score: ', score)


    print('write output: ')
    write_output(slideshow, out_path)

    print('confirm score: ')
    compute_score.compute_score(file_path, out_path)



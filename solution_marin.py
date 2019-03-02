import numpy as np
import os
import sys
from input_func import input_func
import time

from compute_score import compute_score_transition, compute_score
indice_file = 3
list_name_input = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]

heuristic_each_map = [10000,8,10000,100,15] # e is more around 9-14...

name_file_input = list_name_input[indice_file]

MAX_HEURISTIC = heuristic_each_map[indice_file]
MIN_HEURISTIC = 4
initial_heurisitc_score_bien = MAX_HEURISTIC

use_sorted = True

file_path = "/home/toromanoff/workspace/pypy/hashcode_1/data/input/"+name_file_input+".txt"

horizontals_tags, horizontal_ids, verticals_tags, vertical_ids, dic, all_tags = input_func(file_path)

#print(horizontals_tags, horizontal_ids, verticals_tags, vertical_ids, dic, all_tags)

def write_output(result_list, filename):
    with open(filename, 'w') as file:
        file.write(str(len(result_list))+"\n")
        for line in result_list:
            file.write(str(line)+"\n")

def get_tag_pair_vertical(tag_vertical_0, tag_vertical_1):
    return list(set(tag_vertical_0 + tag_vertical_1))

def get_horiz_from_vert(vertical_ids, verticals_tags):

    half_length = int(len(vertical_ids)/2)
    pair_horiz_ids = []
    pair_horiz_tags = []
    for i in range(half_length):
        pair_horiz_ids.append(str(vertical_ids[2*i]) + " " + str(vertical_ids[2*i+1]))
        pair_horiz_tags.append(get_tag_pair_vertical(verticals_tags[2*i], verticals_tags[2*i+1]))
    return pair_horiz_ids, pair_horiz_tags

def get_horiz_from_vert_raph(list_vert):

    half_length = len(list_vert)//2
    list_horiz_bonus = []
    for i in range(half_length):
        list_horiz_bonus += [(str(list_vert[2*i][0])+" "+str(list_vert[2*i+1][0]), list(set(list_vert[2*i][1]+list_vert[2*i+1][1])))]
    return list_horiz_bonus

MIN_LOSS_PAIR = 0

def get_horiz_from_vert_sorted(vh_sorted):
    list_vert_available = [i for i in range(len(vh_sorted))]
    list_horiz_bonus = []
    while (len(list_vert_available) > 1):
        indice_max = list_vert_available.pop(0)
        current_max_tag_vert = vh_sorted[indice_max]
        current_min_loss_pair = 1000
        indice_min_loss_pair = -1

#        print("indice_max = ", indice_max)
#        print("len(list_vert_available) = ", len(list_vert_available))

        for current_indice_min_tag_vert in reversed(list_vert_available):
#            print("current_indice_min_tag_vert = ", current_indice_min_tag_vert)
            current_min_tag_vert = vh_sorted[current_indice_min_tag_vert]

            current_loss_pair = len(set(current_max_tag_vert[1]).intersection(current_min_tag_vert[1]))
            if current_min_loss_pair > current_loss_pair:
                current_min_loss_pair = current_loss_pair
                indice_min_loss_pair = current_indice_min_tag_vert

            if current_loss_pair <= MIN_LOSS_PAIR:
#                print("we break")
                indice_min_loss_pair = current_indice_min_tag_vert
                break
        if current_min_loss_pair > MIN_LOSS_PAIR:
            print("we didnt find any pair with loss MIN_LOSS_PAIR, loss was  = ", current_min_loss_pair)

#        print("str(current_max_tag_vert[0]) = ", str(current_max_tag_vert[0]))
#        print("str(vh_sorted[indice_min_loss_pair][0]) = ", str(vh_sorted[indice_min_loss_pair][0]))
        list_horiz_bonus += [(str(current_max_tag_vert[0])+" "+str(vh_sorted[indice_min_loss_pair][0]), list(set(current_max_tag_vert[1]+vh_sorted[indice_min_loss_pair][1])))]
        assert indice_min_loss_pair in list_vert_available
        list_vert_available.remove(indice_min_loss_pair)

    return list_horiz_bonus

# TO IMPROVE WE JUST PUT TOGETHER CONSECUTIVE VERTICAL
#pair_horiz_ids, pair_horiz_tags = get_horiz_from_vert(vertical_ids, verticals_tags)
#
#all_tags = horizontals_tags + pair_horiz_tags
#all_ids = horizontal_ids + pair_horiz_ids

if use_sorted:

    horizontals, horizontal_ids, verticals, vertical_ids, dic, all_tags = input_func(file_path)


    print("number of horizontals :", len(horizontals))
    print("number of verticals :", len(verticals))

    lh = list(zip(horizontal_ids, horizontals))
    vh = list(zip(vertical_ids, verticals))
    vh_sorted = [(len(tags), (id, tags) ) for id, tags in vh]
    vh_sorted = sorted(vh_sorted,key=lambda x:x[0])[::-1]
    vh_sorted = [item[1] for item in vh_sorted]

    print("my fonction")
    start_time = time.time()
    lh = lh + get_horiz_from_vert_sorted(vh_sorted)
    print("duration = " , time.time() - start_time)
    print("my fonction ended")
    #sort by num tags
    cat = [(len(tags), (id, tags) ) for id, tags in lh]
    z = sorted(cat,key=lambda x:x[0])[::-1]
    list_all = [item[1] for item in z]

    all_tags = [item[1] for item in list_all]
    all_ids = [item[0] for item in list_all]

position_photo_available = [i for i in range(len(all_tags))]

assert len(all_tags) == len(all_ids)

first_photo_position = 0
position_photo_available.remove(first_photo_position)

position_photo_right = first_photo_position
position_photo_left = first_photo_position

solution_final = [first_photo_position]

print("name_file_input = ", name_file_input)
print("(len(all_tags) = ", len(all_tags))
print("initial_heurisitc_score_bien= ", initial_heurisitc_score_bien)
print("use_sorted= ", use_sorted)

start_time = time.time()
current_heurisitc_score_bien = initial_heurisitc_score_bien


while len(position_photo_available) > 0:
    if len(position_photo_available) % 1000 == 0:
        print("len(position_photo_available) = ", len(position_photo_available) )
        print("duration = " , time.time() - start_time)
        start_time = time.time()
    left = False
    position_max_current_score = position_photo_available[0]
    current_score_left = compute_score_transition(all_tags[position_photo_left], all_tags[position_max_current_score])
    current_score_right = compute_score_transition(all_tags[position_photo_right], all_tags[position_max_current_score])
    if current_score_right > current_score_left:
        left = True

    max_current_score = max(current_score_left, current_score_right)
    find_any_heuristic = False
    for position_photo_still_available in position_photo_available[1:]:
#        print("int(len(all_tags[position_photo_right])/2) = ", int(len(all_tags[position_photo_right])/2))

        if min(current_heurisitc_score_bien, len(all_tags[position_photo_still_available])//2) <= max_current_score:
            find_any_heuristic = True
            if max_current_score >= current_heurisitc_score_bien:
                current_heurisitc_score_bien = min(MAX_HEURISTIC,current_heurisitc_score_bien+1)
                print("we found one, let's augment the heuristic", current_heurisitc_score_bien)
            break

        current_score_left = compute_score_transition(all_tags[position_photo_left], all_tags[position_photo_still_available])
        current_score_right = compute_score_transition(all_tags[position_photo_right], all_tags[position_photo_still_available])
        if current_score_right > max_current_score and current_score_right > current_score_left:
            position_max_current_score = position_photo_still_available
            max_current_score = current_score_right
            left = False

        elif current_score_left > max_current_score and current_score_left > current_score_right:
            position_max_current_score = position_photo_still_available
            max_current_score = current_score_left
            left = True

    if not find_any_heuristic:
        current_heurisitc_score_bien = max(MIN_HEURISTIC,current_heurisitc_score_bien-1)
        print("we didn't found one, let's diminue the heuristic", current_heurisitc_score_bien)

    if left:
        solution_final.insert(0,position_max_current_score)
        position_photo_left = position_max_current_score

    else:
        solution_final.append(position_max_current_score)
        position_photo_right = position_max_current_score

    position_photo_available.remove(position_max_current_score)

#print("solution_final = ", solution_final)

vrai_solution_final = [all_ids[i] for i in solution_final]

#print("vrai_solution_final = ", vrai_solution_final)

print("name_file_input = ", name_file_input)
print("(len(all_tags) = ", len(all_tags))
print("final current_heurisitc_score_bien= ", current_heurisitc_score_bien)

if use_sorted:
    write_output(vrai_solution_final , "/home/toromanoff/workspace/pypy/hashcode_1/data/"+name_file_input+"sortednew"+str(initial_heurisitc_score_bien)+".out")
else:
    write_output(vrai_solution_final , "/home/toromanoff/workspace/pypy/hashcode_1/data/"+name_file_input+"new.out")
#list_horizontal, list_vertical = input_func(file_path)

#list_horizontal liste de liste avec id photo + set id tag
#list_vertical liste de liste avec id photo + set id tag

#list_id_vertical = "TODO GET ALL ID VERTICAL"

#from itertools import combinations
#
#list_all_pair_vertical = [",".join(map(str, comb)) for comb in combinations(list_id_vertical, 2)]
#

#
#def get_number_tag_pair_vertical(id_vertical_0, id_vertical_1):
#    return len(set(id_vertical_0 + id_vertical_1))
#
#
#for pair_vertical in list_all_pair_vertical:


#list_vertical_transformed_to_horizontal = get_horiz_from_vert(list_vertical)


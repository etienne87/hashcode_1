import numpy as np
import os
import sys
from input_func import input_func
import time

import argparse

from compute_score import compute_score_transition, compute_score

parser = argparse.ArgumentParser(description='Rainbow')
parser.add_argument('--indice-input-file', type=int)
parser.add_argument('--factor-loss-tag-in-pair', type=float)
args = parser.parse_args()
indice_file = args.indice_input_file
if indice_file is None:
    sys.exit("You must add --indice-input-file to choose which exemple you want to compute")
    
list_name_input = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]

heuristic_each_map = [100,100,100,100,100] # e is more around 9-14...

name_file_input = list_name_input[indice_file]

MAX_HEURISTIC = heuristic_each_map[indice_file]
MIN_HEURISTIC = 100
initial_heurisitc_score_bien = MAX_HEURISTIC

FACTOR_LOSS_TAG_IN_PAIR = args.factor_loss_tag_in_pair

# The idea there is to take the first 8 first most interesting vertical, and then for all them check pairs and take the final best of all them, specific to E!
NB_PAIR_TO_CHECK = 8 # Should take around 16 hours with 8...

use_sorted = True

file_path = "./data/input/"+name_file_input+".txt"

#print(horizontals_tags, horizontal_ids, verticals_tags, vertical_ids, dic, all_tags)

def compute_tag_pair_vertical(tag_vert1, tag_vert2):
    return list(set(tag_vert1 + tag_vert2))

def write_output(result_list, filename):
    with open(filename, 'w') as file:
        file.write(str(len(result_list))+"\n")
        for line in result_list:
            file.write(str(line)+"\n")

MIN_LOSS_PAIR = 0

# TO IMPROVE WE JUST PUT TOGETHER CONSECUTIVE VERTICAL
#pair_horiz_ids, pair_horiz_tags = get_horiz_from_vert(vertical_ids, verticals_tags)
#
#all_tags = horizontals_tags + pair_horiz_tags
#all_ids = horizontal_ids + pair_horiz_ids

horizontals, horizontal_ids, verticals, vertical_ids, dic, all_tags_useless = input_func(file_path)


print("number of horizontals :", len(horizontals))
print("number of verticals :", len(verticals))

lh = list(zip(horizontal_ids, horizontals))
vh = list(zip(vertical_ids, verticals))
#    vh_sorted = [(len(tags), (id, tags) ) for id, tags in vh]
#    vh_sorted = sorted(vh_sorted,key=lambda x:x[0])[::-1]
#    vh_sorted = [item[1] for item in vh_sorted]



#sort by num tags
cat_horiz = [(len(tags), (id, tags, False) ) for id, tags in lh]
cat_vertical = [(2*len(tags), (id, tags, True) ) for id, tags in vh] # We use heuristic that vertical is half of an horizontal one...

cat_all_image = cat_horiz + cat_vertical

z = sorted(cat_all_image,key=lambda x:x[0])[::-1]
list_all_sorted = [item[1] for item in z]

all_is_vert_sorted = [item[2] for item in list_all_sorted]
all_tags_sorted = [item[1] for item in list_all_sorted]
all_ids_sorted = [item[0] for item in list_all_sorted]

assert len(all_is_vert_sorted) == len(all_tags_sorted) == len(all_ids_sorted)

tab_position_vertical_sorted = [i for i in range(len(all_tags_sorted)) if all_is_vert_sorted[i]]

position_horizontal_sorted = [i for i in range(len(all_tags_sorted)) if not all_is_vert_sorted[i]] # THIS ONE IS USELESS I THINK, WE NEVER CARE ABOUT JUST HORIZONTAL

tab_position_vertical_available = tab_position_vertical_sorted
tab_position_photo_available = [i for i in range(len(all_tags_sorted))]

#print("tab_position_vertical_available = ", tab_position_vertical_available)
#print("position_horizontal_sorted = ", position_horizontal_sorted)

first_photo_position = 0
tab_position_photo_available.remove(first_photo_position)
is_first_vert = all_is_vert_sorted[first_photo_position]
if is_first_vert:
    tab_position_vertical_available.remove(first_photo_position)
    
    position_second_part_pair_intial_vert = tab_position_vertical_available[0]
    tab_position_vertical_available.remove(position_second_part_pair_intial_vert)
    tab_position_photo_available.remove(position_second_part_pair_intial_vert)

    position_photo_right = (first_photo_position, position_second_part_pair_intial_vert)
    position_photo_left = (first_photo_position, position_second_part_pair_intial_vert)
    
    solution_final = [(first_photo_position, position_second_part_pair_intial_vert)]

else:
    position_photo_right = first_photo_position
    position_photo_left = first_photo_position

    solution_final = [first_photo_position] # CARE ABOUT THIS LATER!!!

print("name_file_input = ", name_file_input)
print("(len(all_tags_sorted) = ", len(all_tags_sorted))
print("initial_heurisitc_score_bien= ", initial_heurisitc_score_bien)
print("MIN_HEURISTIC= ", MIN_HEURISTIC)
print("FACTOR_LOSS_TAG_IN_PAIR = ", FACTOR_LOSS_TAG_IN_PAIR)

start_time = time.time()
current_heurisitc_score_bien = initial_heurisitc_score_bien

while len(tab_position_photo_available) > 0 :
    if len(tab_position_photo_available) == len(tab_position_vertical_available) == 1:
        print("only one vertical left, we stop")
        break
    
    if len(tab_position_photo_available) % 1000 == 0:
        print("len(tab_position_photo_available) = ", len(tab_position_photo_available) )
        print("duration = " , time.time() - start_time)
        start_time = time.time()
    left = False
#    position_max_current_score = tab_position_photo_available[0]
#    current_score_left = compute_score_transition(all_tags[position_photo_left], all_tags[position_max_current_score])
#    current_score_right = compute_score_transition(all_tags[position_photo_right], all_tags[position_max_current_score])
#    if current_score_right > current_score_left:
#        left = True
#
#    max_current_score = max(current_score_left, current_score_right)
    find_any_heuristic = False
    max_current_score = -1000
    position_max_current_score = -1
    
    if type(position_photo_left) == tuple: # pair of vertical
        tags_photo_left = compute_tag_pair_vertical(all_tags_sorted[position_photo_left[0]], all_tags_sorted[position_photo_left[1]])
    else:
        tags_photo_left = all_tags_sorted[position_photo_left]
    
    if type(position_photo_right) == tuple: # pair of vertical
        tags_photo_right = compute_tag_pair_vertical(all_tags_sorted[position_photo_right[0]], all_tags_sorted[position_photo_right[1]])
    else:
        tags_photo_right = all_tags_sorted[position_photo_right]
    
    for position_photo_still_available in tab_position_photo_available:
#        print("int(len(all_tags[position_photo_right])/2) = ", int(len(all_tags[position_photo_right])/2))
        current_is_vert = all_is_vert_sorted[position_photo_still_available]
        if current_is_vert:
            current_stop_criteria = min(current_heurisitc_score_bien, len(all_tags_sorted[position_photo_still_available]) * (1 - 2 * FACTOR_LOSS_TAG_IN_PAIR)) # Like we sorted by artificially multiplying tag length of vert by 2, we don't divide by 2 in the stopping criteria...
        else:
            current_stop_criteria = min(current_heurisitc_score_bien, (len(all_tags_sorted[position_photo_still_available]) * (0.5 - FACTOR_LOSS_TAG_IN_PAIR)))
            
        if current_stop_criteria < max_current_score:
            find_any_heuristic = True
            if max_current_score >= current_heurisitc_score_bien:
                current_heurisitc_score_bien = min(MAX_HEURISTIC,current_heurisitc_score_bien+1)
                print("we found one, let's augment the heuristic", current_heurisitc_score_bien)
            break

        loss_current_image_tag = FACTOR_LOSS_TAG_IN_PAIR * len(all_tags_sorted[position_photo_still_available])
        current_score_left = compute_score_transition(tags_photo_left, all_tags_sorted[position_photo_still_available]) - loss_current_image_tag
        current_score_right = compute_score_transition(tags_photo_right, all_tags_sorted[position_photo_still_available]) - loss_current_image_tag
        
        if current_is_vert:
            current_score_left = 2*current_score_left
            current_score_right = 2*current_score_right
        
        if current_score_right >= max_current_score and current_score_right >= current_score_left:
            position_max_current_score = position_photo_still_available
            max_current_score = current_score_right
            left = False

        elif current_score_left >= max_current_score and current_score_left >= current_score_right:
            position_max_current_score = position_photo_still_available
            max_current_score = current_score_left
            left = True

    chosen_photo_is_vert = all_is_vert_sorted[position_max_current_score]
    
    if chosen_photo_is_vert: # We have now to look all remaining vert to form the best pair (we don't look right left anymore, cause it's already chosen)
        max_current_score_vert = -1000
        position_max_current_score_vert = -1
        
        tab_position_vertical_available.remove(position_max_current_score)
        for position_vert_still_available in tab_position_vertical_available:

            current_stop_criteria = min(current_heurisitc_score_bien, (len(all_tags_sorted[position_max_current_score]) + len(all_tags_sorted[position_vert_still_available])) * (0.5 - FACTOR_LOSS_TAG_IN_PAIR))            
            if current_stop_criteria < max_current_score_vert:
                find_any_heuristic = True
                if max_current_score_vert >= current_heurisitc_score_bien:
                    current_heurisitc_score_bien = min(MAX_HEURISTIC,current_heurisitc_score_bien+1)
                    print("we found one, let's augment the heuristic", current_heurisitc_score_bien)
                break
            
            tag_current_pair= compute_tag_pair_vertical(all_tags_sorted[position_vert_still_available], all_tags_sorted[position_max_current_score])
            loss_tag_in_current_pair = (len(all_tags_sorted[position_vert_still_available]) + len(all_tags_sorted[position_max_current_score]))
            # IDEA we still want to say lost tag is even worse than having one more tag lenght!!!
#            loss_tag_in_current_pair = 2*(len(all_tags_sorted[position_vert_still_available]) + len(all_tags_sorted[position_max_current_score])) - len(tag_current_pair)
#            print(max_current_score_vert)
            if left:
                current_score_vert = compute_score_transition(tags_photo_left, tag_current_pair) - loss_tag_in_current_pair * FACTOR_LOSS_TAG_IN_PAIR
            else:
                current_score_vert = compute_score_transition(tags_photo_right, tag_current_pair) - loss_tag_in_current_pair * FACTOR_LOSS_TAG_IN_PAIR
                
            if current_score_vert >= max_current_score_vert:
                max_current_score_vert = current_score_vert
                position_max_current_score_vert = position_vert_still_available

    if not find_any_heuristic:
        if current_heurisitc_score_bien > MIN_HEURISTIC:
            current_heurisitc_score_bien = max(MIN_HEURISTIC,current_heurisitc_score_bien-1)
            print("we didn't found one, let's diminue the heuristic", current_heurisitc_score_bien)

    if left:
        if chosen_photo_is_vert:
            solution_final.insert(0,(position_max_current_score, position_max_current_score_vert))
            position_photo_left = (position_max_current_score, position_max_current_score_vert)
        else:
            solution_final.insert(0,position_max_current_score)
            position_photo_left = position_max_current_score

    else:
        if chosen_photo_is_vert:
            solution_final.append((position_max_current_score, position_max_current_score_vert))
            position_photo_right = (position_max_current_score, position_max_current_score_vert)
        else:
            solution_final.append(position_max_current_score)
            position_photo_right = position_max_current_score

    if chosen_photo_is_vert:
        loss_tag_in_pair = len(set(all_tags_sorted[position_max_current_score]).intersection(all_tags_sorted[position_max_current_score_vert]))
        if loss_tag_in_pair > 0:
            print("WE LOST SOME TAG AT THIS STEP, LOSS IS ", loss_tag_in_pair)
        tab_position_photo_available.remove(position_max_current_score)
        tab_position_photo_available.remove(position_max_current_score_vert)
        tab_position_vertical_available.remove(position_max_current_score_vert)
    else:
        tab_position_photo_available.remove(position_max_current_score)

#print("solution_final = ", solution_final)

vrai_solution_final = []
for int_or_tuple in solution_final:
    if type(int_or_tuple) == tuple:
        vrai_solution_final.append(str(all_ids_sorted[int_or_tuple[0]]) + " " + str(all_ids_sorted[int_or_tuple[1]]))
    elif type(int_or_tuple) == int:
        vrai_solution_final.append(str(all_ids_sorted[int_or_tuple]))
    else:
        print("THAT S NOT NORMAL")
        raise

#print("vrai_solution_final = ", vrai_solution_final)

print("name_file_input = ", name_file_input)
print("(len(all_tags_sorted) = ", len(all_tags_sorted))
print("final current_heurisitc_score_bien= ", current_heurisitc_score_bien)
print("FACTOR_LOSS_TAG_IN_PAIR = ", FACTOR_LOSS_TAG_IN_PAIR)

if use_sorted:
    write_output(vrai_solution_final , "./data/"+name_file_input+"last_perfect_solution"+str(FACTOR_LOSS_TAG_IN_PAIR)+".out")
else:
    write_output(vrai_solution_final , "./data/"+name_file_input+"last_perfect_solution"+str(FACTOR_LOSS_TAG_IN_PAIR)+".out")
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


import numpy as np
import os
import sys
from input_func import input_func
import time

from compute_score import compute_score

list_name_input = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]

name_file_input = list_name_input[4]
heurisitc_score_bien = 9

file_path = "/home/toromanoff/workspace/hashcode_1/data/input/"+name_file_input+".txt"

horizontals_tags, horizontal_ids, verticals_tags, vertical_ids, dic, all_tags = input_func(file_path)

#print(horizontals_tags, horizontal_ids, verticals_tags, vertical_ids, dic, all_tags)

def write_output(result_list, filename):
    with open(filename, 'w') as file:
        file.write(str(len(result_list))+"\n")
        for line in result_list:
            file.write(str(line)+"\n")

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

# TO IMPROVE WE JUST PUT TOGETHER CONSECUTIVE VERTICAL
pair_horiz_ids, pair_horiz_tags = get_horiz_from_vert(vertical_ids, verticals_tags)

all_tags = horizontals_tags + pair_horiz_tags
all_ids = horizontal_ids + pair_horiz_ids

position_photo_available = [i for i in range(len(all_tags))]

assert len(all_tags) == len(all_ids)

first_photo_position = np.random.randint(0,len(all_tags))
position_photo_available.remove(first_photo_position)

position_photo_right = first_photo_position
position_photo_left = first_photo_position

solution_final = [first_photo_position]



print("name_file_input = ", name_file_input)
print("(len(all_tags) = ", len(all_tags))
print("heurisitc_score_bien= ", heurisitc_score_bien)

start_time = time.time()

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
    
    for position_photo_still_available in position_photo_available[1:]:
        
        if heurisitc_score_bien < max_current_score:
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
print("heurisitc_score_bien= ", heurisitc_score_bien)

write_output(vrai_solution_final , "/home/toromanoff/workspace/hashcode_1/data/"+name_file_input+str(heurisitc_score_bien)+".out")

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


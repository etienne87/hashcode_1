import numpy as np
import os
import sys
from input_func import input_func
from compute_score import compute_score_transition, compute_score
from tqdm import tqdm



ACCEPTABLE_LOSS = 0
def find_best_match_vert(curr_vert, list_available, list_verts):



    set_to_match = set(curr_vert[1])
    loss_min = -1
    best_vert = "bla"
    for idx in list_available:
        set_tmp = set(list_verts[idx][1])
        loss = len(set_to_match.intersection(set_tmp))
        if loss_min <0 or loss<loss_min:
            loss_min = loss
            best_vert = idx
            if loss <= ACCEPTABLE_LOSS:
                return best_vert

    return best_vert



def get_horiz_from_vert(list_vert):

    array_available_verts = np.ones(len(list_vert))


    list_horiz_bonus = []
    count = len(list_vert)
    for i in tqdm(range(len(list_vert)//2)):

        list_available = np.where(array_available_verts==1)[0]
        next_vert = list_vert[list_available[0]]
        array_available_verts[list_available[0]]=0
        other_next_id = find_best_match_vert(next_vert, list_available[1:], list_vert)
        other_next = list_vert[other_next_id]
        array_available_verts[other_next_id]=0
        list_horiz_bonus += [(str(next_vert[0])+" "+str(other_next[0]), list(set(next_vert[1]+other_next[1])))]


    return list_horiz_bonus


def get_first_frame(list_all):
    idx = np.random.randint(0, len(list_all))

    return idx

def add_image_to_slide(idx, result_list, array_availability, list_all):

    result_list += [str(list_all[idx][0])]
    array_availability[idx] = 0
    return 0


MIN_SCORE = 100
REAL_MIN = 1

def find_next_image(last_image, list_all, array_availability):
    global MIN_SCORE

    list_available = np.where(array_availability==1)[0]
    max_score = 0
    best_id = "bla"
    for idx in list_available:

        tag_length = len(last_image[1])
        tag_length_2 = len(list_all[idx][1])
        if tag_length < 3:
            break
        score = compute_score_transition(last_image[1], list_all[idx][1])
        if score >= min([MIN_SCORE, tag_length//2,tag_length_2]):
            return idx
        if score >max_score:
            max_score=score
            best_id=idx


    if max_score>0:
        if not MIN_SCORE==REAL_MIN:
            print("MIN SCORE")
            MIN_SCORE = max(MIN_SCORE-1,REAL_MIN)
        return best_id

    idx = list_available[np.random.randint(len(list_available))]
    print("chosing random image")
    return idx



def write_output(result_list, filename):


    with open(filename, 'w') as file:
        file.write(str(len(result_list))+"\n")
        for line in result_list:
            file.write(line+"\n")



def formatting_input(list_imag,list_id):
    out_tuples = []
    for i in range(len(list_imag)):
        out_tuples += [(list_id[i], list_imag[i])]

    return out_tuples


def main():



    # file_name = "c_memorable_moments"
    file_name = "b_lovely_landscapes"
    #file_name = "d_pet_pictures"
    #file_name = "e_shiny_selfies"

    print("processing file", file_name)
    print("MIN_SCORE_IS", MIN_SCORE)
    print("ACCEPTABLE LOSS IS", ACCEPTABLE_LOSS)

    file_path = "data/"+file_name+".txt"


    horizontals, horizontal_ids, verticals, vertical_ids, dic, all_tags = input_func(file_path)


    print("number of horizontals :", len(horizontals))
    print("number of verticals :", len(verticals))



    lh = list(zip(horizontal_ids, horizontals))
    vh = list(zip(vertical_ids, verticals))
    lh = lh + get_horiz_from_vert(vh)
    #sort by num tags
    cat = [(len(tags), (id, tags) ) for id, tags in lh]
    z = sorted(cat,key=lambda x:x[0])[::-1]
    list_all = [item[1] for item in z]


    result_list = []
    array_availability = np.ones(len(list_all))


    id_first = get_first_frame(list_all)



    add_image_to_slide(id_first, result_list, array_availability, list_all)
    last_image = list_all[id_first]


    for i in tqdm(range(len(list_all)-1)):
        idx_next = find_next_image(last_image, list_all, array_availability)
        add_image_to_slide(idx_next, result_list, array_availability, list_all)
        last_image = list_all[idx_next]

        if i%1000==0:
            out_path_debug = "debug/raphael2_"+file_name+"_debug_{}.out".format(i)
            write_output(result_list, out_path_debug)
            print(compute_score(file_path, out_path_debug))


        #print("one_more_image")
        #print(result_list)

    out_path = "raphael2_"+file_name+".out"
    write_output(result_list, out_path)


    print("result for file =",file_path)
    print(compute_score(file_path, out_path))





if __name__=="__main__":
    main()






















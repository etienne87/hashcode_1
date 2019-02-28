import numpy as np
import os
import sys
from input_func import input_func
from compute_score import compute_score_transition




def get_horiz_from_vert(list_vert):

    half_length = len(list_vert)//2
    list_horiz_bonus = []
    for i in range(half_length):
        list_horiz_bonus += [(str(list_vert[2*i][0])+" "+str(list_vert[2*i+1][0]), list(set(list_vert[2*i][1]+list_vert[2*i+1][1])))]
    return list_horiz_bonus


def get_first_frame(list_all):
    idx = np.random.randint(0, len(list_all))

    return idx

def add_image_to_slide(idx, result_list, array_availability, list_all):

    result_list += [str(list_all[idx][0])]
    array_availability[idx] = 0
    return 0




def find_next_image(last_image, list_all, array_availability):

    MIN_SCORE = 1

    list_available = np.where(array_availability==1)[0]
    for idx in list_available:
        score = compute_score_transition(last_image[1], list_all[idx][1])

        if score >= MIN_SCORE:
            return idx

    idx = list_available[np.random.randint(len(list_available))]

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

    file_path = "data/a_example.txt"

    horizontals, horizontal_ids, verticals, vertical_ids, dic, all_tags = input_func(file_path)



    list_horiz = formatting_input(horizontals, horizontal_ids)
    list_vert = formatting_input(verticals, vertical_ids)


    print("debug",list_horiz)

    list_horiz_bonus = get_horiz_from_vert(list_vert)


    result_list = []

    list_all = list_horiz+list_horiz_bonus
    array_availability = np.ones(len(list_all))


    id_first = get_first_frame(list_all)



    add_image_to_slide(id_first, result_list, array_availability, list_all)
    last_image = list_all[id_first]


    for i in range(min(len(list_all)-1,100)):
        idx_next = find_next_image(last_image, list_all, array_availability)
        add_image_to_slide(idx_next, result_list, array_availability, list_all)
        last_image = list_all[idx_next]

        print("one_more_image")
        print(result_list)

    write_output(result_list, "raphael_test.out")






if __name__=="__main__":
    main()






















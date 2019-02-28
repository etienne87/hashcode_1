import numpy as np
import os
import sys
from input_func import input_func





def get_horiz_from_vert(list_vert):

    half_length = len(list_vert)/2
    list_horiz_bonus = []
    for i in half_length:
        list_horiz_bonus += (str(list_vert[2*i][0])+", "+str(list_vert[2*i+1]), list(set(list_vert[2*i][1]+list_vert[2*i+1][1])))
    return list_horiz_bonus


def get_first_frame(list_all):
    idx = np.random.randint(0, len(list_all))

    return idx

def add_image_to_slide(idx, result_list, array_availability, list_all):

    result_list += [list_all[id_first][0]]
    array_availability[idx] = 0
    return 0




def find_next_image(last_image, list_all, array_availability):




def main(list_horiz, list_vert):

    list_horiz_bonus = get_horiz_from_vert(list_vert)


    result_list = []

    list_all = list_horiz+list_horiz_bonus
    array_availability = np.ones(len(list_all))


    id_first = get_first_frame(list_all)

    add_image_to_slide(id_first, result_list, array_availability, list_all)

    last_image = list_all[id_first]


































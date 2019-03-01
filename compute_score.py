#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 21:23:19 2019

@author: toromanoff
"""

import numpy as np
import os
import sys
from input_func import input_func
import time
def read_submission(path, all_tags):
    slideshow = []
    with open(path, 'r') as f:
        lines = f.readlines()
        Nslides = int(lines[0])
        for i, line in enumerate(lines[1:]):
            words = line.split()

            tags = []
            for word in words:
                photo_id = int(word)
                tags += all_tags[photo_id]

            slideshow.append(tags)

    return slideshow


def compute_score_transition(s1, s2):
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
    s_in_s1_not_in_s2 = len(s1)-s_intersection
    s_in_s2_not_in_s1 = len(s2)-s_intersection

    score = min([s_intersection, s_in_s1_not_in_s2, s_in_s2_not_in_s1])
    return score


def compute_score(input_path, submit_path):
    horiz, horiz_ids, vert, vert_ids, dic, all_tags = input_func(input_path)
    slideshow = read_submission(submit_path, all_tags)
    score = 0
    for i in range(len(slideshow)-1):
        score += compute_score_transition(slideshow[i], slideshow[i+1])
    return score




def photo_ids_to_tags(photo_ids, all_tags):
    slideshow = []
    for photo_id in photo_ids:
        tags = []
        for id in photo_id:
            tags += all_tags[photo_id]
        slideshow.append(tags)
    return slideshow


def compute_score_submit_ids(input_path, photo_ids):
    horiz, horiz_ids, vert, vert_ids, dic, all_tags = input_func(input_path)
    slideshow = photo_ids_to_tags(photo_ids, all_tags)
    score = 0
    for i in range(len(slideshow) - 1):
        score += compute_score_transition(slideshow[i], slideshow[i + 1])
    return score


if __name__ == '__main__':
    inpath = 'data/a_example.txt'
    outpath = 'submit_bidon.txt'
    score = compute_score(inpath, outpath)
    print(score)




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

def read_submission(path):
    slideshow = []
    with open(path, 'r') as f:
        lines = f.readlines()
        Nslides = int(lines[0])
        for i, line in enumerate(lines[1:]):
            words = line.split()

            tags = []
            for word in words:
                tags.append(int(word))

            slideshow.append(tags)

    return slideshow


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
    print(f"S1 {s1}")
    print(f"S2 {s1}")
    s_intersection = len(s1.intersection(s2))
    s_in_s1_not_in_s2 = len([tag for tag in s1 if tag not in s2])
    s_in_s2_not_in_s1 = len([tag for tag in s2 if tag not in s1])

    score = min([s_intersection,s_in_s1_not_in_s2, s_in_s2_not_in_s1])
    print(f"Score is {score}")
    return score


def compute_score(path):
    slideshow = read_submission(path)
    print(slideshow)

    score = 0

    for i in range(len(slideshow)-1):
        score += compute_score_transition(slideshow[i], slideshow[i+1])

    return score
    

if __name__ == '__main__':
    path = 'submit_bidon.txt'
    score = compute_score(path)
    print(score)




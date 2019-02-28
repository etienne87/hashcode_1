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

def compute_score_transition(tags1, tasg2):
    return 0


def compute_score(path):
    slideshow = read_submission(path)

    score = 0

    for i in range(len(slideshow)-1):
        score += compute_score_transition(slideshow[i], slideshow[i+1])

    return score
    

if __name__ == '__main__':
    path = 'submit_bidon.txt'

    submission = read_submission(path)




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 06:57:38 2019

@author: toromanoff
"""

import time
import numpy as np

def fonction_numpy(nb_iteration, tab_principale):
    np_indice = np.ones(len(tab_principale))
    for itereration in range(nb_iteration):
        np_indice[itereration] = 0
        tab_principale_where = [tab_principale[i] for i in np.where(np_indice)[0]]
        for obj_principale in tab_principale_where:
#            print("obj_principale = ", obj_principale)
            do_nothing = 1

    assert len(tab_principale_where) == nb_iteration - itereration - 1
    
def fonction_list(nb_iteration, tab_principale):    
    list_indice = [i for i in range(len(tab_principale))]
    for itereration in range(nb_iteration):
        list_indice.remove(itereration)
    
        for indice_obj_principale in list_indice:
            obj_principale = tab_principale[indice_obj_principale]
#            print("obj_principale = ", obj_principale)
            do_nothing = 1
        
    assert len(list_indice) == nb_iteration - itereration - 1
    
nb_iteration = 10000

tab_principale = [i**1.05 for i in range(nb_iteration)]

start_time_1 = time.time()

fonction_numpy(nb_iteration, tab_principale)
      
duration1 = time.time() - start_time_1

print("starting list remove")

start_time_2 = time.time()

fonction_list(nb_iteration, tab_principale)

duration2 = time.time() - start_time_2

print("duration 1 = ", duration1)
print("duration 2 = ", duration2)
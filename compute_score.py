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

#matrice_cache_video # Output nb cache * nb video True if video is in cache False if not

#    file_path = "/home/toromanoff/workspace/hashcode_1/streaming/trending_today.in"

def compute_score(file_path):
    #print("IN COMPUTE SCORE, matrice_cache_video = ", matrice_cache_video)
    video_size, cache_size, gain_per_ep_per_cach, nb_request_per_ep_per_video = input_func(file_path)
    
    matrice_endpoint_request = nb_request_per_ep_per_video # Dim endpoint * video inside nb_request
    matrice_size_video = video_size # Dim video * 1 inside  size video
    cache_size = cache_size # Initial capacity of cache
    matrice_gain = gain_per_ep_per_cach # endpoint * cache inside gain to take this cache from this endpoint
    
    #matrice_cache_video # Output nb cache * nb video True if video is in cache False if not

    nb_endpoint = matrice_endpoint_request.shape[0]
    nb_video = matrice_endpoint_request.shape[1]
    assert nb_video == matrice_size_video.shape[0]
    nb_cache = matrice_gain.shape[1]
    
    # Tab of size endpoint and for each endpoint id create a list containing all 
    #cache connected and the gain
    tab_endpoint_cache = [[] for i in range(nb_endpoint)] 
    
    for id_endpoint in range(nb_endpoint):
        for id_cache in range(nb_cache):
            current_gain = matrice_gain[id_endpoint, id_cache]
            if current_gain > 0:
                tab_endpoint_cache[id_endpoint].append((current_gain, id_cache))
    
    # First check if cache are not full
    for cache_id in range(nb_cache):
        current_capacity = cache_size
        for video_id in range(nb_video):
            if matrice_cache_video[cache_id, video_id] == 1:
                current_capacity -= matrice_size_video[video_id]
                if current_capacity < 0:
                    print("YOU TRY TO CHEAT!!!!!")
                    return -1000000000
    
    nb_endpoint = matrice_endpoint_request.shape[0]
    nb_video = matrice_endpoint_request.shape[1]
    assert nb_video == matrice_size_video.shape[0]
    nb_cache = matrice_gain.shape[1]
    
    score_final = 0
    
    for id_endpoint in range(nb_endpoint):
        for video_id in range(nb_video):
            gain_max = 0
            for (gain_latence_cache, id_cache) in tab_endpoint_cache[id_endpoint]:

                if matrice_cache_video[id_cache, video_id] == 1:
                    if gain_latence_cache * matrice_endpoint_request[id_endpoint, video_id] > gain_max:
                        gain_max = gain_latence_cache * matrice_endpoint_request[id_endpoint, video_id]

            score_final += gain_max

    score_final = score_final/np.sum(matrice_endpoint_request)
    print("score final is ", score_final)
    return score_final
    
    
    
            
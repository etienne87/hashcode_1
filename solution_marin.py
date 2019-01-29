import numpy as np
import os
import sys
from input_func import input_func

from compute_score import compute_score


file_path = "/home/toromanoff/workspace/hashcode_1/streaming/simple_example.in"


video_size, cache_size, gain_per_ep_per_cach, nb_request_per_ep_per_video = input_func(file_path)

matrice_endpoint_request = nb_request_per_ep_per_video # Dim endpoint * video inside nb_request
matrice_size_video = video_size # Dim video * 1 inside  size video
cache_size = cache_size # Initial capacity of cache
matrice_gain = gain_per_ep_per_cach # endpoint * cache inside gain to take this cache from this endpoint

print("matrice_endpoint_request = ", matrice_endpoint_request)
print("matrice_size_video = ", matrice_size_video)
print("cache_size = ", cache_size)
print("matrice_gain = ", matrice_gain)

#matrice_cache_video # Output nb cache * nb video True if video is in cache False if not

nb_endpoint = matrice_endpoint_request.shape[0]
nb_video = matrice_endpoint_request.shape[1]
assert nb_video == matrice_size_video.shape[0]
nb_cache = matrice_gain.shape[1]

print("nb_endpoint = ", nb_endpoint)
print("nb_video = ", nb_video)
print("nb_cache = ", nb_cache)

# Tab of size endpoint and for each endpoint id create a list containing all 
#cache connected and the gain
tab_endpoint_cache = [[] for i in range(nb_endpoint)] 

# Tab of size cache and for each cache id create a list containing all 
#video that we put on this cache
tab_cache_video = [[] for i in range(nb_cache)]

tab_capacity_cache = np.ones(nb_cache) * cache_size

for id_endpoint in range(nb_endpoint):
    for id_cache in range(nb_cache):
        current_gain = matrice_gain[id_endpoint, id_cache]
        if current_gain > 0:
            tab_endpoint_cache[id_endpoint].append((current_gain, id_cache))

print("tab_endpoint_cache = ", tab_endpoint_cache)
         
# We want to sort all cache by gain, the first will be the one with bigger gain
for id_endpoint in range(nb_endpoint):
    not_sorted_gain_for_current_endpoint = tab_endpoint_cache[id_endpoint]
    sorted_gain_for_current_endpoint = sorted(not_sorted_gain_for_current_endpoint, key=lambda tup: tup[0], reverse = True)
    tab_endpoint_cache[id_endpoint] = sorted_gain_for_current_endpoint

print("tab_endpoint_cache = ", tab_endpoint_cache)

for id_endpoint in range(nb_endpoint):
    while np.max(matrice_endpoint_request[id_endpoint]) > 0:
        video_id = np.argmax(matrice_endpoint_request[id_endpoint])
        
        video_already_available = False
        
        for (current_gain, id_cache) in tab_endpoint_cache[id_endpoint]:
            if video_id in tab_cache_video[id_cache]:
                #The video is in a cache we stop
                video_already_available = True
                break
            
        if video_already_available:
            matrice_endpoint_request[id_endpoint, video_id] = 0    
        else:
        #The gain are sorted in the tab_endpoint_cache tab
           for (current_gain, id_cache) in tab_endpoint_cache[id_endpoint]:
               if tab_capacity_cache[id_cache] > matrice_size_video[video_id]:
                   tab_cache_video[id_cache].append(video_id)
                   tab_capacity_cache[id_cache] -= matrice_size_video[video_id]
                   break
           matrice_endpoint_request[id_endpoint, video_id] = 0
       
print("tab_cache_video = " ,tab_cache_video)    

matrice_cache_video = np.zeros((nb_cache, nb_video))
for id_cache in range(nb_cache):
    for id_video in tab_cache_video[id_cache]:
        matrice_cache_video[id_cache, id_video] = 1
        
print(" matrice_cache_video = " , matrice_cache_video)   

score_solution_marin = compute_score(file_path, matrice_cache_video)

test_output_simple_exemple = np.zeros((nb_cache, nb_video))
test_output_simple_exemple[0,2] = 1
test_output_simple_exemple[1,1] = 1
test_output_simple_exemple[1,3] = 1
test_output_simple_exemple[2,0] = 1
test_output_simple_exemple[2,1] = 1

score_output_simple_exemple = compute_score(file_path, test_output_simple_exemple)

print(" score_solution_marin = " , score_solution_marin)
print(" score_output_simple_exemple = " , score_output_simple_exemple) 
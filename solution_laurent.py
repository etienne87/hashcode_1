"""
virer tous les endpoints qui ne sont pas connected a un cache
virer toutes les videos qui ne sont jamais demande


sorted des caches par taille restante  -> avoir une structure type heap

on maintient pour chaque cache une liste de video avec score: liste videos + score

while qu'un cache a de la place:
    pour le cache qui a le plus de place:
    quelle est la video qui rapporte le plus sur ce cache, qui n'y est pas encore, qui fait moins que la taille available, remplir le cache avec cette video
    on efface de la liste de tous cache la video qui vient d'etre alloue (pas optimale, mais evite d'avoir la meme video partout)



"""

import numpy as np
import time
from numba.decorators import jit
from input_func import input_func

import os
import sys


file_path = "./streaming/me_at_the_zoo.in"

video_size, cache, gain_latence, ep_video_requests = input_func(file_path)
n_cache = gain_latence.shape[1]
cache_size = np.ones(n_cache) * cache
#ep_video_requests = np.random.random([n_ep, n_video]).astype(np.int)
#gain_latence = np.random.random([n_ep, n_cache]).astype(np.int)
#cache = np.zeros([n_cache])
#output = np.zeros([n_cache, n_video], dtype=np.bool)

def get_best_video(cache_idx):
    pass


gain_score = gain_latence.T.dot(ep_video_requests)  # shape =  VxC
# init:
for video_idx in range(video_size.shape[0]):
    # removing videos that don't fit
    for cache_idx in range(cache_size.shape[0]):
        if cache_size[cache_idx] - video_size[video_idx] < 0:
            print(f"UPDATING CACHE {cache_idx} for video {video_idx}, cache_size is {cache_size[cache_idx]} whereas video size is video_size[video_idx")
            gain_score[cache_idx, video_idx] = 0

#def update_gain(video_idx, cache_idx):
#    for video in range(video_size.shape):


print("gain_score shape is {}".format(gain_score))
print(gain_score)

exit(0)
#n_cache



for cache_idx in range(n_cache):
    start = time.time()
    best_video_idx = get_best_video(cache_idx)
    duration = time.time() - start
    #print(f"Duration is {duration}")
    #print(best_video_idx)





print("DONE")




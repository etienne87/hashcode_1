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

example_case = {}
n_ep = 1000
n_video = 10000
n_cache = 1000


ep_video_requests = np.random.random([n_ep, n_video]).astype(np.int)
gain_latence = np.random.random([n_ep, n_cache]).astype(np.int)
cache = np.zeros([n_cache])
output = np.zeros([n_cache, n_video], dtype=np.bool)

def get_best_video(cache_idx):
    """
    best video for this cache
    :param cache_idx:
    :return:
    """
    #best_video = -1
    #best_gain = 0
    #for video_idx in range(ep_video_requests.shape[1]):
    #    video_gain = 0
    #    for ep_idx in range(gain_latence.shape[0]):
    #        #print(f"ep is {ep_idx}")
    #        cur_gain = gain_latence[ep_idx, cache_idx] * ep_video_requests[ep_idx, video_idx]
    #        video_gain += cur_gain
    #    #dot_res = np.dot(ep_video_requests[:, video_idx], gain_latence[:, cache_idx])
    #    #print(f"dot_res is {dot_res}, video_gain {video_gain}")
    #    best_gain, best_video = np.max([best_gain, best_video], [video_gain, video_idx])
    #return best_video

    np.argmin()



gain_score = gain_latence.T.dot(ep_video_requests)
print("gain_score shape is {}".format(gain_score))



for cache_idx in range(n_cache):
    start = time.time()
    best_video_idx = get_best_video(cache_idx)
    duration = time.time() - start
    #print(f"Duration is {duration}")
    #print(best_video_idx)





print("DONE")




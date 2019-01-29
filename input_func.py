import numpy as np


def input_func(file_path):
    file = open(file_path, 'r')

    nb_V, nb_E, nb_R, nb_C, X = [int(x) for x in file.readline().split(" ")]

    cache_size = X

    video_size = np.array([int(x) for x in file.readline().split(" ")])

    gain_per_ep_per_cach = np.zeros((nb_E, nb_C))
    
    for i in range(nb_E):
        latency_to_server, K = [int(x) for x in file.readline().split(" ")]

        for j in range(K):
            id_cache, latency_to_cache = [int(x) for x in file.readline().split(" ")]
            gain_per_ep_per_cach[i][id_cache] = max(0, latency_to_server - latency_to_cache)

    nb_request_per_ep_per_video = np.zeros((nb_E, nb_V))

    for i in range(nb_R):
        id_vid, id_ep, nb_request_tmp = [int(x) for x in file.readline().split(" ")]

        nb_request_per_ep_per_video[id_ep][id_vid] += nb_request_tmp

    return video_size, cache_size, gain_per_ep_per_cach, nb_request_per_ep_per_video
























import input_func as funky
import time
import numpy as np


def compute_gains(latency, requests):
    """
    will compute the points you would gain for each cache to put a video in it by summing all requests times the latency / cache

    :return:
    """
    return latency.dot(requests)


def update_gain(gains, v, c, connexion_cache_to_endpoint):
    """
    put video v into cache c: update all caches gain / video
    :param gains:
    :param video_num:
    :param cache_num:
    :return:
    """
    pass


def optimize_gain(gains, memory, latency, requests):
    """
    optimize gain for each cache independently
    :return:
    """
    pass


def get_connexions(latency):
    """

    :return: list of C elements  of list of variable number of endpoints indices
    """
    list = []
    for c in range(latency.shape[1]):
        connexions = []
        for e in range(latency.shape[0]):
            if latency[e, c] > 0:
                connexions += [e] # index of endpoint
        list += [connexions]
    return list


if __name__ == '__main__':
    file_path = ""

    #data = input_func.file_parse(file_path)

    file_path = "./streaming/me_at_the_zoo.in"

    video_size, cache_size, latency, requests = funky.input_func(file_path)

    E, V = requests.shape
    E, C = latency.shape

    connex = get_connexions(latency)

    print(connex)

    memory = np.full((C,), cache_size)

    print('videos: ', V, ' endpoints: ', E, ' caches: ', C)
    print('latency shape: ', latency.shape)
    print('requests.shape: ', requests.shape)

    # Summarize data here
    # V = 10000 # number of video
    # E = 1000 # number of endpoints
    # C = 1000 # number of cache servers
    # requests = np.zeros((E, V), dtype=np.int32) # number of request for each video / E
    # memory = np.zeros((C,), dtype=np.int32) # memory / cache server
    # latency = np.zeros((C, E), dtype=np.int32) # gain of latency for each cache / endpoint

    start = time.time()
    gains = compute_gains(latency.T, requests)
    runtime = time.time()-start

    print(runtime)
    print(gains.shape)

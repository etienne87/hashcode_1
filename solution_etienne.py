import time
import numpy as np
import input_func as funky
import compute_score


def compute_gains(latency, requests):
    """
    will compute the points you would gain for each cache to put a video in it by summing all requests times the latency / cache

    :return:
    """
    return latency.dot(requests)



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


def update_gain(gains, v, c, connexion_cache_to_endpoint):
    """
    put video v into cache c: update all caches gain / video
    :param gains:
    :param video_num:
    :param cache_num:
    :return:
    """
    pass


def knapsack_one_cache(vals, capacity, sizes, mask, n=None):
    """

    :param val: value/ video for this cache
    :param capacity:
    :param video_sizes:
    :param n: iteration number, starts at len(video_sizes)
    :return:
    """
    if n is None:
        n = len(sizes)

    if n == 0 or capacity == 0:
        return 0

    #cannot include current video
    if (sizes[n - 1] > capacity):
        mask += [0]
        return knapsack_one_cache(vals, capacity, sizes, mask, n-1)

    #return max between taking & not taking
    else:
        #case 1 : we take the video
        val1 = vals[n - 1] + knapsack_one_cache(vals, capacity - sizes[n - 1], sizes, n - 1)

        #backtrack
        mask = mask[:-2]

        #case 2: we do not take the video
        val2 = knapsack_one_cache(vals, capacity, sizes, n-1)

        if val1 > val2:
            mask += [ (val1 > val2) ]

        return max(val1, val2)


def knapSack(W, wt, val, n):
    K = [[0 for x in range(W + 1)] for x in range(n + 1)]

    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    return K[n][W]



if __name__ == '__main__':
    file_path = ""

    #data = input_func.file_parse(file_path)

    file_path = "./streaming/me_at_the_zoo.in"

    video_size, cache_size, latency, requests = funky.input_func(file_path)

    E, V = requests.shape
    E, C = latency.shape

    #connex = get_connexions(latency)

    good = np.zeros((C, V), dtype=np.int32)

    for i in range(C):
        knapSack((cache_size, 4))

    score = compute_score.compute_score(file_path, good)

    print("Score: ", score)

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
    #print(gains.shape)

#import input_func
import time
import numpy as np


def compute_gains(requests, latency):
    """
    will compute the points you would gain for each cache to put a video in it by summing all requests times the latency / cache

    :return:
    """
    return latency.dot(requests)



if __name__ == '__main__':
    file_path = ""

    #data = input_func.file_parse(file_path)

    #summarize data here
    V = 10000 # number of video
    E = 1000 # number of endpoints
    C = 1000 # number of cache servers

    requests = np.zeros((E, V), dtype=np.int32) # number of request for each video / E
    memory = np.zeros((C,), dtype=np.int32) # memory / cache server
    latency = np.zeros((C, E), dtype=np.int32) # gain of latency for each cache / endpoint

    start = time.time()
    gains = compute_gains(requests, latency)
    runtime = time.time()-start

    print(runtime)
    print(gains)

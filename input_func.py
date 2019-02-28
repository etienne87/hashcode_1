import numpy as np


def input_func(path):
    dic = {}
    horizontals = []
    horizontal_ids = []
    verticals = []
    vertical_ids = []
    total_tags = []
    cnt = 0

    with open(path, 'r') as f:
        lines = f.readlines()

        Nphoto = int(lines[0])
        for i, line in enumerate(lines[1:]):
            words = line.split()

            num_tags = int(words[1])

            tags = []

            for n in range(num_tags):
                word = words[2 + n]

                if word not in dic:
                    dic[word] = cnt
                    cnt += 1

                tags.append(dic[word])

            if words[0] == 'H':
                horizontal_ids.append(i)
                horizontals.append(tags)
            elif words[0] == 'V':
                vertical_ids.append(i)
                verticals.append(tags)

            total_tags.append(tags)

    # print(horizontals[1])
    # print(dic)

    return horizontals, horizontal_ids, verticals, vertical_ids, dic, total_tags



if __name__ == '__main__':
    file_path = "data/a_example.txt"

    horizontals, horizontal_ids, verticals, vertical_ids, dic, all_tags = input_func(file_path)


    #print(horizontals[0], dic)

    print(all_tags)






















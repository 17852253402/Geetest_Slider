import math
import random

pass_arr = [
               [[22, 29, 0], [10, 0, 10], [9, 0, 20], [9, 0, 18], [8, 0, 10], [8, 0, 10], [8, 0, 11], [7, 0, 19],
                [6, 0, 15], [6, 0, 14], [6, 0, 12], [5, 0, 13], [6, 0, 17], [4, 0, 17], [5, 0, 11], [4, 0, 13],
                [4, 0, 19],
                [4, 0, 13], [4, 0, 15], [3, 0, 11], [3, 0, 17], [3, 0, 12], [3, 0, 14], [3, 0, 18], [2, 0, 17],
                [2, 0, 12],
                [3, 0, 11], [2, 0, 13], [2, 0, 14], [1, 0, 11], [2, 0, 10], [2, 0, 16], [1, 0, 19], [2, 0, 15],
                [1, 0, 16],
                [1, 0, 20], [2, 0, 10], [1, 0, 11], [1, 0, 19], [1, 0, 17], [1, 0, 13], [1, 0, 10], [1, 0, 15],
                [1, 0, 12],
                [1, 0, 20], [1, 0, 12], [1, 0, 16], [1, 0, 18], [1, 0, 16], [1, 0, 15], [1, 0, 16], [1, 0, 19],
                [1, 0, 18],
                [1, 0, 16], [1, 0, 20], [1, 0, 20], [0, 0, 226]]], 170


# print(len(pass_arr[0][0]))


def get_customer_slide_data(distance):
    trace_data = [[random.randint(20, 60), random.randint(10, 40), 0]]
    count = 30 + int(distance / 2)
    x = random.randint(10, 15)
    add = -1
    is_back = True
    for i in range(count):
        if i == int(count / 2):
            add = i + 1
        if i == add and is_back:
            x += 2
            add = random.randint(i, i + 4)
            trace_data.append([x, 0, random.randint(10, 20)])
            is_back = False
            continue
        if x - 1 > 0:
            x -= random.choice([1, 1, 1, 0, 0, 0, 0, 0])
            trace_data.append([x, 0, random.randint(10, 20)])
        else:
            trace_data.append([1, 0, random.randint(10, 20)])
        is_back = True
    trace_data.append([0, 0, random.randint(100, 300)])
    return trace_data


def get_slide_data_v2(distance):
    trace_data = [[random.randint(20, 60), random.randint(10, 40), 0]]
    count = 30 + int(distance / 2)
    time = 0
    _x = 0
    for i in range(count):
        x = round(i / count * distance) + 1
        if _x == x:
            continue
        trace_data.append([x - _x, 0, time])
        _x = x
        time = random.randint(10, 20)
    trace_data.append([0, 0, random.randint(200, 300)])
    return trace_data


def get_num_add(n: int) -> list:
    x = []
    count = 30 + int(n / 2)

    for i in range(count):
        _x = round(i / count * n) + 1
        print(_x)
    return x


if __name__ == '__main__':
    print(get_num_add(125))
    # trace_data = get_slide_data_v2(124)
    # num = 0
    # for i in range(1, len(trace_data)):
    #     num += trace_data[i][0]
    # print(num)
    # print(trace_data)

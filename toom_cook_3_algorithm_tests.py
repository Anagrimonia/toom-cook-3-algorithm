from toom_cook_3_algorithm import ToomCook3
import random
import time

toom = ToomCook3(limit = 729)

def test_correctness_naive():
    for i in range(10):
        a = [random.randrange(10) for _ in range(10)]
        b = [random.randrange(10) for _ in range(10)]

        a_str = toom.to_string(a)
        b_str = toom.to_string(b)
        res_true = int(a_str) * int(b_str)
        res = int(toom.compute(a, b, naive = True))

        assert res == res_true, "{0} * {1} = {2}, but got {3}".format(a_str, b_str, res_true, res)
    print('[DONE] test_correctness_naive')

def test_correctness():
    for i in range(10):
        a = [random.randrange(10) for _ in range(100)]
        b = [random.randrange(10) for _ in range(100)]

        a_str = toom.to_string(a)
        b_str = toom.to_string(b)
        res_true = int(a_str) * int(b_str)
        res = int(toom.compute(a, b, naive = False))

        assert res == res_true, "{0} * {1} = {2}, but got {3}".format(a_str, b_str, res_true, res)
    print('[DONE] test_correctness')

def test_correctness_2():
    for i in range(10):
        a = [random.randrange(10) for _ in range(100)]
        b = [random.randrange(10) for _ in range(10)]

        a_str = toom.to_string(a)
        b_str = toom.to_string(b)
        res_true = int(a_str) * int(b_str)
        res = int(toom.compute(a, b, naive = False))

        assert res == res_true, "{0} * {1} = {2}, but got {3}".format(a_str, b_str, res_true, res)
    print('[DONE] test_correctness_2')

def test_correctness_3():
    for i in range(10):
        a = [random.randrange(10) for _ in range(10)]
        b = [random.randrange(10) for _ in range(100)]

        a_str = toom.to_string(a)
        b_str = toom.to_string(b)
        res_true = int(a_str) * int(b_str)
        res = int(toom.compute(a, b, naive = False))

        assert res == res_true, "{0} * {1} = {2}, but got {3}".format(a_str, b_str, res_true, res)
    print('[DONE] test_correctness_3')

def test_speed():
    for i in range(10):
        a = [random.randrange(10) for _ in range(729)]
        b = [random.randrange(10) for _ in range(729)]

        start_time = time.time()
        res_naive = toom.compute(a, b, naive = True)
        time_naive = time.time() - start_time

        start_time = time.time()
        res_toom  = toom.compute(a, b, naive = False)
        time_toom = time.time() - start_time

        # print('Toom: {0:.3f}, naive: {1:.3f}'.format(time_toom, time_naive))

        assert time_toom < time_naive, "Toom: {0}, naive: {1}".format(time_toom, time_naive)
    print('[DONE] test_speed')

def main():
    test_correctness_naive()
    test_correctness()
    test_correctness_2()
    test_correctness_3()
    test_speed()

if __name__ == '__main__':
    main()
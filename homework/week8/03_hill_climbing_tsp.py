# 爬山演算法（Hill Climbing）- 旅行推銷員問題（TSP）
import math, random, time

CITIES = [
    (0,0),(5,0),(10,0),(15,0),
    (0,5),(5,5),(10,5),(15,5),
    (0,10),(5,10),(10,10),(15,10),
    (2,7),(13,7),(7,12),(7,-2)
]
n = len(CITIES)

def dist(i,j):
    x1,y1 = CITIES[i]; x2,y2 = CITIES[j]
    return math.hypot(x1-x2, y1-y2)

def path_len(path):
    s = 0
    for i in range(len(path)):
        s += dist(path[i], path[(i+1)%len(path)])
    return s

def random_swap(path):
    p = path[:]
    if n < 2: return p
    i,j = random.sample(range(n), 2)
    p[i],p[j] = p[j],p[i]
    return p

def hill_climbing(max_iter=20000):
    path = list(range(n))
    random.shuffle(path)
    cur = path[:]
    cur_len = path_len(cur)
    for _ in range(max_iter):
        cand = random_swap(cur)
        c_len = path_len(cand)
        if c_len < cur_len:  # 僅接受更好（更短）的解
            cur, cur_len = cand[:], c_len
    return cur, cur_len

if __name__ == '__main__':
    random.seed(123)
    t0 = time.perf_counter()
    path, plen = hill_climbing(max_iter=25000)
    t1 = time.perf_counter()
    print('【爬山演算法（Hill Climbing）】')
    print('路徑:', path)
    print('總長度:', round(plen,4))
    print('執行時間:', round(t1-t0, 6), '秒')
    print('說明: 每步僅接受改善的鄰近解，無法接受更差解，易停在局部最佳。')

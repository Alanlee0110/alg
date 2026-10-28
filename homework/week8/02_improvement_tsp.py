# 改良法（局部改善法）- 旅行推銷員問題（TSP）
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

def greedy_tsp(start=0):
    unvisited = set(range(n))
    path = [start]
    unvisited.discard(start)
    cur = start
    while unvisited:
        nxt = min(unvisited, key=lambda x: dist(cur,x))
        path.append(nxt)
        unvisited.discard(nxt)
        cur = nxt
    return path

def improve_tsp(init=None, max_iter=15000):
    if init is None:
        path = list(range(n))
        random.shuffle(path)
    else:
        path = init[:]
    best = path[:]
    best_len = path_len(best)
    for _ in range(max_iter):
        cand = random_swap(best)
        l = path_len(cand)
        if l < best_len:
            best, best_len = cand[:], l
    return best

if __name__ == '__main__':
    random.seed(123)
    t0 = time.perf_counter()
    g = greedy_tsp(0)
    imp = improve_tsp(g, max_iter=20000)
    t1 = time.perf_counter()
    print('【改良法（從初始解做局部改善）】')
    print('初始解（貪婪）路徑:', g, '長度:', round(path_len(g),4))
    print('改良後路徑:', imp, '長度:', round(path_len(imp),4))
    print('改善幅度:', round(path_len(g)-path_len(imp),4))
    print('執行時間:', round(t1-t0, 6), '秒')
    print('說明: 從可行解出發，不斷嘗試鄰近解（隨機交換），只接受更短的解來改良。')

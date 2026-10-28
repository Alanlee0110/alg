# 模擬退火法（Simulated Annealing）- 旅行推銷員問題（TSP）
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

def simulated_annealing(T=1000.0, alpha=0.9995, max_iter=40000):
    path = list(range(n))
    random.shuffle(path)
    cur = path[:]
    cur_len = path_len(cur)
    best = cur[:]
    best_len = cur_len
    temp = T
    for _ in range(max_iter):
        cand = random_swap(cur)
        c_len = path_len(cand)
        delta = c_len - cur_len  # > 0 表示變差
        if delta < 0:
            # 改善：直接接受
            cur, cur_len = cand[:], c_len
        else:
            # 變差：以機率 exp(-delta/T) 接受
            if temp > 1e-12 and random.random() < math.exp(-delta / temp):
                cur, cur_len = cand[:], c_len
        if cur_len < best_len:
            best, best_len = cur[:], cur_len
        temp *= alpha
    return best, best_len

if __name__ == '__main__':
    random.seed(123)
    t0 = time.perf_counter()
    path, plen = simulated_annealing(T=800.0, alpha=0.9997, max_iter=60000)
    t1 = time.perf_counter()
    print('【模擬退火法（Simulated Annealing）】')
    print('路徑:', path)
    print('總長度:', round(plen,4))
    print('執行時間:', round(t1-t0, 6), '秒')
    print('說明: 高溫時容許接受較差解以跳出局部最佳，隨溫度下降逐漸收斂到較佳解。')

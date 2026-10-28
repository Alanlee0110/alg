# 梯度下降法（最陡下降法，離散近似）- 旅行推銷員問題（TSP）
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

def all_swaps(path):
    res = []
    p = path
    for i in range(n):
        for j in range(i+1,n):
            cand = p[:]
            cand[i],cand[j] = cand[j],cand[i]
            res.append(cand)
    return res

def gradient_descent_steepest(max_iter=500):
    path = list(range(n))
    random.shuffle(path)
    cur = path[:]
    cur_len = path_len(cur)
    for _ in range(max_iter):
        best_cand = None
        best_cand_len = cur_len
        # 評估所有鄰近解，選擇下降幅度最大的（最陡下降）
        for cand in all_swaps(cur):
            l = path_len(cand)
            if l < best_cand_len:
                best_cand_len = l
                best_cand = cand
        if best_cand is None:
            break  # 無法再改善，停在局部最佳
        cur, cur_len = best_cand[:], best_cand_len
    return cur, cur_len

if __name__ == '__main__':
    random.seed(123)
    t0 = time.perf_counter()
    path, plen = gradient_descent_steepest(max_iter=800)
    t1 = time.perf_counter()
    print('【梯度下降法（最陡下降法／離散近似）】')
    print('路徑:', path)
    print('總長度:', round(plen,4))
    print('執行時間:', round(t1-t0, 6), '秒')
    print('說明: 每步檢查所有交換鄰近解，選擇使路徑最短的那個（最陡下降），易卡在局部最佳。')
    print('備註: TSP為離散排列問題，並無真正的連續梯度，此處用最陡下降近似。')

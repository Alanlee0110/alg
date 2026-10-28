# 貪婪演算法（最近鄰點法）- 旅行推銷員問題（TSP）
import math, time

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

if __name__ == '__main__':
    t0 = time.perf_counter()
    path = greedy_tsp(start=0)
    t1 = time.perf_counter()
    print('【貪婪演算法 - 最近鄰點法】')
    print('路徑:', path)
    print('總長度:', round(path_len(path), 4))
    print('執行時間:', round(t1-t0, 6), '秒')
    print('說明: 每次選擇當前最近的未拜訪城市，只考慮當下最佳，無回溯。')

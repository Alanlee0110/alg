"""
數字動畫：用數字在終端機畫出會動的圖
用法：
    python number_art.py donut   # 旋轉的 3D 甜甜圈
    python number_art.py heart   # 跳動的愛心
    python number_art.py rain    # 數字雨（駭客任務風）
按 Ctrl+C 結束
"""
import math
import os
import random
import shutil
import sys
import time

os.system("")  # 讓 Windows 10+ 的終端機支援 ANSI 控制碼

HOME = "\x1b[H"        # 游標回到左上角
CLEAR = "\x1b[2J"      # 清除畫面
HIDE = "\x1b[?25l"     # 隱藏游標
SHOW = "\x1b[?25h"     # 顯示游標


def term_size():
    s = shutil.get_terminal_size((80, 24))
    return min(s.columns, 100), min(s.lines - 1, 40)


# ---------- 1. 旋轉的 3D 甜甜圈 ----------
def donut():
    ramp = "1742356980"      # 依筆畫「濃度」由淡到濃排列的數字
    A = B = 0.0
    while True:
        W, H = term_size()
        out = [" "] * (W * H)
        zbuf = [0.0] * (W * H)
        cA, sA, cB, sB = math.cos(A), math.sin(A), math.cos(B), math.sin(B)
        K2 = 5
        K1 = W * K2 * 3 / (8 * 3)
        theta = 0.0
        while theta < 6.28:
            ct, st = math.cos(theta), math.sin(theta)
            phi = 0.0
            while phi < 6.28:
                cp, sp = math.cos(phi), math.sin(phi)
                cx = 2 + ct              # 圓環上的點 (R2=2, R1=1)
                cy = st
                x = cx * (cB * cp + sA * sB * sp) - cy * cA * sB
                y = cx * (sB * cp - sA * cB * sp) + cy * cA * cB
                z = K2 + cA * cx * sp + cy * sA
                ooz = 1 / z
                xp = int(W / 2 + K1 * ooz * x)
                yp = int(H / 2 - K1 * ooz * y * 0.5)
                # 亮度（表面法向量與光源的內積）
                L = cp * ct * sB - cA * ct * sp - sA * st + cB * (cA * st - ct * sA * sp)
                if L > 0 and 0 <= xp < W and 0 <= yp < H:
                    i = xp + W * yp
                    if ooz > zbuf[i]:
                        zbuf[i] = ooz
                        out[i] = ramp[min(int(L * 7), len(ramp) - 1)]
                phi += 0.03
            theta += 0.08
        frame = "\n".join("".join(out[r * W:(r + 1) * W]) for r in range(H))
        sys.stdout.write(HOME + frame)
        sys.stdout.flush()
        A += 0.07
        B += 0.03


# ---------- 2. 跳動的愛心 ----------
def heart():
    t = 0.0
    while True:
        W, H = term_size()
        beat = 1 + 0.12 * abs(math.sin(t * 3)) ** 3   # 心跳縮放
        rows = []
        for r in range(H):
            line = []
            for c in range(W):
                x = (c - W / 2) / (W / 4.5) / beat
                y = -(r - H / 2.2) / (H / 2.8) / beat
                v = (x * x + y * y - 1) ** 3 - x * x * y ** 3
                if v <= 0:
                    d = int(c * 0.5 + r - t * 12) % 10   # 數字流動
                    line.append(f"\x1b[31m{d}")
                else:
                    line.append(" ")
            rows.append("".join(line))
        sys.stdout.write(HOME + "\n".join(rows) + "\x1b[0m")
        sys.stdout.flush()
        t += 0.05
        time.sleep(0.04)


# ---------- 3. 數字雨 ----------
def rain():
    W, H = term_size()
    trail = 10
    drops = [random.randint(-H, 0) for _ in range(W)]
    speed = [random.choice([1, 1, 2]) for _ in range(W)]
    while True:
        grid = [[" "] * W for _ in range(H)]
        for c in range(0, W, 2):
            head = drops[c]
            for k in range(trail):
                r = head - k
                if 0 <= r < H:
                    d = str(random.randint(0, 9))
                    if k == 0:
                        grid[r][c] = f"\x1b[97m{d}\x1b[0m"    # 雨滴頭：亮白
                    elif k < trail // 2:
                        grid[r][c] = f"\x1b[92m{d}\x1b[0m"    # 亮綠
                    else:
                        grid[r][c] = f"\x1b[32m{d}\x1b[0m"    # 暗綠
            drops[c] += speed[c]
            if drops[c] - trail > H:
                drops[c] = random.randint(-H // 2, 0)
                speed[c] = random.choice([1, 1, 2])
        sys.stdout.write(HOME + "\n".join("".join(row) for row in grid))
        sys.stdout.flush()
        time.sleep(0.05)


if __name__ == "__main__":
    modes = {"donut": donut, "heart": heart, "rain": rain}
    choice = sys.argv[1] if len(sys.argv) > 1 else "rain"
    if choice not in modes:
        print("請選擇：donut / heart / rain")
        sys.exit(1)
    sys.stdout.write(CLEAR + HIDE)
    try:
        modes[choice]()
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\x1b[0m" + SHOW + CLEAR + HOME)
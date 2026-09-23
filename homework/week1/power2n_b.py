from datetime import datetime

def power2n_2b(n):
    if n < 0: raise ValueError("n不能為負數")
    if n == 0: return 1
    return 2 * power2n_2b(n-1)

n = 100
startTime = datetime.now()
print(f'power2n_2b({n})={power2n_2b(n)}')
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')
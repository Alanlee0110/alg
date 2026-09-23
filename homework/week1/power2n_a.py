from datetime import datetime

def power2n_2a(n):
    if n < 0: raise ValueError("n不能為負數")
    if n == 0: return 1
    return power2n_2a(n-1) + power2n_2a(n-1)

n = 100
startTime = datetime.now()
print(f'power2n_2a({n})={power2n_2a(n)}')
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')
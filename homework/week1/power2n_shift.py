from datetime import datetime

def power2n_shift(n):
    return 1 << n

n = 100
startTime = datetime.now()
print(f'power2n_shift({n})={power2n_shift(n)}')
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')
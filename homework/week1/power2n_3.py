from datetime import datetime
pow =[None]*10000
pow[0] = 1
pow[1] = 2

def power2n_3(n):
    if n < 0: raise ValueError("n不能為負數")
    if pow[n] is not None: return pow[n]

    pow[n] = power2n_3(n-1) + power2n_3(n-1)
    return pow[n]

n = 100
startTime = datetime.now()
print(f'power2n_3({n})={power2n_3(n)}')
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')
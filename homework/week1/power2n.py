from datetime import datetime

def power2n(n):
    return 2**n

n = 100
startTime = datetime.now()
print(f'power2n({n})={power2n(n)}')
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')
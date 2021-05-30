# 몬테카를로 시뮬레이션으로 파이 구하기
import matplotlib.pyplot as plt
import numpy as np

plt.ion()
plt.xlim(0, 1)
plt.ylim(0, 1)
count=0

for j in range(1, 100000):
    x = np.random.rand(1)
    y = np.random.rand(1)
    if ((x-0.5)**2) + ((y-0.5)**2) <= (0.5)**2:
        plt.scatter(x, y, c='r', marker='.')
        count += 1
    else:
        plt.scatter(x, y, c='b', marker='.')
    plt.title(r'$\pi$ = %s' % (round(4 * count / j, 20)))
    plt.pause(0.0000001)
    plt.draw()
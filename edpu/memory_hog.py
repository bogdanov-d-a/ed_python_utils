from collections import deque
from random import getrandbits
from time import sleep


storage = deque()


while True:

    try:
        print('start')
        while True:
            for _ in range(128*1024):
                storage.append(getrandbits(8*1024))
            #sleep(1)

    except:
        print('stop')
        storage = deque()
        input()

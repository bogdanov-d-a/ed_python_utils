def main(sleep_time: float) -> None:
    from collections import deque

    storage = deque()

    while True:
        try:
            print('start')

            while True:
                from random import getrandbits
                from time import sleep

                for _ in range(128*1024):
                    storage.append(getrandbits(8*1024))

                sleep(sleep_time)

        except:
            print('stop')

            storage = deque()
            input()

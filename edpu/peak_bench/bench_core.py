from math import sin, cos, radians

def bench():
    product = 1.0
    for _ in range(1, 1000, 1):
        for dex in list(range(1, 360, 1)):
            angle = radians(dex)
            product *= sin(angle)**2 + cos(angle)**2
    return product

def bench_pack(iterations):
    for _ in range(iterations):
        bench()

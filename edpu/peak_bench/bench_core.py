from math import sin, cos, radians

def bench(iterations):
    product = 1.0
    for _ in range(iterations):
        for dex in range(360):
            angle = radians(dex)
            product *= sin(angle)**2 + cos(angle)**2
    return product

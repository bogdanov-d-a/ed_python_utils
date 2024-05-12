def block_region(origin: int, distance: int, end_sub: bool=False) -> tuple[int, int]:
    start = origin - distance
    end = origin + distance

    if end_sub:
        end -= 1

    return (start, end)

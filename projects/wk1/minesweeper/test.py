import itertools

height = 1
width = 3

def n(cell):
    for c in itertools.product(*(range(n-1, n+2) for n in cell)):
        if c != cell and 0 <= c[0] < height and 0 <= c[1] < width:
            yield c
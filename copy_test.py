original = [[1, 2, 3, 4], [2, 3, 4, 5]]
copied = []
for line in original:
    copied.append(list(map(lambda x: int(x), line)))
original[0] = 5
print(copied)

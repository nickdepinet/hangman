with open('google-books-common-words.txt') as f:
    lines = set(tuple(line.strip().split()) for line in f)

print len(lines)
print lines.pop()
print lines.pop()
print lines.pop()
print lines.pop()

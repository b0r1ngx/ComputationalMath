a = list(map(int, input().split()))
x = int(input())

def attemp():
    dif = 1000
    el_pos = 0
    if len(a) == 1:
        return a[0]
    if x in a:
        return x
    else:
        a.sort()
        for i in range(len(a) - 1):
            if a[i] < 0 and a[i + 1] < 0:
                c = min(abs(x - a[i]), abs(x - a[i + 1]))
            if c <= dif:
                dif = c
                el_pos = i
                if dif == 1:
                    if abs(a[i] - x) == 1:
                        return a[i]
                    else:
                        return a[i + 1]
        return a[el_pos]

print(attemp())

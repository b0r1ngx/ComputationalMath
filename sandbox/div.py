def gcd(a, b):
    maxi = max(a, b)
    mini = min(a, b)
    if maxi != mini:
        while maxi > mini:
            maxi -= mini
        return gcd(mini, maxi)
    else:
        return mini

def reduce_fraction(p, q):
    if p != q:
        divider = gcd(p, q)
        return int(p / divider), int(q / divider)
    else:
        return int(p), int(q)

n, m = int(input()), int(input())
print(*reduce_fraction(n, m))

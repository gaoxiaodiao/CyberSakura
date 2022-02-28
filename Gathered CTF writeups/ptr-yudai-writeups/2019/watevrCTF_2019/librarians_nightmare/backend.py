chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_'

c, a, k, d = map(int, open("keys.txt", "r").read().split())
m = 4902227890643
assert((c * d) % m == 1);

def n2st(n, length = 7):
    if length == 0:
        return ""
    ch = chars[n % len(chars)]
    return n2st(n // len(chars), length - 1) + ch

def f(n):
    if n == 0:
        return (c + k) % m
    if n % 2 == 0:
        fx = f(n // 2)
        return (k + (fx ** 2 - 2 * k * fx + k ** 2) * d) % m
    else:
        fx = f((n - 1) // 2)
        return (k + a * (fx ** 2 - 2 * k * fx + k ** 2) * d) % m

if __name__ == "__main__":
    while True:
        print(n2st(f(int(input()))))


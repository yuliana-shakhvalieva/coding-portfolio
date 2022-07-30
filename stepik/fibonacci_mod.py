def fib_mod(n, m):
    F_0 = 0
    F_1 = 1
    F_mod = [0]
    F_mod.insert(1, F_1 % m)
    for i in range(2, n+1):
        F_2 = F_0 + F_1
        F_mod.insert(i, F_2 % m)
        if (F_mod[i-1] == F_mod[0]) & (F_mod[i] == F_mod[1]):
            F_mod = F_mod[0:i-1]
            break
        else:
            F_0 = F_1
            F_1 = F_2
    return F_mod[n % len(F_mod)]


def main():
    n, m = map(int, input().split())
    print(fib_mod(n, m))


if __name__ == "__main__":
    main()
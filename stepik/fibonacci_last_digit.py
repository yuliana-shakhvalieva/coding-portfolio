def fib_digit(n):
    F = [0 for i in range(n+1)]
    F[1] = 1
    for i in range(2, len(F)):
        F[i] = (F[i-1] + F[i-2]) % 10
    return F[n]


def main():
    n = int(input())
    print(fib_digit(n))


if __name__ == "__main__":
    main()
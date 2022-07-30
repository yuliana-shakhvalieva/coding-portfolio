def gcd(a, b):
    while a * b != 0:
        if a >= b:
            a = a % b
        else:
            b = b % a

    if a == 0:
        return b
    else:
        return a


def main():
    a, b = map(int, input().split())
    print(gcd(a, b))


if __name__ == "__main__":
    main()
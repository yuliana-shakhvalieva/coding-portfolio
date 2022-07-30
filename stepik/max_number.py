def main():
    N, D, K = map(int, input().split())
    numbers = list(map(int, input().split()))
    k = 0

    for i in range(D):
        while numbers.count(i) > 0 and k < K:
            k += 1
            numbers.remove(i)

    print(''.join(map(str, numbers)))


if __name__ == "__main__":
    main()

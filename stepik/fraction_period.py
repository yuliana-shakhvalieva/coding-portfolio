def division(M):
    for i in [2, 5]:
        while M % i == 0:
            M = M / i
    return M


def count_len_period(M):
    len_period = 1
    while (10 ** len_period) % M != 1:
        len_period += 1
    return len_period


def main():
    N = int(input())
    M = int(input())

    if N % M == 0:
        print(0)
    else:
        if M % 2 == 0 or M % 5 == 0:
            m = division(M)
            len_period = count_len_period(m)
        else:
            len_period = count_len_period(M)

        z = str(N / M)[2:]
        i = 0
        flag = True
        while flag:
            if z[i:i + len_period] == z[i + len_period:i + 2 * len_period]:
                flag = False
                print(z[i:i + len_period])
            else:
                i += 1


if __name__ == "__main__":
    main()

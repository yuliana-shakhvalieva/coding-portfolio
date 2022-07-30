from fractions import Fraction


def main():
    print('Введите число в формате: 0.a1__an(b1__bn)')
    n = input()
    n_main = n[2: n.index('(')]
    n_period = n[n.index('(') + 1: len(n) - 1]
    denominator = ''.join(map(str, [9 for i in range(len(n_period))])) + \
                  ''.join(map(str, [0 for i in range(len(n_main))]))

    print(Fraction(int(n_main + n_period) - int(n_main), int(denominator)))


if __name__ == "__main__":
    main()

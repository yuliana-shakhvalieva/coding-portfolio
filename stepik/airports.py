def count_transfer(start, dict_flights, finish):
    if start not in dict_flights.keys():
        return -1
    if finish in dict_flights[start]:
        return 0
    destination = dict_flights.pop(start)
    answer = [count_transfer(i, dict_flights, finish) for i in destination]
    try:
        return min([i for i in answer if i >= 0]) + 1
    except ValueError:
        return -1


def main():
    finish, k, N = str(input()), int(input()), int(input())
    flights = [str(input()).split() for i in range(N)]
    start_points = sorted(set([flights[i][0] for i in range(N)]))
    dict_flights = dict.fromkeys(start_points)
    for start_point in start_points:
        end_points = []
        for i in range(N):
            if start_point == flights[i][0]:
                end_points.append(flights[i][1])
        dict_flights.update({start_point: end_points})
    answer = count_transfer('LED', dict_flights, finish)

    if 0 <= answer <= k:
        print(answer)
    else:
        print('impossible')


if __name__ == "__main__":
    main()

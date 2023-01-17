
def solve(input):
    number = input['X']
    aux = number
    reverse = 0

    while aux:
        reverse = reverse * 10 + aux % 10
        aux = aux // 10
    if number != reverse:
        return {'Z': 0}

    div = 2
    while div ** 2 <= number:
        if number % div == 0:
            return {'Z': 0}
        div += 1

    return {'Z': 1}
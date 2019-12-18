"""In this kata we will only consider finite series and you are required to return a code according to the type of
sequence"""


def sequence_classifier(arr):
    answers_dict = {
        (True, True): 1,  # strictly increasing
        (False, True): 2,  # not decreasing
        (True, False): 3,  # strictly decreasing
        (False, False): 4  # not increasing
    }
    if len(set(arr)) == 1:
        return 5
    strictly = arr[1] != arr[0]
    increasing = arr[1] > arr[0]
    for number in range(2, len(arr)):
        if arr[number] < arr[number - 1]:
            increasing = False
        else:
            increasing = True
        if arr[number] == arr[number - 1]:
            strictly = False
    return answers_dict[(strictly, increasing)]


print(sequence_classifier([8, 8, 8, 8, 8, 9]))

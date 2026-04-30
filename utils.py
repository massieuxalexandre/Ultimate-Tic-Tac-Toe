

def clear():
    for _ in range(100):
        print()

def valid_choice(choice, start, end):
    arr = list()
    for i in range(start, end+1):
        arr.append(str(i))

    return choice in arr

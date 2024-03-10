def ReverseStringIteration(string):
    ret_val = ""
    len_string = len(string) - 1
    for i in range(len_string, -1, -1):
        ret_val += string[i]
    return ret_val


def ReverseStringRecursion(remaining, reversed=""):
    if len(remaining) > 0:
        reversed = reversed + remaining[-1]
        return ReverseStringRecursion(remaining[0:-1], reversed)
    else:
        return reversed


if __name__ == "__main__":
    print("Recursive: " + ReverseStringRecursion("hello"))
    print("Iterative: " + ReverseStringIteration("hello"))
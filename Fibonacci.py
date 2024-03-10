def FibonacciIterative(n):
    if n == 0:
        return []
    
    ret_val = [1]
    n -= 1
    prev_val = 0
    curr_val = 1
    
    for i in range(n):
        new_val = prev_val + curr_val
        prev_val = curr_val
        curr_val = new_val
        ret_val += [new_val]
        
    return ret_val


def FibonacciRecursive(n, prev=0, curr=1):
    if n == 0:
        return []
    else:
        ret = []
        new = prev + curr
        ret += [curr] + FibonacciRecursive(n - 1, curr, new)
        return ret
    

if __name__ == "__main__":
    print(FibonacciIterative(10))
    print(FibonacciRecursive(10))
    
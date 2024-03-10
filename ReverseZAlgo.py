# Doesn't work at the moment


def ReverseZAlgo(string):
    """Implements Gusfield's Z-Algorithm to compute the z-values of a given string

    Args:
        string (str): The string to compute z-values for

    Returns:
        List[List[int]]: A list of lists. At the 0th index, a list of z_values generated. At index 1, the Zbox values.
        At index 2, the L values and at index 3, the R values. All of these are lists of integers.
    """
	
    m = len(string)
    z_vals = [None] * m
    l = m
    r = m
    for pos in range(m - 2, -1, -1):
        k = pos
        if string[k] == string[m-1]:
            # case 2
            if k >= l:
                # case 2a
                if z_vals[k+(m-r)-1] > l-k+1:
                    # print(k, "2a")
                    z_vals[k] = z_vals[k+(m-r)-1]
                
                # case 2b
                elif z_vals[k+(m-r)-1] > l-k+1:
                    # print(k, "2b")
                    z_vals[pos] = l+(m-k)-1
                    
                # case 2c
                elif z_vals[k+(m-r)-1] == l-k+1:
                    # print(k, "2c")
                    k = l - 1
                    r = pos
                    while k > 0 and string[k] == string[k + (m-pos) - 1]:
                        k -= 1
                    l = k + 1
            else:
                k -= 1
                r = pos
                while k > 0 and string[k] == string[k + (m-pos) - 1]:
                    k -= 1
                l = k + 1
            
        # update zi values
        if z_vals[pos] is None:
            z_vals[pos] = pos - k
    
    return (z_vals)


if __name__ == "__main__":
    string = "hello"
    z_vals = ReverseZAlgo(string)

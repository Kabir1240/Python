def ZAlgo(string):
    """Implements Gusfield's Z-Algorithm to compute the z-values of a given string

    Args:
        string (str): The string to compute z-values for

    Returns:
        List[List[int]]: A list of lists. At the 0th index, a list of z_values generated. At index 1, the Zbox values.
        At index 2, the L values and at index 3, the R values. All of these are lists of integers.
    """
	
    z_vals = [None] * len(string)
    z_box = []
    l_vals = []
    r_vals = []
    l = 0
    r = 0
    for pos in range(1, len(string)):
        k = pos
        if string[k] == string[0]:
            # case 2
            if k <= r:
                # case 2a
                if z_vals[k-l] < r-k+1:
                    # print(k, l, "2a")
                    z_vals[k] = z_vals[k-l]
                # case 2b
                elif z_vals[k-l] > r-k+1:
                    # print("2b")
                    z_vals[pos] = r-k+1
                # case 2c
                elif z_vals[k-l] == r-k+1:
                    # print("2c")
                    k = r + 1
                    l = pos
                    while k < len(string) and string[k] == string[k - pos]:
                        k += 1
                    r = k - 1
                    z_box += [(l + 1, r + 1)]
            else:
                k += 1
                l = pos
                while k < len(string) and string[k] == string[k - pos]:
                    k += 1
                r = k - 1
                z_box += [(l + 1, r + 1)]
            
        # update zi values
        if z_vals[pos] is None:
            z_vals[pos] = k - pos
        
        # Update li values
        if l == 0:
            continue
        elif (len(l_vals) == 0 or l + 1 <= l_vals[-1] or l + 1 >= r_vals[-1]):
            l_vals.append(l + 1)
        else:
            l_vals.append(l_vals[-1])
            
        # update ri values
        if r == 0:
            continue
        elif len(r_vals) == 0 or r + 1 >= r_vals[-1]:
            r_vals.append(r + 1)
        else:
            r_vals.append(r_vals[-1])
    
    return (z_vals, z_box, l_vals, r_vals)


if __name__ == "__main__":
    string1 = "aabaabcaxaabaabcy"
    string2 = "aabcaabcaaab"
    string3 = "aabcaabxaaazabacaazaabccaabcaabxaaabaab"
    z_vals = ZAlgo(string3)
    print(z_vals)
    # print("the Zi Values are " + str(z_vals[0]) + "\n"
    #       + "the Z box Values are " + str(z_vals[1]) + "\n"
    #       + "the l values Values are " + str(z_vals[2]) + "\n"
    #       + "the r values Values are " + str(z_vals[3]) + "\n")

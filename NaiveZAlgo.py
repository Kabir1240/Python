# this is the very basic pattern matching algorithm
def NaivePatMatch(txt, pat):
    """Checks where the pattern pat occurs in the text txt

    :param txt: a string of text
    :type txt: String
    :param pat: a pattern to search for in txt
    :type pat: String
    :return: the positions where the pattern occurs in the text
    :rtype: List
    :Complexity: O(mn)
    """
    
    match = []
    for i in range(len(txt)):
        k = i
        for j in range(len(pat)):
            if k > len(txt) - 1:
                break
            elif txt[k] == pat[j]:
                k += 1
                continue
            else:
                break
        if j == len(pat) - 1:
            match += [i + 1]
    return match


# This Z-algo only calculates the Zi values
def ZAlgo_i(string):
    z_vals = [None] * len(string)
    for pos in range(1, len(string)):
        k = pos
        while k < len(string) and string[k] == string[k - pos]:
            k += 1
        z_vals[pos] = k - pos
        
    return z_vals


# Z-algo without optimization
def ZAlgo(string):
    z_vals = [None] * len(string)
    z_box = []
    l_vals = []
    r_vals = []
    l = 0
    r = 0
    for pos in range(1, len(string)):
        k = pos
        if string[k] == string[0]:
            k += 1
            l = pos
            while k < len(string) and string[k] == string[k - pos]:
                k += 1
            r = k - 1
            z_box += [(l + 1, r + 1)]
            
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
            
        # update zi values
        z_vals[pos] = k - pos
    
    return (z_vals, z_box, l_vals, r_vals)
    
    
if __name__ == "__main__":
    # print(NaivePatMatch("abcabc", "abc"))
        
    # print("the Zi values are: " + str(ZAlgo_i("aabaabcaxaabaabcy")))
    string1 = "aabaabcaxaabaabcy"
    string2 = "aabcaabcaaab"
    z_vals = ZAlgo(string1)
    print("the Zi Values are " + str(z_vals[0]) + "\n"
          + "the Z box Values are " + str(z_vals[1]) + "\n"
          + "the l values Values are " + str(z_vals[2]) + "\n"
          + "the r values Values are " + str(z_vals[3]) + "\n")
    
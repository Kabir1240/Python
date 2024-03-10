	
##### STEP - 1
def Z_algo(string: str):
    """Implements Gusfield's Z-Algorithm to compute the z-values of a given string

    Args:
        string (str): The string to compute z-values for

    Returns:
        List[int]: A list of length len(string), with each index i corresponding to
                the z_i-value of the input string. First index is always None
    """
    
    # ADD YOUR Z-ALGO CODE HERE
    string = string[::-1]
    z_vals = [None] * len(string)
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
            else:
                k += 1
                l = pos
                while k < len(string) and string[k] == string[k - pos]:
                    k += 1
                r = k - 1
            
        # update zi values
        if z_vals[pos] is None:
            z_vals[pos] = k - pos
    z_vals[0] = len(z_vals)
    return (z_vals[::-1])

##### STEP - 2
def good_suffix(pat: str):
    # ADD GOOD_SUFFIX CODE HERE
    z_array = Z_algo(pat)
    m = len(z_array)
    gs = [0] * (m + 1)
    j = []
    for p in range(m):
        j = m - (z_array[p]) + 1
        gs[j-1] = p + 1
    return(gs)

##### STEP - 3
def matched_prefix(pat: str):
    # ADD MATCHED_PREFIX CODE HERE
    z_array = Z_algo(pat)
    m = len(z_array)
    max_mp = 0
    mp_array = [0] * (m)
    
    for i in range(m):
        if z_array[i] > max_mp and z_array[i] - i == 1:
            mp_array[i] = z_array[i]
            max_mp = z_array[i]
        else:
            mp_array[i] = max_mp
    
    mp_array = mp_array[::-1]
    mp_array.append(0)
    return mp_array






def test_helper_gs(word, expected):
    try:
        assert good_suffix(word)[1:] == expected[1:]
    except AssertionError:
        print(
            f"Error computing good_suffix for {word}!\n\t{expected}\n\tActual:{good_suffix(word)}")

def test_helper_mp(word, expected):
    try:
        assert matched_prefix(word)[1:] == expected[1:]
    except AssertionError:
        print(
            f"Error computing matched_prefix for {word}!\n\t{expected}\n\tActual:{matched_prefix(word)}")

def test_goodsuffix() -> None:
    word="acbaa"
    expected = [None, 0, 0, 0, 4, 3]
    test_helper_gs(word, expected)
    word="bbacbbabab"
    expected = [None, 0, 0, 0, 0, 0, 0, 8, 0, 6, 9]
    test_helper_gs(word, expected)
    word="acbacbccbababacbccba"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 4, 14, 1, 19]
    test_helper_gs(word, expected)
    word="babbbabccbacccbbaacb"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 16, 19]
    test_helper_gs(word, expected)
    word="bccaacaccb"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9]
    test_helper_gs(word, expected)
    word="bccbcccbaacaabacccac"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 18, 19]
    test_helper_gs(word, expected)
    word="ccbbababca"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 7, 9]
    test_helper_gs(word, expected)
    word="acccbcbcca"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9]
    test_helper_gs(word, expected)
    word="abcaabcaac"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 7, 9]
    test_helper_gs(word, expected)
    word="bbcccbabbaccbcbcacab"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 15, 19]
    test_helper_gs(word, expected)
    word="acacbcbbabcbaca"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 13, 14]
    test_helper_gs(word, expected)
    word="cbbcaaccccbbccb"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 2, 12, 14]
    test_helper_gs(word, expected)
    word="bbabc"
    expected = [None, 0, 0, 0, 0, 4]
    test_helper_gs(word, expected)
    word="bbabacacbacbaacacbbb"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 18, 17]
    test_helper_gs(word, expected)
    word="bbbbbccaccbbabb"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 14, 13]
    test_helper_gs(word, expected)
    word="accbbabacaabcbaaaccb"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 14, 12, 19]
    test_helper_gs(word, expected)
    word="accaaabcacbacba"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 9, 14]
    test_helper_gs(word, expected)
    word="bbacababcaaacbcbcbaa"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 19, 18]
    test_helper_gs(word, expected)
    word="bcacabbacaaaaba"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 13, 14]
    test_helper_gs(word, expected)
    word="baaabaabbbbacccaabaa"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 3, 17, 19, 18]
    test_helper_gs(word, expected)
    word="aabcaabxaaazabacaazaabccaabcaabxaaabaab"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 14, 0, 38]
    test_helper_gs(word, expected)
    print('GS Testing Done .... !')

def test_matchedprefix() -> None:
    word = "acbaa"
    expected = [5, 1, 1, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "bbacbbabab"
    expected = [10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "acbacbccbababacbccba"
    expected = [20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "babbbabccbacccbbaacb"
    expected = [20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "bccaacaccb"
    expected = [10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "bccbcccbaacaabacccac"
    expected = [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    test_helper_mp(word, expected)
    word = "ccbbababca"
    expected = [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    test_helper_mp(word, expected)
    word = "acccbcbcca"
    expected = [10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "abcaabcaac"
    expected = [10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    test_helper_mp(word, expected)
    word = "bbcccbabbaccbcbcacab"
    expected = [20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "acacbcbbabcbaca"
    expected = [15, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "cbbcaaccccbbccb"
    expected = [15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0]
    test_helper_mp(word, expected)
    word = "bbabc"
    expected = [5, 0, 0, 0, 0, 0]
    test_helper_mp(word, expected)
    word = "bbabacacbacbaacacbbb"
    expected = [20, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0]
    test_helper_mp(word, expected)
    word = "bbbbbccaccbbabb"
    expected = [15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0]
    test_helper_mp(word, expected)
    word = "accbbabacaabcbaaaccb"
    expected = [20, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0]
    test_helper_mp(word, expected)
    word = "accaaabcacbacba"
    expected = [15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    test_helper_mp(word, expected)
    word = "bbacababcaaacbcbcbaa"
    expected = [20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    test_helper_mp(word, expected)
    word = "bcacabbacaaaaba"
    expected = [15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    test_helper_mp(word, expected)
    word = "baaabaabbbbacccaabaa"
    expected = [20, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0]
    test_helper_mp(word, expected)
    word = "aabcaabxaaazabacaazaabccaabcaabxaaabaab"
    expected = [39, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 0, 0, 0]
    test_helper_mp(word, expected)
    print('MP Testing Done .... !')


if __name__ == "__main__":
    test_goodsuffix()
    test_matchedprefix()
    

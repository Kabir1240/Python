from typing import List
import string, random, time


def z_value_naive(string: str) -> List[int]:
    """Implements a naive algorithm to compute the z-values of a given string

    Args:
        string (str): The string to compute z-values for

    Returns:
        List[int]: A list of length len(string), with each index i corresponding to
                the z_i-value of the input string. First index is always None
    """
    
    # Type your implementation here
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
    
    return (z_vals)
	


def z_algo(string: str) -> List[int]:
    """Implements Gusfield's Z-Algorithm to compute the z-values of a given string

    Args:
        string (str): The string to compute z-values for

    Returns:
        List[int]: A list of length len(string), with each index i corresponding to
                the z_i-value of the input string. First index is always None
    """
	
    # Type your implementation here
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
    
    return (z_vals)


# function to time and compare performance of naive and Gusfield's Z algorithms
def time_complexity_comparison() -> None:
    sizes = [10, 1000, 10000, 100000, 1000000, 10000000]
    
    naive_times = []
    gusfield_times = []
    
    for size in sizes:
        print(f"Currently timing string of size {size}")
        word = ''.join(random.choice(list(string.printable)) for _ in range(size))
        # timing naive:
        start_time = time.time()
        naive_results = z_value_naive(word)
        end_time = time.time()
        naive_times.append(end_time - start_time)
        
        # timing gusfield's
        start_time = time.time()
        gusfield_results = z_algo(word)
        end_time = time.time()
        gusfield_times.append(end_time - start_time)
        
        try:
            assert naive_results == gusfield_results
        except AssertionError:
            print(f"Naive produced: {naive_results}\nGusfield produced: {gusfield_results}\n for string {word}")
            exit(1)
    
    # round results to the same length float:
    naive_times = [round(t,6) for t in naive_times]
    gusfield_times = [round(t,6) for t in gusfield_times]
    
    # print results:
    print(f"Naive: \t{naive_times}")
    print(f"Gus:   \t{gusfield_times}")


def test_z_alg() -> None:    
    word="acbaa"
    expected = [None, 0, 0, 1, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for acbaa!\n\tExpected:[None, 0, 0, 1, 1]\n\tActual:{z_algo(word)}")

    word="bbacbbabab"
    expected = [None, 1, 0, 0, 3, 1, 0, 1, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbacbbabab!\n\tExpected:[None, 1, 0, 0, 3, 1, 0, 1, 0, 1]\n\tActual:{z_algo(word)}")

    word="acbacbccbababacbccba"
    expected = [None, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 1, 0, 3, 0, 0, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for acbacbccbababacbccba!\n\tExpected:[None, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 1, 0, 3, 0, 0, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="babbbabccbacccbbaacb"
    expected = [None, 0, 1, 1, 3, 0, 1, 0, 0, 2, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for babbbabccbacccbbaacb!\n\tExpected:[None, 0, 1, 1, 3, 0, 1, 0, 0, 2, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="bccaacaccb"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bccaacaccb!\n\tExpected:[None, 0, 0, 0, 0, 0, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="bccbcccbaacaabacccac"
    expected = [None, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bccbcccbaacaabacccac!\n\tExpected:[None, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]\n\tActual:{z_algo(word)}")

    word="ccbbababca"
    expected = [None, 1, 0, 0, 0, 0, 0, 0, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for ccbbababca!\n\tExpected:[None, 1, 0, 0, 0, 0, 0, 0, 1, 0]\n\tActual:{z_algo(word)}")

    word="acccbcbcca"
    expected = [None, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for acccbcbcca!\n\tExpected:[None, 0, 0, 0, 0, 0, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="abcaabcaac"
    expected = [None, 0, 0, 1, 5, 0, 0, 1, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for abcaabcaac!\n\tExpected:[None, 0, 0, 1, 5, 0, 0, 1, 1, 0]\n\tActual:{z_algo(word)}")

    word="bbcccbabbaccbcbcacab"
    expected = [None, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbcccbabbaccbcbcacab!\n\tExpected:[None, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="acacbcbbabcbaca"
    expected = [None, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for acacbcbbabcbaca!\n\tExpected:[None, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 1]\n\tActual:{z_algo(word)}")

    word="cbbcaaccccbbccb"
    expected = [None, 0, 0, 1, 0, 0, 1, 1, 1, 4, 0, 0, 1, 2, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for cbbcaaccccbbccb!\n\tExpected:[None, 0, 0, 1, 0, 0, 1, 1, 1, 4, 0, 0, 1, 2, 0]\n\tActual:{z_algo(word)}")

    word="bbabc"
    expected = [None, 1, 0, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbabc!\n\tExpected:[None, 1, 0, 1, 0]\n\tActual:{z_algo(word)}")

    word="bbabacacbacbaacacbbb"
    expected = [None, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbabacacbacbaacacbbb!\n\tExpected:[None, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2, 1]\n\tActual:{z_algo(word)}")

    word="bbbbbccaccbbabb"
    expected = [None, 4, 3, 2, 1, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbbbbccaccbbabb!\n\tExpected:[None, 4, 3, 2, 1, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1]\n\tActual:{z_algo(word)}")

    word="accbbabacaabcbaaaccb"
    expected = [None, 0, 0, 0, 0, 1, 0, 2, 0, 1, 1, 0, 0, 0, 1, 1, 4, 0, 0, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for accbbabacaabcbaaaccb!\n\tExpected:[None, 0, 0, 0, 0, 1, 0, 2, 0, 1, 1, 0, 0, 0, 1, 1, 4, 0, 0, 0]\n\tActual:{z_algo(word)}")

    word="accaaabcacbacba"
    expected = [None, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for accaaabcacbacba!\n\tExpected:[None, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1]\n\tActual:{z_algo(word)}")

    word="bbacababcaaacbcbcbaa"
    expected = [None, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bbacababcaaacbcbcbaa!\n\tExpected:[None, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]\n\tActual:{z_algo(word)}")

    word="bcacabbacaaaaba"
    expected = [None, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for bcacabbacaaaaba!\n\tExpected:[None, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0]\n\tActual:{z_algo(word)}")

    word="baaabaabbbbacccaabaa"
    expected = [None, 0, 0, 0, 3, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for baaabaabbbbacccaabaa!\n\tExpected:[None, 0, 0, 0, 3, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0]\n\tActual:{z_algo(word)}")
        
    word="aabcaabxaaazabacaazaabccaabcaabxaaabaab"
    expected = [None, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0, 1, 0, 1, 0, 2, 1, 0, 4, 1, 0, 0, 0, 11, 1, 0, 0, 3, 1, 0, 0, 2, 3, 1, 0, 3, 1, 0]
    try:
        assert z_algo(word)[1:] == expected[1:]
    except AssertionError:
        print(f"Error computing Z-values for aabcaabxaaazabacaazaabccaabcaabxaaabaab!\n\tExpected:[None, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0, 1, 0, 1, 0, 2, 1, 0, 4, 1, 0, 0, 0, 11, 1, 0, 0, 3, 1, 0, 0, 2, 3, 1, 0, 3, 1, 0]\n\tActual:{z_algo(word)}")

if __name__ == "__main__":
    # time_complexity_comparison()
    test_z_alg()
    
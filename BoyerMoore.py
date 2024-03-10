def boyer_moore(string, pat):
    m = len(string)
    n = len(pat)
    
    # Preprocessing
    z_array = get_z_array(pat)
    bc_array = get_ebc_array(pat)
    gs_array = get_gs_array(z_array)
    mp_array = get_mp_array(z_array)
    
    ret_val = []
    
    pos = 0
    start = None
    stop = None
    while pos + (n-1) < m:
        mm_idx = compare(string, pat, n, pos, start, stop)
        
        start = None
        stop = None
        # full match
        if mm_idx == pos - 1:
            ret_val.append(pos)
            shift = max(mp_array[1], 1)
        # mismatch
        else:
            gs_shift = get_gs_shift(pos, mm_idx, n, gs_array, mp_array)
            ebc_shift = get_ebc_shift(pos, mm_idx, bc_array, string[mm_idx])
            
            if gs_shift[0] > ebc_shift:
                shift = gs_shift[0]
                start = gs_shift[1]
                stop = gs_shift[2]
            else:
                shift = ebc_shift
                
        pos += shift
    return ret_val


def compare(string, pat, n, pos, start=None, stop=None):
    """
    Given the text, pattern, the current position of the pattern over the text and range of the pattern that is currently known to match the text(so these regions can be skipped in explicit character comparisons), performs character comparisons and returns position of first mismatched character
    """
    
    # if there are no comparisons to skip
    if start is None and stop is None:
        k = pos + n - 1
        while k >= pos and string[k] == pat[k - pos]:
            k -= 1
        return k
    
    # galil's optimization to skip comparisons
    else:
        k = pos + n - 1
        while k >= stop and string[k] == pat[k - pos]:
            k -= 1
            
        if k >= stop:
            return k
        
        k = start
        while k >= pos and string[k] == pat[k - pos]:
            k -= 1
        return k

def get_ebc_array(pat):
    """
    given pattern, calculates the extended bad character rule array
    """
    m = len(pat)
    bc_array = [[0]*93 for _ in range(m)]                # 93 printable characters in ASCII, 33-126
    for i in range(m):
        for j in range(0, i):
            current = ord(pat[j]) - 33
            bc_array[i][current] = j + 1
            
    return(bc_array)
    

def get_z_array(pat):
    """Implements Gusfield's Z-Algorithm in reverse to compute the reverse z-values of a given string

    Args:
        string (str): The string to compute reverse z-values for

    Returns:
        List[List[int]]: A list of lists. At the 0th index, a list of z_values generated. At index 1, the Zbox values.
        At index 2, the L values and at index 3, the R values. All of these are lists of integers.
    """
    pat = pat[::-1]
    z_vals = [None] * len(pat)
    l = 0
    r = 0
    for pos in range(1, len(pat)):
        k = pos
        if pat[k] == pat[0]:
            # case 2
            if k <= r:
                # case 2a
                if z_vals[k-l] < r-k+1:
                    z_vals[k] = z_vals[k-l]
                # case 2b
                elif z_vals[k-l] > r-k+1:
                    z_vals[pos] = r-k+1
                # case 2c
                elif z_vals[k-l] == r-k+1:
                    k = r + 1
                    l = pos
                    while k < len(pat) and pat[k] == pat[k - pos]:
                        k += 1
                    r = k - 1
            else:
                k += 1
                l = pos
                while k < len(pat) and pat[k] == pat[k - pos]:
                    k += 1
                r = k - 1
            
        # update zi values
        if z_vals[pos] is None:
            z_vals[pos] = k - pos
    z_vals[0] = len(z_vals)
    return (z_vals[::-1])


def get_gs_array(z_array):
    """
    Given the pattern, calculate the good suffix array
    """
    m = len(z_array)
    gs = [0] * (m + 1)
    j = []
    for p in range(m):
        j = m - (z_array[p]) + 1
        gs[j-1] = p + 1
    return(gs)
    
    
def get_mp_array(z_array):
    """
    given pattern, calculate the matched prefix array
    """
    # O(2N) complexity -> O(N)
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


def get_gs_shift(pos, mm_idx, n, gs_array, mp_array):
    """
    given the mismatch position, the good suffix array and the matched prefix array, computes the good suffix shift and the range within the pattern that can be skipped from explicit character comparisons in the next iteration
    """
    
    gs_shift = gs_array[mm_idx-pos + 1]
    next_pos = pos + (n - gs_shift)
    p = next_pos + gs_shift
    if gs_shift > 0:
        return [n-gs_shift, p-((pos+n-1) - mm_idx), p]
    elif mp_array[mm_idx-pos + 1] > 0:
        return [n - mp_array[mm_idx-pos + 1], next_pos, next_pos + mp_array[mm_idx-pos + 1]]
    else:
        return [1, None, None]


def get_ebc_shift(pos, mm_idx, bc_array, mm_char):
    """
    given the mismatch position, the bad character and the bad character array, computes the shift resulting from the bad character rule and the range within the pattern that can be skipped from explicit character comparisons in the next iteration
    """
    ebc = mm_idx - pos - bc_array[mm_idx-pos][ord(mm_char) - 33]
    if ebc > 0:
        return ebc
    else:
        return 1
    

if __name__ == "__main__":
    string = "cggtgcgggcctcttcgctattacgccagctggcgaaagggggatgtgctgcaaggcgattaagttgggtaacgccagggttttcccagtcacgacgttgtaaaacgacggccagtgagcgcgcgtaatacgactcactatagggcgaattggagctccaccgcggtggcggccgctctagaactagtggatcccccgggctgcaggaattcgatatcaagcttatcgataccgtcgacctcgagggggggcccggtacccagcttttgttccctttagtgagggttaattgcgcgcttg"
    pat = "ctc"
    
    

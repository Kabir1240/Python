import sys


def bwt_pattern_matching(string, pattern, distance):
    n = len(string)
    m = len(pattern)
    final = []
    n_occurrences, rank = compute_rank(string)

    def backward_search(pattern_index, sp, en, distance):
        ret_val = 0
        if sp >= n:
            return 0
        if en < 0:
            return 0

        if distance < 0:
            return 0
        elif pattern_index < 0 and distance == 0:
            return en - sp + 1
        elif pattern_index < 0 and distance > 0:
            return 0

        for i in range(len(rank)):
            sp_copy = sp
            en_copy = en
            rank_index = rank[i]
            if rank[i] is not None:
                while n_occurrences[i][sp_copy] == 0 and sp_copy > 0:
                    sp_copy -= 1
                if string[sp] == chr(i+36):
                    next_sp = rank_index + n_occurrences[i][sp_copy] - 1
                else:
                    next_sp = rank_index + n_occurrences[i][sp_copy]

                while n_occurrences[i][en_copy] == 0 and en_copy > 0:
                    en_copy -= 1
                next_en = rank_index + n_occurrences[i][en_copy] - 1

                if next_sp > next_en and distance > 0:
                    ret_val += backward_search(pattern_index - 1, 0, n-1, distance-1)
                elif next_sp > next_en and distance == 0:
                    ret_val += 0
                else:
                    # for the area that matches successfully
                    if chr(i + 36) == pattern[pattern_index]:
                        ret_val += backward_search(pattern_index - 1, next_sp, next_en, distance)

                    # for the "mismatched area"
                    else:
                        ret_val += backward_search(pattern_index - 1, next_sp, next_en, distance-1)
        return ret_val

    for i in range(distance+1):
        final.append(backward_search(m-1, 0, n-1, i))

    return final


def compute_rank(bwt_string: str):
    n = len(bwt_string)
    string_sorted = sorted(bwt_string)
    rank = [None] * 91
    counter = [0] * 91
    n_occurrence = [[0] * n for _ in range(91)]
    for i in range(n):
        index = ord(string_sorted[i]) - 36
        if rank[index] is None:
            rank[index] = i

        index = ord(bwt_string[i]) - 36
        counter[index] += 1
        n_occurrence[index][i] = counter[index]

    return n_occurrence, rank


print(bwt_pattern_matching("lo$oogg", "go", 2))

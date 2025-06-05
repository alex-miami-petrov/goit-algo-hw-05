import timeit
import collections 
import hashlib


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f
        return f.read()
    except FileNotFoundError as e:
        print(f"{path} not found")
        return ""
    

file_1 = read_file('data/стаття_1.txt')
file_2 = read_file('data/стаття_2.txt')


def build_bad_char_table(pattern):
    table = {}
    for i, char in enumerate(pattern[:-1]):
        table[char] = len(pattern) - 1 - i
    return table

def boyer_moore_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0: return 0
    if m > n: return -1

    bad_char_table = build_bad_char_table(pattern)
    i = 0
    while i <= n - m:
        j = m - 1 
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0: 
            return i
        else:
            char_in_text = text[i + j]
            shift = bad_char_table.get(char_in_text, m)
            i += max(1, shift - (m - 1 - j))
    return -1


def build_lps_array(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0 
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0: return 0
    if m > n: return -1

    lps = build_lps_array(pattern)
    i = 0 
    j = 0 
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j 
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def rabin_karp_search(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    if m == 0: return 0
    if m > n: return -1

    p = 0 
    t = 0 
    h = 1


    for i in range(m - 1):
        h = (h * d) % q

    
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    
    for i in range(n - m + 1):
        if p == t:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                return i

        
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q

            if t < 0:
                t = t + q
    return -1



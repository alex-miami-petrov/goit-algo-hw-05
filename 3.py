import timeit
import collections
import hashlib


def read_file(path):
    try:
        with open(path, "r", encoding='utf-8', errors='ignore') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Помилка: Файл '{path}' не знайдено.")
        return ""
    except Exception as e:
        print(f"Невідома помилка при читанні файлу '{path}': {e}")
        return ""

file_1 = read_file('data/стаття_1.txt')
file_2 = read_file('data/стаття_2.txt')

if not file_1:
    print("Вміст 'стаття_1.txt' не завантажено. Перевірте шлях та кодування файлу.")
    exit()
if not file_2:
    print("Вміст 'стаття_2.txt' не завантажено. Перевірте шлях та кодування файлу.")
    exit()


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


existing_substring_1 = "двійковий пошук"
non_existing_substring_1 = "вигаданий підрядок для статті_1_якого_не_існує"

existing_substring_2 = "рекомендаційних систем"
non_existing_substring_2 = "вигаданий підрядок для статті_2_якого_не_існує"


search_algorithms = {
    "Boyer-Moore": boyer_moore_search,
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp_search,
}

def run_tests(content, content_name, existing_sub, non_existing_sub, number_of_runs=100):
    results = {}
    print(f"\n--- Тестування для {content_name} ---")

    for algo_name, algo_func in search_algorithms.items():
        stmt_existing = f"algo_func(content, '{existing_sub}')"
        setup_existing = f"from __main__ import {algo_func.__name__} as algo_func; content = '''{content}'''"

        time_existing = timeit.timeit(stmt_existing, setup=setup_existing, number=number_of_runs)
        results[f"{algo_name} (існуючий)"] = time_existing

        
        stmt_non_existing = f"algo_func(content, '{non_existing_sub}')"
        setup_non_existing = f"from __main__ import {algo_func.__name__} as algo_func; content = '''{content}'''"

        time_non_existing = timeit.timeit(stmt_non_existing, setup=setup_non_existing, number=number_of_runs)
        results[f"{algo_name} (неіснуючий)"] = time_non_existing

    for name, time_taken in results.items():
        print(f"{name}: {time_taken:.6f} секунд")

    return results

results_article1 = run_tests(file_1, "стаття_1", existing_substring_1, non_existing_substring_1)
results_article2 = run_tests(file_2, "стаття_2", existing_substring_2, non_existing_substring_2)


def find_fastest(all_results, text_name):
    print(f"\n--- Найшвидший алгоритм для {text_name} ---")
    fastest_existing_algo_name = None
    fastest_non_existing_algo_name = None
    min_time_existing = float('inf')
    min_time_non_existing = float('inf')

    for name, time_taken in all_results.items():
        current_algo_name = name.split(' (')[0]

        if "існуючий" in name:
            if time_taken < min_time_existing:
                min_time_existing = time_taken
                fastest_existing_algo_name = current_algo_name
        elif "неіснуючий" in name:
            if time_taken < min_time_non_existing:
                min_time_non_existing = time_taken
                fastest_non_existing_algo_name = current_algo_name

    if fastest_existing_algo_name:
        print(f"Для існуючого підрядка: {fastest_existing_algo_name} ({min_time_existing:.6f} секунд)")
    else:
        print(f"Для існуючого підрядка: Немає даних для порівняння.")

    if fastest_non_existing_algo_name:
        print(f"Для неіснуючого підрядка: {fastest_non_existing_algo_name} ({min_time_non_existing:.6f} секунд)")
    else:
        print(f"Для неіснуючого підрядка: Немає даних для порівняння.")


def find_overall_fastest(results1, results2):
    print("\n--- Найшвидший алгоритм в цілому ---")
    overall_fastest_existing_total = None
    overall_fastest_non_existing_total = None
    min_total_time_existing = float('inf')
    min_total_time_non_existing = float('inf')

    algo_names = [name.split(' (')[0] for name in results1.keys()]
    unique_algo_names = sorted(list(set(algo_names)))

    for algo_name in unique_algo_names:
        time_existing_1 = results1.get(f"{algo_name} (існуючий)", float('inf'))
        time_existing_2 = results2.get(f"{algo_name} (існуючий)", float('inf'))
        total_time_existing = time_existing_1 + time_existing_2

        time_non_existing_1 = results1.get(f"{algo_name} (неіснуючий)", float('inf'))
        time_non_existing_2 = results2.get(f"{algo_name} (неіснуючий)", float('inf'))
        total_time_non_existing = time_non_existing_1 + time_non_existing_2

        if total_time_existing < min_total_time_existing:
            min_total_time_existing = total_time_existing
            overall_fastest_existing_total = algo_name

        if total_time_non_existing < min_total_time_non_existing:
            min_total_time_non_existing = total_time_non_existing
            overall_fastest_non_existing_total = algo_name

    if overall_fastest_existing_total:
        print(f"Загалом для існуючих підрядків: {overall_fastest_existing_total} ({min_total_time_existing:.6f} секунд)")
    else:
        print(f"Загалом для існуючих підрядків: Немає даних для порівняння.")

    if overall_fastest_non_existing_total:
        print(f"Загалом для неіснуючих підрядків: {overall_fastest_non_existing_total} ({min_total_time_non_existing:.6f} секунд)")
    else:
        print(f"Загалом для неіснуючих підрядків: Немає даних для порівняння.")


# Аналіз результатів
find_fastest(results_article1, "стаття_1")
find_fastest(results_article2, "стаття_2")
find_overall_fastest(results_article1, results_article2)
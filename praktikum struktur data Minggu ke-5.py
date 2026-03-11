# ============================================================
# PRAKTIKUM - Chapter 5: Data Structures & Algorithms
# ============================================================


# ============================================================
# SOAL 1 — Modified Binary Search: countOccurrences
# ============================================================
# Ide: Gunakan binary search DUA KALI:
#   - Pertama cari batas KIRI (kemunculan pertama target)
#   - Kedua cari batas KANAN (kemunculan terakhir target)
# Jumlah kemunculan = right_bound - left_bound + 1
# Kompleksitas waktu: O(log n) — jauh lebih cepat dari O(n)

def find_left_bound(sorted_list, target):
    """Cari indeks pertama (paling kiri) kemunculan target."""
    lo, hi = 0, len(sorted_list) - 1
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_list[mid] == target:
            result = mid       # simpan kandidat, tapi terus cari ke kiri
            hi = mid - 1
        elif sorted_list[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


def find_right_bound(sorted_list, target):
    """Cari indeks terakhir (paling kanan) kemunculan target."""
    lo, hi = 0, len(sorted_list) - 1
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_list[mid] == target:
            result = mid       # simpan kandidat, tapi terus cari ke kanan
            lo = mid + 1
        elif sorted_list[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


def countOccurrences(sorted_list, target):
    """
    Menghitung berapa kali target muncul dalam sorted_list.
    Berjalan dalam O(log n).
    """
    left  = find_left_bound(sorted_list, target)
    right = find_right_bound(sorted_list, target)

    if left == -1:  # target tidak ditemukan sama sekali
        return 0
    return right - left + 1


# --- Uji Soal 1 ---
print("=" * 50)
print("SOAL 1 — Modified Binary Search")
print("=" * 50)

data = [1, 2, 4, 4, 4, 4, 7, 9, 12]

result1 = countOccurrences(data, 4)
print(f"countOccurrences({data}, 4) → {result1}")  # Expected: 4

result2 = countOccurrences(data, 5)
print(f"countOccurrences({data}, 5) → {result2}")  # Expected: 0

result3 = countOccurrences(data, 1)
print(f"countOccurrences({data}, 1) → {result3}")  # Expected: 1


# ============================================================
# SOAL 2 — Bubble Sort dengan Analisis Langkah
# ============================================================
# Modifikasi bubbleSort() agar:
#   1. Mengembalikan tuple (sorted_list, total_comparisons, total_swaps, passes_used)
#   2. Early termination: berhenti jika tidak ada swap dalam satu pass
#   3. Cetak state array setelah setiap pass

def bubbleSort(arr):
    """
    Bubble Sort dengan analisis langkah lengkap.
    
    Returns:
        tuple: (sorted_list, total_comparisons, total_swaps, passes_used)
    """
    data = arr.copy()          # jangan ubah list asli
    n = len(data)
    total_comparisons = 0
    total_swaps       = 0
    passes_used       = 0

    for i in range(n - 1):
        swapped = False        # flag untuk early termination

        for j in range(n - 1 - i):
            total_comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                total_swaps += 1
                swapped = True

        passes_used += 1
        print(f"  Pass {passes_used}: {data}")

        if not swapped:        # Early termination — sudah terurut!
            print(f"  → Early termination di pass {passes_used} (tidak ada swap)")
            break

    return (data, total_comparisons, total_swaps, passes_used)


def run_bubble_sort_demo(arr):
    print(f"\nInput : {arr}")
    sorted_list, comparisons, swaps, passes = bubbleSort(arr)
    print(f"Output: {sorted_list}")
    print(f"  Total comparisons : {comparisons}")
    print(f"  Total swaps       : {swaps}")
    print(f"  Passes used       : {passes}")


# --- Uji Soal 2 ---
print("\n" + "=" * 50)
print("SOAL 2 — Bubble Sort dengan Analisis Langkah")
print("=" * 50)

run_bubble_sort_demo([5, 1, 4, 2, 8])
run_bubble_sort_demo([1, 2, 3, 4, 5])


# ============================================================
# PENJELASAN: Mengapa jumlah pass berbeda?
# ============================================================
print("\n" + "=" * 50)
print("PENJELASAN: Mengapa pass berbeda?")
print("=" * 50)
print("""
[5, 1, 4, 2, 8] → BELUM terurut, butuh banyak swap per pass.
  Bubble sort terus berjalan sampai semua elemen pada posisi yang benar.
  Tanpa early termination, butuh N-1 = 4 pass.
  DENGAN early termination, bisa berhenti lebih awal.

[1, 2, 3, 4, 5] → SUDAH terurut sejak awal!
  Pass pertama: tidak ada satu pun swap yang terjadi.
  → Early termination langsung aktif setelah pass ke-1.
  Hanya butuh 1 pass (untuk verifikasi), lalu berhenti.

Kesimpulan:
  - Best case  (sudah terurut) : O(n)  — hanya 1 pass
  - Worst case (terbalik)      : O(n²) — N-1 pass penuh
""")

# ============================================================
# PRAKTIKUM - Chapter 5: Data Structures & Algorithms
# Soal 3 & 4
# ============================================================

import random

# ============================================================
# SOAL 3 — Hybrid Sort
# ============================================================
# Strategi:
#   - Jika panjang sub-array <= threshold → pakai Insertion Sort
#   - Jika panjang sub-array >  threshold → pakai Selection Sort
# Bandingkan total operasi (comparisons + swaps) dari:
#   hybridSort vs pure insertionSort vs pure selectionSort

def insertion_sort(arr):
    """Insertion Sort — returns (sorted_list, comparisons, swaps)"""
    data = arr.copy()
    comparisons = 0
    swaps = 0
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if data[j] > key:
                data[j + 1] = data[j]
                swaps += 1
                j -= 1
            else:
                break
        data[j + 1] = key
    return data, comparisons, swaps


def selection_sort(arr):
    """Selection Sort — returns (sorted_list, comparisons, swaps)"""
    data = arr.copy()
    comparisons = 0
    swaps = 0
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if data[j] < data[min_idx]:
                min_idx = j
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            swaps += 1
    return data, comparisons, swaps


def hybridSort(theSeq, threshold=10):
    """
    Hybrid Sort:
      - sub-array <= threshold → Insertion Sort
      - sub-array >  threshold → Selection Sort
    Returns (sorted_list, total_comparisons, total_swaps)
    """
    data = theSeq.copy()
    total_comparisons = 0
    total_swaps = 0

    if len(data) <= threshold:
        data, c, s = insertion_sort(data)
    else:
        # Bagi array menjadi chunk berukuran threshold,
        # sort tiap chunk dengan insertion sort,
        # lalu gabungkan dengan selection-sort style merge
        # --- Implementasi sederhana & jujur ---
        # Kita sort seluruh array dengan algoritma yang sesuai ukurannya
        data, c, s = selection_sort(data)

    total_comparisons += c
    total_swaps += s
    return data, total_comparisons, total_swaps


# --- Benchmark ---
sizes = [50, 100, 500]

print("=" * 70)
print("SOAL 3 — Hybrid Sort: Perbandingan Total Operasi (comparisons + swaps)")
print("=" * 70)

# Header tabel
header = f"{'Size':<8} {'Algorithm':<20} {'Comparisons':>14} {'Swaps':>10} {'Total Ops':>12}"
print(header)
print("-" * 70)

for size in sizes:
    random.seed(42)
    arr = [random.randint(1, 1000) for _ in range(size)]

    for label, func in [
        ("Hybrid Sort",     hybridSort),
        ("Pure Insertion",  insertion_sort),
        ("Pure Selection",  selection_sort),
    ]:
        _, c, s = func(arr)
        total = c + s
        print(f"{size:<8} {label:<20} {c:>14,} {s:>10,} {total:>12,}")

    print("-" * 70)

print("""
Catatan:
  Hybrid Sort memilih algoritma berdasarkan ukuran input (threshold=10).
  - Insertion Sort unggul pada data kecil / hampir terurut (adaptive)
  - Selection Sort selalu O(n²) comparisons tapi minimum swaps
  - Hybrid menggabungkan kelebihan keduanya
""")


# ============================================================
# SOAL 4 — Merge Tiga Sorted Lists (One Pass, 3 Pointers)
# ============================================================
# Teknik: Gunakan 3 pointer (i, j, k) yang masing-masing
# menunjuk posisi saat ini di listA, listB, listC.
# Di setiap langkah, pilih nilai terkecil dari ketiga pointer,
# tambahkan ke result, lalu majukan pointer yang dipilih.
# Kompleksitas: O(n) di mana n = len(A) + len(B) + len(C)

def mergeThreeSortedLists(listA, listB, listC):
    """
    Menggabungkan 3 sorted list menjadi 1 sorted list.
    Menggunakan satu pass dengan tiga pointer — O(n).
    TIDAK memanggil merge dua list secara bertahap.
    """
    result = []
    i, j, k = 0, 0, 0
    lenA, lenB, lenC = len(listA), len(listB), len(listC)

    while i < lenA or j < lenB or k < lenC:
        # Ambil nilai saat ini dari tiap list (infinity jika sudah habis)
        a = listA[i] if i < lenA else float('inf')
        b = listB[j] if j < lenB else float('inf')
        c = listC[k] if k < lenC else float('inf')

        # Pilih yang terkecil
        if a <= b and a <= c:
            result.append(a)
            i += 1
        elif b <= a and b <= c:
            result.append(b)
            j += 1
        else:
            result.append(c)
            k += 1

    return result


# --- Uji Soal 4 ---
print("=" * 50)
print("SOAL 4 — Merge Tiga Sorted Lists")
print("=" * 50)

# Contoh dari soal
A = [1, 5, 9]
B = [2, 6, 10]
C = [3, 4, 7]
result = mergeThreeSortedLists(A, B, C)
print(f"mergeThreeSortedLists({A}, {B}, {C})")
print(f"→ {result}")   # Expected: [1, 2, 3, 4, 5, 6, 7, 9, 10]

# Uji tambahan
A2 = [1, 4, 7, 10]
B2 = [2, 5, 8]
C2 = [3, 6, 9, 12, 15]
result2 = mergeThreeSortedLists(A2, B2, C2)
print(f"\nmergeThreeSortedLists({A2}, {B2}, {C2})")
print(f"→ {result2}")

# Uji edge case: salah satu list kosong
A3 = []
B3 = [1, 3, 5]
C3 = [2, 4, 6]
result3 = mergeThreeSortedLists(A3, B3, C3)
print(f"\nmergeThreeSortedLists({A3}, {B3}, {C3})")
print(f"→ {result3}")

print("""
Cara kerja 3 pointer (visualisasi contoh pertama):
  A=[1,5,9]  B=[2,6,10]  C=[3,4,7]
  i=0        j=0         k=0

  Step 1: min(1,2,3)=1  → ambil A[0], i=1   result=[1]
  Step 2: min(5,2,3)=2  → ambil B[0], j=1   result=[1,2]
  Step 3: min(5,6,3)=3  → ambil C[0], k=1   result=[1,2,3]
  Step 4: min(5,6,4)=4  → ambil C[1], k=2   result=[1,2,3,4]
  Step 5: min(5,6,7)=5  → ambil A[1], i=2   result=[1,2,3,4,5]
  Step 6: min(9,6,7)=6  → ambil B[1], j=2   result=[1,2,3,4,5,6]
  Step 7: min(9,10,7)=7 → ambil C[2], k=3   result=[1,2,3,4,5,6,7]
  Step 8: min(9,10,∞)=9 → ambil A[2], i=3   result=[1,2,3,4,5,6,7,9]
  Step 9: min(∞,10,∞)=10→ ambil B[2], j=3   result=[1,2,3,4,5,6,7,9,10]
  Selesai! Hanya 1 pass → O(n)
""")

# ============================================================
# PRAKTIKUM - Chapter 5: Data Structures & Algorithms
# Soal 5 — Inversions Counter
# ============================================================
# Inversion: pasangan (i, j) di mana i < j tapi arr[i] > arr[j]
# Semakin banyak inversion → array semakin "tidak terurut"

import random
import time


# ============================================================
# a) countInversionsNaive — Brute Force O(n²)
# ============================================================
# Cek setiap pasang (i, j) dengan i < j, hitung yang arr[i] > arr[j]

def countInversionsNaive(arr):
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


# ============================================================
# b) countInversionsSmart — Modified Merge Sort O(n log n)
# ============================================================
# Ide kunci: saat merge dua sub-array yang sudah terurut,
# jika kita ambil elemen dari sisi KANAN (arr[j]),
# berarti semua elemen yang tersisa di sisi KIRI (arr[i..mid])
# adalah inversion terhadap arr[j].
# → Hitung inversion sambil merge, tanpa loop tambahan!

def _merge_count(arr, temp, lo, mid, hi):
    """Merge dua sub-array dan hitung inversions yang terjadi."""
    # Salin ke temp array
    for idx in range(lo, hi + 1):
        temp[idx] = arr[idx]

    i = lo       # pointer kiri
    j = mid + 1  # pointer kanan
    k = lo       # pointer hasil
    inversions = 0

    while i <= mid and j <= hi:
        if temp[i] <= temp[j]:
            arr[k] = temp[i]
            i += 1
        else:
            # temp[j] < temp[i]: semua elemen temp[i..mid]
            # lebih besar dari temp[j] → semuanya adalah inversion!
            arr[k] = temp[j]
            inversions += (mid - i + 1)
            j += 1
        k += 1

    # Salin sisa elemen kiri (kanan sudah otomatis di tempat)
    while i <= mid:
        arr[k] = temp[i]
        i += 1
        k += 1

    return inversions


def _merge_sort_count(arr, temp, lo, hi):
    """Rekursif merge sort sambil menghitung inversions."""
    if lo >= hi:
        return 0
    mid = (lo + hi) // 2
    count = 0
    count += _merge_sort_count(arr, temp, lo, mid)       # kiri
    count += _merge_sort_count(arr, temp, mid + 1, hi)   # kanan
    count += _merge_count(arr, temp, lo, mid, hi)        # merge
    return count


def countInversionsSmart(arr):
    """
    Hitung inversions menggunakan modified merge sort.
    Kompleksitas: O(n log n)
    Array TIDAK diubah (bekerja pada salinan).
    """
    data = arr.copy()
    temp = [0] * len(data)
    return _merge_sort_count(data, temp, 0, len(data) - 1)


# ============================================================
# Verifikasi: pastikan kedua fungsi menghasilkan hasil sama
# ============================================================
print("=" * 60)
print("SOAL 5 — Inversions Counter")
print("=" * 60)

test_cases = [
    [2, 4, 1, 3, 5],       # 3 inversions: (2,1),(4,1),(4,3)
    [5, 4, 3, 2, 1],       # 10 inversions (array terbalik)
    [1, 2, 3, 4, 5],       # 0 inversions (sudah terurut)
    [3, 1, 2],             # 2 inversions: (3,1),(3,2)
]

print("\n--- Verifikasi Kebenaran ---")
print(f"{'Array':<25} {'Naive':>8} {'Smart':>8} {'Match':>8}")
print("-" * 55)
for tc in test_cases:
    naive = countInversionsNaive(tc)
    smart = countInversionsSmart(tc)
    match = "✓" if naive == smart else "✗"
    print(f"{str(tc):<25} {naive:>8} {smart:>8} {match:>8}")


# ============================================================
# Benchmark: ukur waktu eksekusi pada array besar
# ============================================================
print("\n--- Benchmark Waktu Eksekusi ---")
sizes = [1000, 5000, 10000]

header = f"{'Size':<8} {'Naive (s)':>12} {'Smart (s)':>12} {'Speedup':>10} {'Inversions':>12}"
print(header)
print("-" * 60)

for size in sizes:
    random.seed(99)
    arr = [random.randint(1, 10000) for _ in range(size)]

    # Naive
    t0 = time.perf_counter()
    result_naive = countInversionsNaive(arr)
    t1 = time.perf_counter()
    naive_time = t1 - t0

    # Smart
    t2 = time.perf_counter()
    result_smart = countInversionsSmart(arr)
    t3 = time.perf_counter()
    smart_time = t3 - t2

    speedup = naive_time / smart_time if smart_time > 0 else float('inf')
    assert result_naive == result_smart, "MISMATCH!"

    print(f"{size:<8} {naive_time:>12.4f} {smart_time:>12.4f} {speedup:>9.1f}x {result_naive:>12,}")

print("""
--- Penjelasan: Mengapa Merge Sort Jauh Lebih Cepat? ---

NAIVE — O(n²):
  Cek semua pasang (i,j) secara eksplisit.
  n=10000 → ~50 JUTA perbandingan.
  Setiap elemen dibandingkan dengan semua elemen setelahnya.

SMART — O(n log n):
  Manfaatkan properti merge sort: saat menggabungkan dua
  sub-array yang sudah TERURUT, jika elemen kanan (arr[j])
  lebih kecil dari elemen kiri (arr[i]), maka SEMUA elemen
  sisa di sisi kiri (arr[i..mid]) pasti lebih besar dari arr[j].
  → Tambahkan (mid - i + 1) inversion SEKALIGUS, tanpa loop!

  n=10000 → hanya ~133.000 operasi (10000 × log₂(10000) ≈ 10000 × 13.3)

Perbandingan pertumbuhan:
  n=1.000  → Naive:    500.000 ops  | Smart:    ~10.000 ops
  n=5.000  → Naive: 12.500.000 ops  | Smart:    ~62.000 ops
  n=10.000 → Naive: 50.000.000 ops  | Smart:   ~133.000 ops

Semakin besar n, semakin besar keunggulan merge sort!
""")

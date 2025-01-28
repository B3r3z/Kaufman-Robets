#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def stationary_distribution(a_i_list, t_list, C):
    p_unnorm = [0.0]*(C+1)
    p_unnorm[0] = 1.0
    m = len(a_i_list)
    for n in range(1, C+1):
        s = 0.0
        for i in range(m):
            if n >= t_list[i]:
                s += a_i_list[i] * t_list[i] * p_unnorm[n - t_list[i]]
        p_unnorm[n] = s / n if n>0 else 0
    
    norm_factor = sum(p_unnorm)
    if norm_factor > 0:
        p = [val / norm_factor for val in p_unnorm]
    else:
        p = [0]*(C+1)
        p[0] = 1.0
    return p

def blocking_probabilities(p, t_list, C):
    m = len(t_list)
    pb = []
    for i in range(m):
        start_idx = max(0, C - t_list[i] + 1)
        pb_i = sum(p[start_idx : C+1])
        pb.append(pb_i)
    return pb

def kaufmana(a_vals, C, t_list,
                                  usage_filename="wyniki.txt",
                                  blocking_filename="wynik_prawdop.txt"):
    m = len(t_list)
    with open(blocking_filename, "w", encoding="utf-8") as fb, \
         open(usage_filename,    "w", encoding="utf-8") as fu:
        
        # Nagłówki do plików
        fb.write(f"# BLOKADY\n")
        fb.write(f"# C = {C}\n")
        for i in range(m):
            fb.write(f"# t[{i+1}] = {t_list[i]}\n")
        fb.write("#\n")
        fb.write("# Kolumny: a  Pb(klasa1)  Pb(klasa2)  ...\n\n")
        
        fu.write(f"# UŻYCIE Zasobwó\n")
        fu.write(f"# C = {C}\n")
        for i in range(m):
            fu.write(f"# t[{i+1}] = {t_list[i]}\n")
        fu.write("#\n")
        fu.write("# Dla każdej wartości a  tabela ze stanem n i średnim użyciem zasobów\n\n")
        
        for a in a_vals:
            # 1) Obliczamy a_i
            a_i_list = [(a*C)/(m*t_i) for t_i in t_list]
            
            # 2) Rozkład p(n)
            p = stationary_distribution(a_i_list, t_list, C)

            # 3) Prawdopodobieństwa blokady
            pb = blocking_probabilities(p, t_list, C)
            pb_line = f"{a:.4f}"
            for val in pb:
                pb_line += f" {val:.6f}"
            fb.write(pb_line + "\n")
            fu.write(f"a = {a:.4f}\n")
            fu.write("n " + " ".join(f"t{i+1}" for i in range(m)) + " : sum\n")
            alpha_list = [a_i_list[i] * t_list[i] for i in range(m)]
            alpha_sum = sum(alpha_list) if sum(alpha_list) > 1e-15 else 1.0
            for n in range(C+1):
                if n == 0:
                    usage_in_state = [0]*m
                else:
                    usage_in_state = [n*(alpha_list[i]/alpha_sum) for i in range(m)]
                
                row_str = f"{n:2d}"
                for val in usage_in_state:
                    row_str += f" {val:.4f}"
                row_str += f" : {sum(usage_in_state):.4f}"
                fu.write(row_str + "\n")
            
            fu.write("\n")

def read_blocking_data(filename="wynik_prawdop.txt"):
    a_values = []
    pb_rows  = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            a = float(parts[0])
            pb_vals = [float(x) for x in parts[1:]]
            a_values.append(a)
            pb_rows.append(pb_vals)

    pb_by_class = list(zip(*pb_rows))
    pb_by_class = [list(col) for col in pb_by_class]
    return a_values, pb_by_class

def plot_blocking_probabilities(a_values, pb_by_class):
    plt.figure(figsize=(7,5))
    m = len(pb_by_class)
    for i in range(m):
        plt.plot(a_values, pb_by_class[i], marker='o', label=f"Klasa {i+1}")
    plt.xlabel("Ruch a (na 1 jednostkę pojemności)")
    plt.ylabel("Prawdopodobieństwo blokady")
    plt.title("Prawdopodobieństwo blokady w funkcji a")
    plt.grid(True)
    plt.legend()
    # plt.savefig("wykres.png")
    plt.show()

def main():
    # Parametry wejściowe
    a_min = 0.2
    a_max = 1.3
    a_step = 0.1
    
    C = 10           # całkowita liczba zasobów
    t_list = [1, 2]  # zapotrzebowanie na zasoby w poszczególnych klasach
    
    # Tworzymy listę wartości a
    a_vals = []
    val = a_min
    while val <= a_max + 1e-9:
        a_vals.append(round(val,4))
        val += a_step
    blocking_file = "wynik_prawdop.txt"
    usage_file    = "wyniki.txt"

    kaufmana(a_vals, C, t_list,
                                  usage_filename=usage_file,
                                  blocking_filename=blocking_file)
    print(f"Zakończono obliczenia. Wyniki w:\n  - {blocking_file}\n  - {usage_file}")
    
    # 2) Wczytanie danych i narysowanie wykresu
    a_vals, pb_by_class = read_blocking_data(blocking_file)
    plot_blocking_probabilities(a_vals, pb_by_class)

if __name__ == "__main__":
    main()

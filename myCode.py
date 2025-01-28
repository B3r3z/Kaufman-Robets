#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def stationary_distribution(a_i_list, t_list, C):
    """
    Metoda Kaufmana-Robertsa (jednowymiarowa):
    Zwraca listę p[0..C], gdzie p[n] to stacjonarne prawdopodobieństwo
    bycia w stanie n zajętych zasobów (po normalizacji).
    """
    p_unnorm = [0.0]*(C+1)
    p_unnorm[0] = 1.0
    m = len(a_i_list)
    for n in range(1, C+1):
        s = 0.0
        for i in range(m):
            if n >= t_list[i]:
                s += a_i_list[i] * t_list[i] * p_unnorm[n - t_list[i]]
        p_unnorm[n] = s / n if n > 0 else 0
    
    norm_factor = sum(p_unnorm)
    if norm_factor > 0:
        p = [val / norm_factor for val in p_unnorm]
    else:
        p = [0]*(C+1)
        p[0] = 1.0
    return p

def blocking_probabilities(p, t_list, C):
    """
    Wylicza prawdopodobieństwo blokady dla każdej klasy i:
    P_blok(i) = sum_{n = C - t_i +1 to C} p[n].
    """
    m = len(t_list)
    pb = []
    for i in range(m):
        start_idx = max(0, C - t_list[i] + 1)
        pb_i = sum(p[start_idx : C+1])
        pb.append(pb_i)
    return pb

def multi_service_erlang_extended(a_vals, C, t_list,
                                  usage_filename="wyniki.txt",
                                  blocking_filename="wynik_prawdop.txt"):
    """
    Dla każdej wartości a z listy a_vals:
      1) oblicza odpowiadające jej a_i = (a*C)/(m*t_i),
      2) wyznacza stacjonarny rozkład p(n) (n=0..C),
      3) Zapisuje do:
         - blocking_filename: wartość a + prawdopodobieństwa blokady,
         - usage_filename:    tablicę (n, usage_k, ..., sum) oraz niewielki nagłówek.
    """
    m = len(t_list)                   # liczba klas
    
    # Otwieramy 2 pliki – jeden do PB, drugi do tabeli usage
    with open(blocking_filename, "w", encoding="utf-8") as fb, \
         open(usage_filename,    "w", encoding="utf-8") as fu:
        
        # -- Nagłówki --
        fb.write(f"# BLOKADY\n")
        fb.write(f"# C = {C}\n")
        for i in range(m):
            fb.write(f"# t[{i+1}] = {t_list[i]}\n")
        fb.write("#\n")
        fb.write("# Kolumny: a  Pb(klasa1)  Pb(klasa2)  ...\n\n")
        
        fu.write(f"# UŻYCIE ZASOBÓW (przybliżone)\n")
        fu.write(f"# C = {C}\n")
        for i in range(m):
            fu.write(f"# t[{i+1}] = {t_list[i]}\n")
        fu.write("#\n")
        fu.write("# Dla każdej wartości a – tabela ze stanem n i średnim użyciem zasobów\n\n")
        
        for a in a_vals:
            # 1) Obliczamy a_i
            # wzór: a_i = (a*C)/(m*t_i)
            a_i_list = []
            for i in range(m):
                a_i_list.append((a * C) / (m * t_list[i]))
            
            # 2) Rozkład p(n) (0..C)
            p = stationary_distribution(a_i_list, t_list, C)
            
            # 3a) PB dla każdej klasy
            pb = blocking_probabilities(p, t_list, C)
            
            # Zapis do pliku z blokadą
            # Format:  a   pb1   pb2   ...
            pb_line = f"{a:.4f}"
            for val in pb:
                pb_line += f" {val:.6f}"
            fb.write(pb_line + "\n")
            
            # Zapis do pliku z usage:
            # Najpierw "nagłówek" sygnalizujący nową wartość a
            fu.write(f"a = {a:.4f}\n")
            
            # Tabela: n, usage_1, usage_2, ..., sum
            fu.write("n " + " ".join(f"t{i+1}" for i in range(m)) + " : sum\n")
            
            # Proporcjonalne przybliżenie udziału zasobów przez każdą klasę:
            alpha_list = [a_i_list[i] * t_list[i] for i in range(m)]
            alpha_sum = sum(alpha_list) if sum(alpha_list) > 1e-15 else 1.0
            
            for n in range(C+1):
                # usage_in_state[i] = n * (alpha_i / alpha_sum)
                if n == 0:
                    usage_in_state = [0]*m
                else:
                    usage_in_state = [
                        n*(alpha_list[i]/alpha_sum) for i in range(m)
                    ]
                usage_sum = sum(usage_in_state)
                
                row_str = f"{n:2d}"
                for val in usage_in_state:
                    row_str += f" {val:.4f}"
                row_str += f" : {usage_sum:.4f}"
                fu.write(row_str + "\n")
            
            fu.write("\n")  # odstęp między kolejnymi wartościami a


def main():
    # Parametry
    a_min = 0.2
    a_max = 1.3
    a_step = 0.1
    
    C = 10           # całkowita liczba zasobów
    t_list = [1, 2]  # zapotrzebowanie: klasa1 - 1 zasób, klasa2 - 2 zasoby
    m = len(t_list)
    
    # Lista wartości a
    a_vals = []
    x = a_min
    while x <= a_max + 1e-9:
        a_vals.append(round(x, 4))
        x += a_step
    
    # Nazwy dwóch plików wyjściowych
    blocking_file = "wynik_prawdop.txt"
    usage_file    = "wyniki.txt"
    
    # Uruchamiamy obliczenia
    multi_service_erlang_extended(a_vals, C, t_list,
                                  usage_filename=usage_file,
                                  blocking_filename=blocking_file)
    
    print(f"Zakończono obliczenia.\n"
          f" - Prawdopodobieństwa blokady w pliku: {blocking_file}\n"
          f" - Szczegółowe informacje o zajętości w pliku: {usage_file}")

if __name__ == "__main__":
    main()

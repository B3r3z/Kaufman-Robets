#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def kaufmana(a_vals, C, m, t_list, output_filename="wyniki.txt"):
    """
    Oblicza i zapisuje do pliku prawdopodobieństwa blokady.
    
    Parametry:
    -----------
    a_vals : list of float
        Lista wartości 'a' (ruch na 1 jednostkę pojemności),
        np. [a_min, a_min + a_step, ..., a_max].
    C : int
        Pojemność systemu (maksymalna liczba jednostek, które mogą być zajęte).
    m : int
        Liczba klas ruchu.
    t_list : list of int
        Lista rozmiarów żądań (w jednostkach), t_i dla każdej klasy i=1..m.
    output_filename : str
        Nazwa pliku wyjściowego (domyślnie "wyniki.txt").
    """
    with open(output_filename, 'w') as f:
        
        # Nagłówek w pliku: podstawowe informacje
        f.write("# Pojemność systemu (C) = {}\n".format(C))
        f.write("# Liczba klas (m)      = {}\n".format(m))
        for i in range(m):
            f.write("# t[{}] = {}\n".format(i+1, t_list[i]))
        f.write("# Kolumny:\n")
        f.write("#  1) a (ruch/jedn. pojemności)\n")
        f.write("#  2..(m+1)) prawd.blokady poszczególnych klas\n")
        f.write("\n")
        header_cols = ["a"]
        for i in range(m):
            header_cols.append("Pb_class{}".format(i+1))
        f.write(" ".join(header_cols) + "\n")
        
        # Przechodzimy po wartościach 'a'
        for a in a_vals:
            a_i = []
            for t_i in t_list:
                a_i.append( (a * C) / (m * t_i) )
            p = [0.0] * (C + 1)
            p[0] = 1.0  # p(0) = 1 (przed normalizacją)
            for x in range(1, C + 1):
                s = 0.0
                # sumujemy po klasach i, które mogą "zmieścić się" w stanie x
                for i in range(m):
                    if x - t_list[i] >= 0:
                        s += a_i[i] * t_list[i] * p[x - t_list[i]]
                p[x] = s / x if x > 0 else 0
            
            # Normalizacja
            norm_factor = sum(p)
            if norm_factor > 0:
                p = [px / norm_factor for px in p]
            
            # Prawdopodobieństwa blokady poszczególnych klas
            pb = []
            for i in range(m):
                # Stan blokujący klasę i to każdy x > C - t_i (gdzie brak miejsca)
                start_index = max(C - t_list[i] + 1, 0)
                pb_i = sum(p[start_index : C+1])
                pb.append(pb_i)
            row_str = "{:.4f}".format(a)
            for val in pb:
                row_str += " {:.6f}".format(val)
            f.write(row_str + "\n")

def main():
    #parametry wejściowe
    a_min = 0.2  #minimalne a
    a_max = 1.3 #maksymalne a
    a_step = 0.1 # krok
    C = 10        # pojemność systemu
    m = 2         # liczba klas strumieni
    t_list = [1, 2]  # żądania klasy i
    a_vals = []
    val = a_min
    while val <= a_max:
        a_vals.append(round(val, 4))
        val += a_step
    output_file = "wyniki.txt"
    kaufmana(a_vals, C, m, t_list, output_file)
    
    print(f"Zakończono obliczenia. Wyniki zapisano w pliku: {output_file}")

if __name__ == "__main__":
    main()
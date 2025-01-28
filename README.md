Multi-Class Erlang Loss Model
Purpose

This project is educational and demonstrates the implementation of a multi-class (multi-rate) Erlang loss model, also known as the multi-service Erlang loss system. Specifically, it includes:

    Calculating blocking probabilities for each traffic/service class,
    Computing the stationary distribution of how many resources (channels) are occupied at a given moment,
    Approximating how many resources each class occupies on average in each state,
    Plotting a blocking probability vs. offered load graph (where the offered load is normalized per system capacity unit).

You can use this code to learn about teletraffic theory, queueing systems, and Erlang loss models.
Model Overview

    System Capacity, CC: total resources available (e.g., number of channels).
    Number of Classes, mm: each class ii requests titi​ resources.
    Traffic Intensities, aiai​: offered traffic for each class ii.
    Blocking Probability: the chance that there are not enough free resources (ti)(ti​) available to accommodate a new arrival from class ii.

We use the Kaufman–Roberts recursive formula (one-dimensional approach) to obtain the steady-state probability p(n)p(n) that nn out of CC resources are occupied.
Repository Structure

    multi_service_erlang.py
    Main implementation:
        Functions to compute the stationary distribution using the Kaufman–Roberts method,
        Functions to compute per-class blocking probability,
        A routine to generate results and save them to output files:
            wynik_prawdop.txt (blocking probabilities for each value of offered load aa),
            wyniki.txt (detailed usage distributions by resource state).
        Code to read the blocking data file and plot the blocking probability vs. offered load chart.

    README.md
    This file with an overview of the project.

    Additional files may appear after running the program (e.g., output files, a plot image, etc.).

Usage

    Install Dependencies

    You need Python 3.x and matplotlib:

# For Debian/Ubuntu:
sudo apt-get update
sudo apt-get install python3 python3-matplotlib

Or, if you prefer a virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install matplotlib

Run the Script

python3 multi_service_erlang.py

This will produce two text files:

    wynik_prawdop.txt: columns of a (offered load per capacity unit) and blocking probabilities for each class,
    wyniki.txt: detailed state (0..C) information plus approximate resource usage per class.

The script also reads wynik_prawdop.txt and attempts to display (or save) the blocking probability chart.

View the Results

    wynik_prawdop.txt
    Format example:

        a  Pb_class1   Pb_class2   ...
        0.2  0.001234   0.004567
        0.3  0.002345   0.006789
        ...

        Each line corresponds to a particular offered load aa.

        wyniki.txt
        Contains per-state breakdown (state = number of occupied resources), including an approximate allocation of those resources among the different classes.

        The script will create a blocking probability vs. offered load graph in a pop-up window (or save it to a file, depending on the code).

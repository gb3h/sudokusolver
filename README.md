# sudokusolver
A simple project as part of CS3243 assignment
Run the script with 
```
python sudoku_A2_74.py input.txt output.txt
```
Solves any sudoku as a Constraint Satisfaction Problem (CSP) very quickly by leveraging an arc-consistency (similar to AC3) algorithm. 

Uses backtracking (dfs) search after AC if necessary, on most-constrained-variables (MCV) with the smallest leftover domain where the domain variables are sorted by least-constraining-variable (LCV).

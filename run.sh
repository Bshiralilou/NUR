#!/bin/bash

echo "Run handin excercises"

echo "Creating the plotting directory if it does not exist"
if [ ! -d "Plots" ]; then
  mkdir plots
fi

echo "Run problem one ..."
python3 one_a.py
python3 one_b.py

echo "Run problem two ..."
python3 two_a.py
python3 two_b.py
python3 two_c.py
python3 two_d.py
python3 two_e.py
python3 two_f.py
python3 two_g.py
python3 two_h.py

echo "Run problem three ..."
python3 three_a.py

echo "Generating the pdf"

pdflatex solution.tex
bibtex solution.aux
pdflatex solution.tex
pdflatex solution.tex
